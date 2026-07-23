# Locumfy Technical Documentation

Professional, developer-facing technical documentation for the Locumfy platform, delivered as a small
static HTML site. No build step is required to *view* it — just open `index.html` in a browser.

## What's here

```
documentation/
  index.html                 Overview / landing + system-context diagram + doc map
  architecture.html          Layered model, 20-project solution, dependency graph
  data-layer.html            EF Core model, entity conventions, core domains, enums
  rest-api.html              API conventions, JWT auth, error mapping, endpoint inventory
  service-layer.html         Feature slices, validation engine, resolvers, DI
  domain-workflows.html      Job-application state machine, timesheet lifecycle
  ai-resume.html             Parsing → structuring → standardized/anonymized resumes → LLM features
  web-frontend.html          React/Vite website (candidate + employer)
  mobile-app.html            Flutter/Dart mobile app
  admin-analytics.html       Admin dashboard + AdminWebsiteApi / AdminCore
  operations-security.html   Running locally, configuration, and external dependencies
  README.md                  This file
  assets/
    css/docs.css             The one shared stylesheet (design tokens live in :root)
    img/                      Screenshots (copied from ../marketing) used across pages
  _shared.py                 Generator: page shell + left nav + pager
  _diagrams.py               Generator: all inline-SVG diagrams
  content_part1.py           Generator: page bodies (overview, architecture, data, api)
  content_part2.py           Generator: page bodies (services, workflows, ai, web, mobile, admin, ops)
  build.py                   Generator entry point → writes the *.html files
```

## How it was built (and how to update it)

The HTML pages are **generated** from small Python source files so the shell, navigation, and diagrams
stay consistent across pages. The generated `.html` is plain static HTML — you can edit it directly for
quick fixes, but for anything structural prefer editing the Python and re-running the build:

```bash
cd documentation
python3 build.py       # regenerates all *.html
```

### Common edits

- **Change wording / add a section paragraph:** edit the relevant `content_part*.py` body string, then
  `python3 build.py`. (Or edit the `.html` directly for a one-off — it's just HTML.)
- **Add a whole new page:** add an entry to `PAGES` in `_shared.py` (id, filename, nav label, group),
  add a body tuple in a `content_part*.py`, include it in `build.py`'s `ALL_PAGES`, and rebuild. The
  left-nav and prev/next pager update automatically.
- **Change branding / colors:** edit the design tokens in `:root` at the top of `assets/css/docs.css`.
- **Edit a diagram:** diagrams are hand-authored inline SVG in `_diagrams.py` (coordinate-based helper
  functions). Adjust the coordinates/labels and rebuild.
- **Refresh screenshots:** copy new PNGs into `assets/img/` (originals live in `../marketing/`).

### Maintenance markers inside the docs

Look for these while reading — they flag things that will need attention as the platform evolves:

- HTML comments beginning `<!-- MAINTAINER:` in the page sources.
- Purple **"Maintainer note"** callouts (`.callout.todo`) in rendered pages.

## Accuracy note

The content reflects a source-analysis snapshot (July 2026). Internal security notes and the
technical-debt register are maintained separately, outside this documentation set.

## Suggested next additions

- A generated, complete endpoint table sourced from the live Swagger `swagger.json` (the REST API page
  currently lists representative endpoints per area).
- A full entity index generated from `DataStorage/Entity/` if the data model keeps growing.
- Sequence diagrams for auth/token-renewal and resume-upload once those flows stabilize.
