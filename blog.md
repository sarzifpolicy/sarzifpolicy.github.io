---
layout: page
title: Regulatory Updates
permalink: /blog/
wide: true
lede: Daily analysis of Pakistan's virtual asset rules, written for operators rather than lawyers. What changed, who it affects, and by when.
description: Daily plain-English analysis of PVARA, SECP, State Bank, FBR and FATF developments affecting crypto businesses in Pakistan.
---

<section class="section">
  {% if site.posts.size == 0 %}
    <div class="empty-note">
      <p>The first articles are being published now. Check back shortly, or <a href="{{ '/vasp-licensing/' | relative_url }}">start a licensing enquiry</a> in the meantime.</p>
    </div>
  {% else %}

    {% assign cats = site.categories | sort %}
    {% if cats.size > 1 %}
    <div class="sources" style="border-top:none;padding-top:0;margin-bottom:2.5rem;justify-content:flex-start">
      <span class="sources-label">Topics</span>
      <ul class="sources-list">
        {% for cat in cats %}
        <li>{{ cat[0] }} <span style="color:var(--text-faint)">({{ cat[1].size }})</span></li>
        {% endfor %}
      </ul>
    </div>
    {% endif %}

    <div class="post-grid">
      {% for post in site.posts %}
      <article class="post-card">
        <div class="blog-item-meta">
          <span class="blog-item-tag">{{ post.categories.first | default: "Regulation" }}</span>
          <span class="blog-item-date">{{ post.date | date: "%-d %b %Y" }}</span>
        </div>
        <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
        <p>{{ post.description | default: post.excerpt | strip_html | truncate: 150 }}</p>
        <a href="{{ post.url | relative_url }}" class="card-link">Read article &rarr;</a>
      </article>
      {% endfor %}
    </div>

  {% endif %}
</section>

<section class="band">
  <div class="section match-grid">
    <div class="match-content">
      <p class="section-label">Consultant matching</p>
      <h2>Applying for a licence?</h2>
      <p>Reading the rules is the first half. The second is finding an adviser who has already filed one. Tell us what you need and we will send a shortlist within two business days.</p>
      <ul class="check-list">
        <li>Free for applicants</li>
        <li>More than 25 vetted consultants worldwide</li>
        <li>No consultant pays to rank higher</li>
      </ul>
      <a href="{{ site.forms.match_short }}" class="btn-primary" target="_blank" rel="noopener">Request my shortlist</a>
    </div>
    <div class="match-panel">
      <h3>How we source these articles</h3>
      <p style="color:var(--text-dim);font-size:0.92rem">Every article is written from the primary document — the notification, circular, judgment or standard itself — not from someone else's coverage of it. Anything stating how a rule applies is reviewed by the lawyer on our team before it publishes.</p>
      <p style="margin-top:1.25rem"><a href="{{ '/editorial-policy/' | relative_url }}" class="card-link">Read our editorial policy &rarr;</a></p>
    </div>
  </div>
</section>
