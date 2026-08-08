# How to publish your own article

**Noor — this is for you. No software to install. Everything happens in your web browser.**

The site publishes three articles a day on its own — at **7:11am, 2:12pm and 7:23pm** Pakistan time. You do not need to do anything for that to happen.

This page is for the days when you want to publish **your own** article instead.

---

## The short version

You put your article in a folder named after the date you want it to appear. That morning, the site publishes yours instead of the automatic one.

**Nothing is lost.** The topic that was queued for that day simply moves to the next day. The queue never skips.

---

## Step by step

### 1. Open the repository

Go to **https://github.com/sarzifpolicy/sarzifpolicy.github.io**

Sign in if it asks.

### 2. Start a new file

Near the top right, click the **`Add file`** button, then choose **`Create new file`**.

### 3. Type the file path

You will see a box at the top with the repository name and an empty field next to it.

Type this into that field, changing the date to the day you want the article to appear:

```
overrides/2026-08-15/article.md
```

**Type the forward slashes `/` as you go.** GitHub creates the folders automatically as you type them. You do not need to make the folders separately.

The date must be written **year-month-day**, with dashes, and always four digits then two then two. `2026-08-15`, not `15-08-2026` and not `2026-8-15`.

The file must be called **`article.md`** exactly.

### 4. Write your article

In the big text box underneath, start with this block, exactly as shown:

```
---
layout: post
title: "Your headline goes here"
date: 2026-08-15 09:00:00 +0500
categories: [PVARA]
author: "Noor Aslam"
description: "One sentence saying what the reader will learn. Around 150 characters."
---
```

Then write your article below it.

**Three things to get right:**

- Keep the three dashes `---` on their own lines, top and bottom. They tell the site where the settings end and the article begins.
- The **date** must match the folder name.
- **categories** must be one of: `PVARA`, `Licensing`, `AML`, `Tax`

### 5. Write in Markdown

Markdown is just plain text with a few marks for formatting:

| To get this | Type this |
|---|---|
| A section heading | `## Your heading here` |
| **Bold text** | `**bold text**` |
| A bullet point | `- your point` |
| A numbered point | `1. your point` |
| A link | `[the words](https://pvara.org)` |

Leave a blank line between paragraphs.

### 6. Save it

Scroll to the bottom. Click the green **`Commit changes`** button, then **`Commit changes`** again in the box that appears.

**That is it.** The article will publish on the morning of the date you chose.

---

## Do it before 7:11am

The site checks for your article at **7:11am** Pakistan time — the first of the day's three runs. Add it any time before then. The night before is safest.

Your article takes the place of the 7:11am automatic one. The other two, at 2:12pm and 7:23pm, still publish from the queue as normal, so the site still gets three articles that day.

**Missed the deadline, or want it live right now?**

1. Click the **`Actions`** tab at the top of the repository
2. Click **`Daily article`** in the left-hand list
3. Click **`Run workflow`** on the right
4. Tick **`force`**
5. Click the green **`Run workflow`**

It publishes within about two minutes.

---

## The house rules

Every article on this site follows these. The automatic ones are checked by machine; yours are down to you.

- **1000 words or more**
- **Headings written as questions** — "What is a VASP?" rather than "VASP definition"
- **Answer the question in the first 40 to 60 words** underneath each heading, before adding detail
- **Use bullet points and numbered lists**
- **Link to https://pvara.org once**
- **Do not link to any other website** except CoinConnect. No competitors, no news sites, no law firms
- **CoinConnect at most once every six articles.** The automatic articles handle this themselves — the system checks the last five and stays silent if any already links there. If you are writing your own, check the five most recent articles on the site first, and leave CoinConnect out if any of them mentions it. Too many links to the same site looks like spam to Google and devalues every one of them
- **Never invent** an ordinance number, a section number, a monetary threshold or a deadline. If you need a specific figure and cannot confirm it, describe the requirement in general terms instead
- **Say when something is general practice** rather than a confirmed Pakistani rule
- **End with a section called `## About this analysis`** explaining how it was researched and stating it is information, not legal advice

---

## A template to start from

Copy everything below into a new file and edit it.

```
---
layout: post
title: "What is the travel rule and how does it affect Pakistani exchanges?"
date: 2026-08-15 09:00:00 +0500
categories: [AML]
author: "Noor Aslam"
description: "The travel rule requires exchanges to share sender and recipient details on transfers. Here is what it means for firms operating in Pakistan."
---

Two or three short paragraphs setting up why this matters to someone running a
crypto business. No heading above this part.

## What is the travel rule?

Answer the question here in 40 to 60 words. Keep it complete on its own, so a
reader who stops here still has the answer. Then carry on with the detail below.

More explanation. Then a list:

- First point
- Second point
- Third point

## Who does it apply to?

Another 40 to 60 word answer, then detail.

## What should firms do about it?

1. First step
2. Second step
3. Third step

## About this analysis

This article was prepared by the Sarzif Policy research desk from primary
regulatory sources. Pakistan's framework is at consultation stage and detail
will change. Verify any specific requirement against the current position
published by [PVARA](https://pvara.org) before acting on it.

This is information, not legal advice.
```

---

## Common mistakes

| What went wrong | The fix |
|---|---|
| Article did not appear | Folder date did not match today. Check the spelling of the folder |
| Page looks broken | A `---` line is missing or has extra spaces. There must be exactly three dashes on their own line |
| File in the wrong place | It must be `overrides/DATE/article.md`. The file name must be exactly `article.md` |
| Date shows wrong | The `date:` inside the file does not match the folder name. They must be the same day |
| Two articles published | You added an override and also ran the workflow with `force` ticked |

---

## Adding a reference document

You can put a PDF or any other file in the same dated folder. Only `article.md` gets published — everything else just stays in the repository as your working record.

---

## Questions

If something does not work, take a screenshot of what you see and send it on. Do not delete anything and try again — it is much easier to fix when the mistake is still visible.
