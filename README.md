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
│   ├── agenda/                # Conference schedule
│   ├── tickets/               # Ticket info
│   ├── sponsors/              # Sponsor info
│   ├── cfp/                   # Call for Papers
│   ├── faq/                   # FAQ
│   ├── venue/                 # Venue details
│   └── code-of-conduct/       # Code of Conduct
├── data/                      # Structured data (YAML)
│   ├── schedule.yaml          # Two-track agenda
│   ├── sponsors.yaml          # Sponsor tiers and logos
│   └── faq.yaml               # FAQ entries
├── i18n/                      # Translation strings
│   ├── en.toml                # English UI text
│   └── da.toml                # Danish UI text
├── layouts/                   # Hugo templates
│   ├── _default/              # Base + generic templates
│   ├── partials/              # Reusable components
│   └── {page}/list.html       # Page-specific templates
├── static/                    # Static assets (copied as-is)
│   ├── css/main.css           # All styles
│   ├── js/main.js             # Countdown, nav, accordion
│   └── images/                # Logo, sponsor logos
└── .github/workflows/         # CI/CD
    └── hugo.yaml              # GitHub Pages deploy
```

## How to Edit Content

### Update the Agenda

Edit `data/schedule.yaml`. Each entry has bilingual titles:

```yaml
- time: "10:15"
  type: "parallel"
  track1:
    title:
      en: "Your Talk Title"
      da: "Din Foredragstitel"
    speaker: "Speaker Name"
  track2:
    title:
      en: "Another Talk"
      da: "Et Andet Foredrag"
    speaker: "Another Speaker"
```

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
