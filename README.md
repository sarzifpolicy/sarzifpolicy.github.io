# Sarzif Policy

Pakistan's virtual asset regulations in plain English, plus consultant matching for VASP licence applicants.

Live at **https://sarzifpolicy.github.io**

## What is here

| Path | What it is |
|---|---|
| `index.html` | Homepage |
| `blog.md` | Article listing |
| `vasp-licensing.md` | The service page |
| `about.md` `contact.md` `editorial-policy.md` `privacy.md` | Static pages |
| `_posts/` | Published articles |
| `_layouts/` `_includes/` | Templates |
| `assets/css/style.css` | All styling |
| `_data/content-calendar.csv` | 120 queued topics |
| `_data/pointer.txt` | Next slot to publish |
| `overrides/` | Manual article drop-in — see `overrides/README.md` |
| `.github/workflows/auto-publish.yml` | 3x daily job — 07:11, 14:12, 19:23 PKT |
| `.github/scripts/publish.py` | The publisher |

## Daily publishing

**Three articles a day**, on three schedules (Pakistan Standard Time):

| Run | PKT | UTC cron |
|---|---|---|
| Morning | 07:11 | `11 2 * * *` |
| Afternoon | 14:12 | `12 9 * * *` |
| Evening | 19:23 | `23 14 * * *` |

None sit on the hour. GitHub queues every cron firing at `:00` together, so top-of-hour schedules are the most delayed and the most likely to be dropped.

Each run checks `overrides/<today>/article.md` first.

- **Manual article present and not yet used today** → publishes it, leaves the calendar pointer alone. The queued topic keeps its place.
- **Otherwise** → takes the next pending topic from the calendar, generates it with Gemini, publishes, advances the pointer.

`MAX_POSTS_PER_DAY = 3` in `publish.py` caps the total, so a double-fired or retried workflow can never flood the blog. Publish on demand from **Actions → Daily article → Run workflow**, with `dry run` to preview and `force` to override the daily cap.

**Burn rate:** 120 topics at 3/day is ~40 days. Top the calendar up around day 30.

**Did it actually publish?** Check `_data/pointer.txt`. If the number went up, it published. A green tick alone proves nothing — a dry run also finishes green.

## Setup checklist

- [ ] Repository named exactly `sarzifpolicy.github.io`, public
- [ ] Settings → Pages → source `main` / root
- [ ] Settings → Secrets and variables → Actions → secret `GEMINI_API_KEY`
- [ ] Settings → Actions → General → Workflow permissions → **Read and write**
- [ ] Google Search Console verified, code pasted into `google_site_verification` in `_config.yml`
- [ ] Sitemap `https://sarzifpolicy.github.io/sitemap.xml` submitted to Search Console

## Content rules

Enforced automatically on generated articles; the same standards apply to manual ones.

- 1000–1400 words
- H2 headings phrased as questions, answered in 40–60 words directly underneath
- Exactly one link to `https://pvara.org`
- **No links to any site except `pvara.org` and `coinconnect.site`**
- CoinConnect may appear in articles only, never on site pages
- **CoinConnect link rate-limited to one per 6 articles.** Before generating, the script reads the last 5 published posts; if any carries a CoinConnect link, the rule flips to "do not mention CoinConnect at all" and an article that ignores it is rejected. Change the frequency via `COINCONNECT_GAP` in `publish.py`
- No invented ordinance numbers, thresholds or dates
- Author byline: Noor Aslam

## Local preview

```bash
bundle install
bundle exec jekyll serve
```
