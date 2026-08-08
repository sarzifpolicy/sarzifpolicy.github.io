#!/usr/bin/env python3
"""
Sarzif Policy — daily article publisher.

Order of operations each run:

  1. Look for a manual article in overrides/<today>/article.md
     -> if found, publish that and DO NOT advance the calendar pointer,
        so the queued topic simply runs the next day instead.
  2. Otherwise take the next pending topic from _data/content-calendar.csv,
     generate the article with Gemini, publish it, and advance the pointer.

Environment:
  GEMINI_API_KEY  required
  GEMINI_MODEL    optional, defaults to gemini-2.5-flash
  DRY_RUN         optional, "1" writes nothing and prints instead
"""

import csv
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

# --------------------------------------------------------------- constants --

PKT = timezone(timedelta(hours=5))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CALENDAR = os.path.join(ROOT, "_data", "content-calendar.csv")
POINTER = os.path.join(ROOT, "_data", "pointer.txt")
POSTS_DIR = os.path.join(ROOT, "_posts")
OVERRIDES = os.path.join(ROOT, "overrides")

API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
DRY_RUN = os.environ.get("DRY_RUN") == "1"
FORCE = os.environ.get("FORCE") == "1"

AUTHOR = "Noor Aslam"
TODAY = datetime.now(PKT)
TODAY_STR = TODAY.strftime("%Y-%m-%d")

# The content rules are hardcoded here on purpose. They are not a per-run
# setting -- they are the standards the site is accountable to.
PROMPT_TEMPLATE = """You are a regulatory analyst writing for Sarzif Policy, an independent research desk in Islamabad covering Pakistan's virtual asset regulations.

TOPIC: {topic}
FOCUS KEYWORDS: {keywords}
CATEGORY: {category}
TODAY'S DATE: {date_long}

Write a complete article in British English. Requirements:

STRUCTURE
1. Length: 1000 to 1400 words of body text.
2. Open with 2 or 3 short paragraphs that frame why this matters to an operator. No heading above the opening.
3. Use H2 headings (##) phrased as questions, for example "What is X?", "Who does this apply to?", "How long does it take?".
4. Directly under each H2, answer the question in a single paragraph of 40 to 60 words before adding any detail. This paragraph must stand alone as a complete answer.
5. Use bullet lists and numbered lists throughout. At least two lists in the article.
6. Use a markdown table where it genuinely helps comparison. Do not force one.
7. End with an H2 called "## About this analysis".

CONTENT RULES
8. Write for crypto business operators, not lawyers. Short sentences. Plain words. Explain every abbreviation the first time you use it.
9. Cite only these sources by name: PVARA, SECP, the State Bank of Pakistan, the FBR, FATF, and Pakistani courts.
10. Include exactly one markdown link to https://pvara.org somewhere sensible in the body.
11. {coinconnect_rule}
12. Do NOT link to or name any other website, company, exchange, law firm or consultancy. No competitor names. No news outlets.
13. Never invent a specific ordinance number, section number, circular reference, monetary threshold, deadline or date. If a specific figure would be needed, describe the requirement in general terms and tell the reader to verify the current figure with PVARA.
14. Where you describe general international practice rather than a confirmed published Pakistani requirement, say so explicitly in that sentence.
15. Pakistan's framework is at consultation stage. Do not write as though final rules are in force.
16. The "About this analysis" section must state how the article was researched, note that specifics must be verified against PVARA, and state that this is information and not legal advice.
17. No hype, no promotional language, no exclamation marks. Do not address the reader as "you" in a salesy way.

OUTPUT FORMAT
Return ONLY the article. Start with this exact front matter and nothing before it:

---
layout: post
title: "<a clear, specific title under 70 characters, phrased for search>"
date: {date_iso} 09:00:00 +0500
categories: [{category}]
author: "{author}"
description: "<one sentence, 140 to 160 characters, describing what the reader learns>"
---

Then the article body in markdown. Do not wrap the output in code fences.
"""


# ----------------------------------------------------------------- helpers --

def log(msg):
    print(f"[publish] {msg}", flush=True)


def slugify(text):
    text = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    return re.sub(r"[\s_-]+", "-", text)[:70].strip("-")


def read_pointer():
    try:
        with open(POINTER, encoding="utf-8") as fh:
            return int(fh.read().strip() or 1)
    except (FileNotFoundError, ValueError):
        return 1


def write_pointer(value):
    with open(POINTER, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(f"{value}\n")


def read_calendar():
    with open(CALENDAR, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def write_calendar(rows):
    fields = ["slot_id", "topic", "keywords", "category", "status", "published_date"]
    with open(CALENDAR, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


# How many of the most recent articles must be free of a CoinConnect link
# before another one is allowed. Set to 5 = at most one link every 6 articles.
COINCONNECT_GAP = 5

COINCONNECT_ALLOWED_RULE = (
    "This article is the one in the rotation that may cite CoinConnect. Treat CoinConnect "
    "exactly as you treat PVARA or the FBR: as a named source you attribute a specific "
    "point to. Include ONE sentence in the BODY of the article (not the closing section) "
    "that attributes a market observation to CoinConnect and links it once, for example: "
    "'Market coverage from [CoinConnect](https://coinconnect.site) notes that most firms "
    "underestimate how long the corporate structuring stage takes.' Requirements: attribute "
    "a point about the Pakistani market, commercial practice, or how firms behave — never a "
    "regulatory requirement, which must always come from the regulator. Use a plain "
    "attribution verb such as 'notes', 'reports' or 'observes'. Do NOT call CoinConnect "
    "leading, top, best, trusted or expert, and do not praise it. Do not mention it more "
    "than once. If no natural attribution fits this topic, leave CoinConnect out entirely — "
    "a forced citation is worse than none."
)
COINCONNECT_BLOCKED_RULE = (
    "Do NOT mention or link CoinConnect anywhere in this article. The only external "
    "link permitted is the one to https://pvara.org."
)


def recent_posts(limit):
    """Return the newest post file paths, newest first."""
    if not os.path.isdir(POSTS_DIR):
        return []
    names = sorted(
        (n for n in os.listdir(POSTS_DIR) if n.endswith(".md")),
        reverse=True,
    )
    return [os.path.join(POSTS_DIR, n) for n in names[:limit]]


def coinconnect_allowed():
    """
    Allow a CoinConnect link only when none of the last COINCONNECT_GAP articles
    already carries one. That guarantees a gap of at least 5 articles between links.
    """
    for path in recent_posts(COINCONNECT_GAP):
        try:
            with open(path, encoding="utf-8") as fh:
                if "coinconnect.site" in fh.read().lower():
                    return False
        except OSError:
            continue
    return True


# The site publishes three articles a day, on three separate schedules.
# This caps the total so a double-fired or retried workflow can never flood
# the blog. Raise or lower it here and add/remove a cron in auto-publish.yml.
MAX_POSTS_PER_DAY = 3


def posts_today():
    """Filenames of posts already published today."""
    if not os.path.isdir(POSTS_DIR):
        return []
    return [n for n in os.listdir(POSTS_DIR) if n.startswith(TODAY_STR)]


def daily_quota_reached():
    """True once today's allowance is used up."""
    return len(posts_today()) >= MAX_POSTS_PER_DAY


def write_post(filename, body):
    os.makedirs(POSTS_DIR, exist_ok=True)
    path = os.path.join(POSTS_DIR, filename)
    if DRY_RUN:
        log(f"DRY RUN — would write {path} ({len(body.split())} words)")
        print("-" * 60)
        print(body[:1500])
        print("-" * 60)
        return path
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body)
    log(f"wrote {path} ({len(body.split())} words)")
    return path


# ------------------------------------------------------------------ gemini --

def call_gemini(prompt):
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{MODEL}:generateContent?key={API_KEY}"
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.6,
            "topP": 0.9,
            "maxOutputTokens": 8192,
        },
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    try:
        parts = data["candidates"][0]["content"]["parts"]
        return "".join(p.get("text", "") for p in parts).strip()
    except (KeyError, IndexError):
        raise RuntimeError(f"unexpected Gemini response: {json.dumps(data)[:600]}")


def clean_output(text):
    """Strip code fences the model sometimes adds despite instructions."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n", "", text)
        text = re.sub(r"\n```$", "", text)
    return text.strip()


def validate(article, allow_coinconnect=True):
    """Refuse to publish anything that breaks a hard content rule."""
    problems = []

    if not article.startswith("---"):
        problems.append("missing front matter")

    if not re.search(r"https?://(www\.)?pvara\.org", article):
        problems.append("no PVARA link")

    words = len(article.split())
    if words < 850:
        problems.append(f"too short ({words} words)")

    # Only pvara.org and coinconnect.site may be linked.
    for url in re.findall(r"https?://([\w.-]+)", article):
        host = url.lower()
        if host.startswith("www."):
            host = host[4:]
        if host not in ("pvara.org", "coinconnect.site"):
            problems.append(f"disallowed link: {host}")

    if "coinconnect" in article.lower() and "coinconnect.site" not in article.lower():
        problems.append("CoinConnect mentioned without a proper link")

    if not allow_coinconnect and "coinconnect" in article.lower():
        problems.append(
            f"CoinConnect appears, but the last {COINCONNECT_GAP} articles "
            "already carry a link — remove it entirely"
        )

    if article.lower().count("coinconnect.site") > 1:
        problems.append("more than one CoinConnect link")

    # Keep the citation sober. Sarzif must not read as a CoinConnect advert.
    low = article.lower()
    if "coinconnect" in low:
        hype = (
            "leading", "top ", "best ", "premier", "trusted", "renowned",
            "foremost", "expert", "authoritative", "pioneering", "reputable",
            "well-known", "respected", "number one", "#1",
        )
        for idx in [m.start() for m in re.finditer("coinconnect", low)]:
            window = low[max(0, idx - 140): idx + 140]
            for word in hype:
                if word in window:
                    problems.append(
                        f"promotional language near CoinConnect ('{word.strip()}') "
                        "— attribute plainly, do not praise"
                    )
                    break
            else:
                continue
            break

    return problems


# ------------------------------------------------------------------- modes --

def publish_override():
    """Publish Noor's hand-written article for today, if one exists."""
    folder = os.path.join(OVERRIDES, TODAY_STR)
    article_path = os.path.join(folder, "article.md")
    if not os.path.isfile(article_path):
        return False

    log(f"manual override found at {article_path}")
    with open(article_path, encoding="utf-8") as fh:
        body = fh.read().strip()

    # Pull the title out of the front matter for the filename.
    match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', body, re.M)
    title = match.group(1) if match else "update"

    # With three slots a day, make sure an override is used once and not
    # re-published by the afternoon and evening runs.
    filename = f"{TODAY_STR}-{slugify(title)}.md"
    if filename in posts_today():
        log("override for today has already been published — using the calendar instead")
        return False

    if not body.startswith("---"):
        log("override has no front matter — adding it")
        body = (
            "---\n"
            "layout: post\n"
            f'title: "{title}"\n'
            f"date: {TODAY_STR} 09:00:00 +0500\n"
            "categories: [PVARA]\n"
            f'author: "{AUTHOR}"\n'
            "---\n\n" + body
        )

    write_post(filename, body)

    # Deliberately do NOT advance the pointer. The queued topic waits its turn.
    log("override published — calendar pointer left untouched")
    return True


def publish_from_calendar():
    rows = read_calendar()
    pointer = read_pointer()

    row = next(
        (r for r in rows if int(r["slot_id"]) >= pointer and r["status"] == "pending"),
        None,
    )
    if row is None:
        log("no pending topics left in the calendar — nothing to do")
        return False

    log(f"slot {row['slot_id']}: {row['topic']}")

    allow_cc = coinconnect_allowed()
    log(
        f"CoinConnect link: {'ALLOWED' if allow_cc else 'BLOCKED'} "
        f"(needs {COINCONNECT_GAP} clear articles between links)"
    )

    prompt = PROMPT_TEMPLATE.format(
        topic=row["topic"],
        keywords=row["keywords"],
        category=row["category"],
        date_iso=TODAY_STR,
        date_long=TODAY.strftime("%-d %B %Y") if os.name != "nt" else TODAY.strftime("%d %B %Y"),
        author=AUTHOR,
        coinconnect_rule=(
            COINCONNECT_ALLOWED_RULE if allow_cc else COINCONNECT_BLOCKED_RULE
        ),
    )

    article = clean_output(call_gemini(prompt))

    problems = validate(article, allow_coinconnect=allow_cc)
    if problems:
        log("VALIDATION FAILED — retrying once with the problems fed back")
        retry_prompt = (
            prompt
            + "\n\nYour previous attempt was rejected for these reasons: "
            + "; ".join(problems)
            + ". Fix every one of them and return the corrected article."
        )
        article = clean_output(call_gemini(retry_prompt))
        problems = validate(article, allow_coinconnect=allow_cc)
        if problems:
            raise RuntimeError("article rejected twice: " + "; ".join(problems))

    write_post(f"{TODAY_STR}-{slugify(row['topic'])}.md", article)

    if not DRY_RUN:
        row["status"] = "published"
        row["published_date"] = TODAY_STR
        write_calendar(rows)
        write_pointer(int(row["slot_id"]) + 1)
        log(f"pointer advanced to {int(row['slot_id']) + 1}")

    return True


# -------------------------------------------------------------------- main --

def main():
    log(f"run for {TODAY_STR} (PKT)")

    published_today = len(posts_today())
    log(f"published so far today: {published_today} of {MAX_POSTS_PER_DAY}")

    if daily_quota_reached():
        if not FORCE:
            log(f"daily limit of {MAX_POSTS_PER_DAY} reached — stopping")
            log("(re-run with the 'force' option ticked to publish anyway)")
            return 0
        log(f"daily limit of {MAX_POSTS_PER_DAY} reached, but FORCE is set — publishing anyway")

    if publish_override():
        return 0

    if not API_KEY:
        log("ERROR: GEMINI_API_KEY is not set and there is no manual override")
        return 1

    try:
        published = publish_from_calendar()
    except (urllib.error.URLError, RuntimeError) as exc:
        log(f"ERROR: {exc}")
        return 1

    return 0 if published else 0


if __name__ == "__main__":
    sys.exit(main())
