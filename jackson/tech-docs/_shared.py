# -*- coding: utf-8 -*-
"""Shared scaffolding for the Locumfy technical documentation static site.
This generator emits plain static HTML (no runtime build step). See README.md.
Run:  python build.py   (build.py imports everything here)."""

# (id, filename, nav-label, group)
PAGES = [
    ("index",        "index.html",                 "Overview",              "Getting Started"),
    ("architecture", "architecture.html",          "System Architecture",   "Architecture"),
    ("data",         "data-layer.html",            "Data Layer",            "Architecture"),
    ("api",          "rest-api.html",              "REST API",              "Architecture"),
    ("services",     "service-layer.html",         "Service Layer",         "Architecture"),
    ("workflows",    "domain-workflows.html",      "Domain Workflows",      "Architecture"),
    ("ai",           "ai-resume.html",             "AI & Resume Engine",    "Subsystems"),
    ("web",          "web-frontend.html",          "Web Frontend",          "Client Apps"),
    ("mobile",       "mobile-app.html",            "Mobile App",            "Client Apps"),
    ("admin",        "admin-analytics.html",       "Admin & Analytics",     "Client Apps"),
    ("ops",          "operations-security.html",   "Operations",            "Running It"),
]
GROUP_ORDER = ["Getting Started", "Architecture", "Subsystems", "Client Apps", "Running It"]
FILE_OF = {p[0]: p[1] for p in PAGES}
LABEL_OF = {p[0]: p[2] for p in PAGES}


def nav(current):
    out = ['<nav class="side">',
           '  <a class="brand" href="index.html">',
           '    <span class="logo">L</span>',
           '    <span class="name">Locumfy<small>Technical Documentation</small></span>',
           '  </a>']
    for g in GROUP_ORDER:
        out.append(f'  <div class="group">{g}</div>')
        out.append('  <ul>')
        for pid, fn, label, grp in PAGES:
            if grp != g:
                continue
            cur = 'true' if pid == current else 'false'
            out.append(f'    <li><a href="{fn}" data-nav="{pid}" data-current="{cur}">{label}</a></li>')
        out.append('  </ul>')
    out.append('</nav>')
    return "\n".join(out)


def pager(current):
    ids = [p[0] for p in PAGES]
    i = ids.index(current)
    prev_html = next_html = ""
    if i > 0:
        pid = ids[i - 1]
        prev_html = (f'<a href="{FILE_OF[pid]}" class="prev"><span class="dir">&larr; Previous</span>'
                     f'<span class="ttl">{LABEL_OF[pid]}</span></a>')
    else:
        prev_html = '<span></span>'
    if i < len(ids) - 1:
        pid = ids[i + 1]
        next_html = (f'<a href="{FILE_OF[pid]}" class="next"><span class="dir">Next &rarr;</span>'
                     f'<span class="ttl">{LABEL_OF[pid]}</span></a>')
    else:
        next_html = '<span></span>'
    return f'<div class="pager">{prev_html}{next_html}</div>'


def page(current, title, crumb, lede, body):
    """Assemble a full HTML document."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} &middot; Locumfy Docs</title>
<meta name="description" content="Locumfy platform technical documentation — {title}.">
<link rel="stylesheet" href="assets/css/docs.css">
</head>
<body data-page="{current}">
<div class="layout">
{nav(current)}
<main>
  <div class="topbar">
    <button class="menu-toggle" aria-label="Toggle navigation">&#9776;</button>
    <span class="crumb">Locumfy Docs &nbsp;/&nbsp; <b>{crumb}</b></span>
    <span class="spacer"></span>
    <span class="tag">Platform snapshot &middot; Jul 2026</span>
  </div>
  <article>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
{body}
{pager(current)}
    <p class="doc-foot">Locumfy platform technical documentation &middot; generated from source analysis &middot;
    see <a href="README.md">README</a> for how to keep this current.</p>
  </article>
</main>
</div>
<script>
  // Minimal, dependency-free: mobile nav toggle + defensive current-page highlight.
  document.querySelector('.menu-toggle')?.addEventListener('click', function () {{
    document.body.classList.toggle('nav-open');
  }});
  var pid = document.body.getAttribute('data-page');
  document.querySelectorAll('nav.side a[data-nav]').forEach(function (a) {{
    a.setAttribute('data-current', a.getAttribute('data-nav') === pid ? 'true' : 'false');
  }});
</script>
</body>
</html>
"""
