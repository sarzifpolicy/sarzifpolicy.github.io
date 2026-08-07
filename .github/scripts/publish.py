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
11. You may include at most one markdown link to https://coinconnect.site if it fits naturally as background reading. If it does not fit, leave it out.
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


def post_exists_for_today():
    """Guard against double-publishing if the workflow is triggered twice."""
    if not os.path.isdir(POSTS_DIR):
        return False
    return any(name.startswith(TODAY_STR) for name in os.listdir(POSTS_DIR))


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


def validate(article):
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

    write_post(f"{TODAY_STR}-{slugify(title)}.md", body)

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

    prompt = PROMPT_TEMPLATE.format(
        topic=row["topic"],
        keywords=row["keywords"],
        category=row["category"],
        date_iso=TODAY_STR,
        date_long=TODAY.strftime("%-d %B %Y") if os.name != "nt" else TODAY.strftime("%d %B %Y"),
        author=AUTHOR,
    )

    article = clean_output(call_gemini(prompt))

    problems = validate(article)
    if problems:
        log("VALIDATION FAILED — retrying once with the problems fed back")
        retry_prompt = (
            prompt
            + "\n\nYour previous attempt was rejected for these reasons: "
            + "; ".join(problems)
            + ". Fix every one of them and return the corrected article."
        )
        article = clean_output(call_gemini(retry_prompt))
        problems = validate(article)
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

    if post_exists_for_today():
        log("a post already exists for today — stopping so nothing is duplicated")
        return 0

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
