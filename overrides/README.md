# Manual article override

This folder lets Noor publish her own article on any given day **without breaking the automation**.

## How it works

Every morning at 06:00 PKT the workflow checks `overrides/<today's date>/article.md` first.

- **If that file exists** — it publishes Noor's article and **does not advance the calendar pointer**. The topic that was queued for today simply runs tomorrow instead. Nothing is skipped or lost.
- **If it does not exist** — it takes the next pending topic from `_data/content-calendar.csv`, generates the article with Gemini, publishes it, and moves the pointer on by one.

Only one article publishes per day either way.

## How to publish your own article

1. Create a folder named with the date you want it to go out, in `YYYY-MM-DD` format:

   ```
   overrides/2026-08-15/
   ```

2. Put your article inside it as `article.md`.

3. Start the file with this front matter:

   ```
   ---
   layout: post
   title: "Your headline here"
   date: 2026-08-15 09:00:00 +0500
   categories: [PVARA]
   author: "Noor Aslam"
   description: "One sentence describing what the reader learns."
   ---
   ```

   Then write the article below it in markdown.

   Categories in use: `PVARA`, `Licensing`, `AML`, `Tax`.

4. Commit it before 06:00 PKT on that date. That is all — the workflow does the rest.

If you forget the front matter, the script adds a basic version automatically, but you will get a better result by including it.

## Supporting files

You can drop a reference PDF or any other file in the same folder. Only `article.md` is published; everything else stays in the repository as your working record.

## Publishing immediately instead of waiting

Go to the **Actions** tab → **Daily article** → **Run workflow**. It runs straight away using the same rules.

To preview without publishing, tick **dry run** when you start it. The article is generated and shown in the log but nothing is committed.

## Content rules the automation enforces

Generated articles are rejected and regenerated if they break any of these:

- Fewer than 850 words
- No link to `https://pvara.org`
- A link to any site other than `pvara.org` or `coinconnect.site`
- Missing front matter

These rules are in `.github/scripts/publish.py`. The same standards apply to manual articles, but nobody checks those automatically — that is on the writer.
