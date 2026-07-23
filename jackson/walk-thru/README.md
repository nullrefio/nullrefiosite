# Locumfy — Business Walkthrough

A professional, **non-technical** walkthrough of the Locumfy platform, written for business
leaders and decision-makers in medical recruiting. Open `index.html` in any web browser — no
build step, no internet connection, no software required.

> Looking for the **developer / architect** documentation instead? That lives in
> `../tech-docs/` — open `../tech-docs/index.html`.

## What's here

```
walk-thru/
  index.html        The walkthrough — a single self-contained HTML page
  assets/img/        Screenshots (copied from ../../marketing), referenced by index.html
  README.md          This file
```

## The story it tells

1. **Overview** — what Locumfy is, in one line
2. **The Problem** — why medical recruiting needs it
3. **How It Works** — the ecosystem, at a glance (diagram)
4. **Two Audiences** — the professional's mobile app vs. the facility web portal
5. **The Journey** — resume → verified profile → jobs → work → timesheet → paid (diagram)
6. **The Engine** — the resume parsing / verification / anonymization moat (diagram)
7. **Network** — the LinkedIn-style social graph and network effect
8. **Product Tour** — real screenshots of the built prototype
9. **Oversight & Insight** — the admin/analytics dashboard
10. **Business Model** — how Locumfy earns (pricing concepts)
11. **Roadmap** — what's built and what's next
12. **About this document** — how to keep it current

## How to update it

Everything is in `index.html`. It is plain HTML with all styling inline — safe to edit directly.

- **Change wording:** each part of the page is a `<section id="...">` with a clear heading. Find
  the text and edit it. Update the matching link in the top `<nav class="topnav">` if you rename
  or add a section.
- **Change brand colors:** edit the CSS variables in `:root` at the top of the `<style>` block
  (search for `--brand`).
- **Refresh screenshots:** replace the files in `assets/img/` keeping the same filenames.
  Originals live in `../../marketing/` (mobile/, website/, adminsite/, other/).
- **Edit a diagram:** the four diagrams are hand-drawn inline `<svg>` inside
  `<figure class="diagram">` — adjust the shapes/labels directly.
- **Find what needs attention:** search the file for `MAINTAINER:` — these HTML comments flag every
  spot likely to need updating as the platform evolves (illustrative figures, pricing, diagrams).

## Accuracy note

Some figures are **illustrative** — seed-data counts (~250k resumes, 21 brands), the 660k projected
connections, the admin dashboard metrics, and the pricing tiers come from concept research and demo
data, not live production. They are labelled as such in the document. Before showing this to any
external party, confirm which numbers can be stated as fact and label the rest as estimates — see
the investor-deck conventions in `../../marketing/CLAUDE.md`.

## Content sources (as of Jul 2026)

- `../../CLAUDE.md` — platform description, workflows, project inventory
- `../../marketing/summary.txt` — concept, data curation buckets, link-scoring stats
- `../../marketing/todo.txt` — roadmap / planned features
- `../../marketing/CLAUDE.md` — messaging pillars, audience & tone
