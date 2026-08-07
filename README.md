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
| `.github/workflows/auto-publish.yml` | Daily 06:00 PKT job |
| `.github/scripts/publish.py` | The publisher |

## Daily publishing

At 06:00 PKT the workflow checks `overrides/<today>/article.md`.

- **Manual article present** → publishes it, leaves the calendar pointer alone. The queued topic runs the next day.
- **No manual article** → takes the next pending topic from the calendar, generates it with Gemini, publishes, advances the pointer.

One article per day either way. Publish on demand from **Actions → Daily article → Run workflow**, with a dry-run option to preview without committing.

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
- No invented ordinance numbers, thresholds or dates
- Author byline: Noor Aslam

## Local preview

```bash
bundle install
bundle exec jekyll serve
```
