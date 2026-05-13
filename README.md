# BSides Aarhus 2026 Website

Official website for [BSides Aarhus 2026](https://bsidesaarhus.dk) — a community-driven security conference in Aarhus, Denmark.

**Date:** June 20, 2026
**Venue:** INCUBA Next, Katrinebjerg, Aarhus

## Tech Stack

- [Hugo](https://gohugo.io/) — static site generator
- Plain CSS (custom properties, no frameworks)
- Vanilla JavaScript
- GitHub Actions → GitHub Pages deployment
- Bilingual: English (default) + Danish (`/da/`)

## Local Development

### Prerequisites

Install Hugo (extended edition):

```bash
# macOS
brew install hugo

# Linux (Debian/Ubuntu)
sudo apt install hugo

# Or download from https://gohugo.io/installation/
```

Verify installation:

```bash
hugo version
# Should show: hugo v0.147.0+extended or newer
```

### Run Locally

```bash
# Clone the repository
git clone https://github.com/BSides-Aarhus/Website-2026.git
cd Website-2026

# Start the development server
hugo server

# Site is now live at http://localhost:1313/
# Danish version at http://localhost:1313/da/
```

The dev server watches for file changes and reloads automatically.

### Build for Production

```bash
hugo --gc --minify
```

Output goes to `public/` (gitignored).

### Useful Development Commands

```bash
# Run with draft content visible
hugo server -D

# Run on a different port
hugo server --port 8080

# Build and check for broken links
hugo --gc --minify 2>&1 | grep -i "error"

# Check which pages were generated
hugo --gc --minify && find public -name "*.html" | wc -l
```

## Project Structure

```
├── hugo.toml                  # Site configuration (languages, menus, params)
├── content/                   # Page content (Markdown)
│   ├── _index.md              # Homepage (EN)
│   ├── _index.da.md           # Homepage (DA)
│   ├── agenda/                # Time-grid schedule page
│   ├── sessions/              # One file per talk (title, time, room, speakers, abstract)
│   ├── speakers/              # One file per speaker (name, tagline, links, bio)
│   ├── tickets/               # Ticket info
│   ├── sponsors/              # Sponsor info
│   ├── cfp/                   # Call for Papers
│   ├── faq/                   # FAQ
│   ├── venue/                 # Venue details
│   └── code-of-conduct/       # Code of Conduct
├── data/                      # Structured data (YAML)
│   ├── schedule.yaml          # Time grid — references sessions by slug
│   ├── sponsors.yaml          # Sponsor tiers and logos
│   └── faq.yaml               # FAQ entries
├── i18n/                      # Translation strings
│   ├── en.toml                # English UI text
│   └── da.toml                # Danish UI text
├── layouts/                   # Hugo templates
│   ├── _default/              # Base + generic templates
│   ├── 404.html               # 404 page (redirects /en/* → /)
│   ├── agenda/list.html       # Time-grid agenda
│   ├── sessions/              # Session detail + index
│   ├── speakers/              # Speaker detail + index
│   └── partials/              # Reusable components + JSON-LD schema
├── static/                    # Static assets (copied as-is)
│   ├── css/main.css           # All styles
│   ├── js/main.js             # Countdown, nav, accordion
│   └── images/
│       ├── speakers/          # Speaker headshots ({slug}.jpg|png|webp)
│       └── sponsors/          # Sponsor logos
├── scripts/
│   ├── fetch-tickets.sh       # CI step: pulls live ticket data
│   └── sync-translations.sh   # Mirrors content/sessions+speakers/*.md → *.da.md
├── worker/                    # Cloudflare Worker — Ticket Butler API proxy
│   ├── ticket-proxy.js
│   └── wrangler.toml
└── .github/workflows/         # CI/CD
    └── hugo.yaml              # GitHub Pages deploy
```

## How to Edit Content

### Add a Speaker

Create `content/speakers/{slug}.md` (slug is lowercase-with-hyphens, e.g. `jane-doe`):

```markdown
---
title: "Jane Doe"
tagline: "Security Engineer at Example Corp"
links:
  linkedin: https://www.linkedin.com/in/janedoe/
  website: https://example.com
  company: https://example-corp.com
---

Bio paragraph one (third-person, BSides Aarhus editorial voice).

Bio paragraph two.
```

Drop a headshot at `static/images/speakers/{slug}.jpg|png|webp`. If no photo
is provided, an initials avatar is rendered automatically.

### Add a Session

Create `content/sessions/{slug}.md`:

```markdown
---
title: "Talk Title"
time: "10:00"
room: "Room 1"
speakers:
  - jane-doe
  - joost-van-dijk
---

Abstract paragraph one.

- Bullet items render as lists.
- Use blank lines around lists.

Abstract paragraph two.
```

### Wire the Session Into the Schedule

Edit `data/schedule.yaml`. Parallel slots reference sessions by slug:

```yaml
- time: "10:00"
  type: parallel
  track1: webauthn-passwordless
  track2: kernel-wars-anti-cheat
```

Other slot types:

```yaml
- time: "11:45"
  type: break
  title:
    en: Lunch
    da: Frokost

- time: "16:30"
  type: plenary
  title:
    en: Continue at Fredagscaféen
    da: Vi fortsætter på Fredagscaféen
  description:
    en: Optional muted subtitle.
    da: Valgfri underrubrik.
  url: https://fredagscafeen.dk/  # optional — makes the title a link
```

### Translations (Sessions and Speakers)

Talks are held in English, so the same content shows on `/sessions/{slug}/`
and `/da/sessions/{slug}/`. The `*.da.md` mirrors are maintained by a script:

```bash
./scripts/sync-translations.sh
```

CI runs this automatically before every Hugo build, so forgetting to run it
locally is harmless. To provide a real Danish translation for a specific
session or speaker, edit the `.da.md` file directly — but note that the next
CI run will overwrite it. Lift it out of the sync set by adding the slug to
the `case` block in `scripts/sync-translations.sh` if you need divergent
content.

### Add a Sponsor

1. Add the logo image to `static/images/sponsors/`
2. Edit `data/sponsors.yaml`:

```yaml
tiers:
  - name:
      en: "Gold Sponsors"
      da: "Guld Sponsorer"
    level: "gold"
    sponsors:
      - name: "Company Name"
        logo: "/images/sponsors/company.png"
        url: "https://company.com"
```

### Update FAQ

Edit `data/faq.yaml` — each entry has bilingual Q&A:

```yaml
- question:
    en: "Your question?"
    da: "Dit spørgsmål?"
  answer:
    en: "The answer."
    da: "Svaret."
```

### Edit Page Content

Content pages live in `content/`. Each page has an English (`.md`) and Danish (`.da.md`) version. Edit the Markdown as needed.

### Edit UI Text (Buttons, Labels)

Translation strings are in `i18n/en.toml` and `i18n/da.toml`.

## Deployment

The site deploys automatically via GitHub Actions when changes are pushed to `main`.

### First-Time Setup (GitHub)

1. Go to **Settings > Pages** in the repository
2. Set **Source** to "GitHub Actions"
3. Set **Custom domain** to `bsidesaarhus.dk`
4. Enable **Enforce HTTPS**

### DNS Configuration

Create a CNAME record:

```
bsidesaarhus.dk → bsides-aarhus.github.io
```

## Links

- Website: https://bsidesaarhus.dk
- Tickets: https://bsidesaarhus.ticketbutler.io/en/e/bsides-aarhus-2026/
- CFP: https://sessionize.com/bsides-aarhus-2026/
- LinkedIn: https://www.linkedin.com/company/bsides-aarhus/

## License

[GPL-3.0](LICENSE)
