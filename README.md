# The Screen Team LLC Website

![GitHub Pages](https://img.shields.io/badge/Deploy-GitHub%20Pages-222222?logo=githubpages&logoColor=white)
![Stack](https://img.shields.io/badge/Stack-HTML%20%2B%20CSS%20%2B%20JS-0f172a)
![SEO](https://img.shields.io/badge/Focus-Local%20SEO-0ea5e9)
![Status](https://img.shields.io/badge/Site-Production-16a34a)

Production website for The Screen Team LLC, a Tampa Bay screen repair and enclosure business. This repository contains the live GitHub Pages site, the custom-domain configuration, search-engine indexing assets, and the lightweight automation used to keep the public website discoverable and maintainable.

![The Screen Team LLC website preview](Images/ScreenTeamBanner.png)

## Live Presence

- Production site: https://screenteamllc.com
- Repository: https://github.com/Screen-Team-LLC/screen-team-website
- Organization: https://github.com/Screen-Team-LLC

## What This Repo Includes

- Multi-page static business website for a real local-service company
- Service landing pages for rescreens, pool enclosures, screen lanais, window screens, garage screens, and gutter work
- Local SEO implementation with canonical URLs, Open Graph tags, Twitter cards, robots.txt, sitemap.xml, and JSON-LD structured data
- Bing site verification and Microsoft Clarity instrumentation
- AJAX contact form handling via Formspree
- GitHub Pages deployment with a custom apex domain (`screenteamllc.com`)
- GitHub Actions automation for IndexNow submission and repository health checks

## Tech Stack

- HTML5
- CSS3
- Vanilla JavaScript
- GitHub Pages
- GitHub Actions
- Formspree
- Microsoft Clarity

## Project Structure

```text
.
|-- index.html
|-- about.html
|-- contact.html
|-- rescreens.html
|-- pool-enclosures.html
|-- screen-lanais.html
|-- window-screens.html
|-- garage-screens.html
|-- gutter-work.html
|-- service-areas.html
|-- service-guarantee.html
|-- privacy-policy.html
|-- styles.css
|-- script.js
|-- sitemap.xml
|-- robots.txt
|-- CNAME
|-- Images/
`-- .github/
    `-- workflows/
```

## Key Implementation Details

- The repository is deployed directly from the `main` branch through GitHub Pages.
- The configured custom domain is the apex host: `screenteamllc.com`.
- The `www` host is intended to resolve through DNS and redirect to the apex domain.
- Structured data includes `HomeAndConstructionBusiness`, `Service`, `FAQPage`, and `BreadcrumbList` markup.
- Contact forms are progressively enhanced with JavaScript and submit through Formspree.
- Microsoft Clarity is deferred until after first paint to reduce initial render pressure.

## Local Development

There is no build step.

1. Clone the repository.
2. Start a static server from the repo root.
3. Open the site locally and test the changed pages.

Example:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`.

## Deployment

Pushes to `main` publish through GitHub Pages. The deployment depends on these files remaining correct:

- `CNAME`
- `sitemap.xml`
- `robots.txt`
- `.github/workflows/indexnow-submit.yml`

If the custom domain or HTTPS appears broken, check GitHub Pages settings first. A successful DNS check does not guarantee that the TLS certificate has already been issued.

## Search and Indexing

- XML sitemap for all public pages
- Robots policy for search crawlers
- IndexNow submission workflow on push
- Bing verification meta tag
- Open Graph and Twitter metadata for social sharing
- JSON-LD for business, service, FAQ, and breadcrumb enhancement

## Maintenance Checklist

- Keep the phone number, business copy, and service area current
- Verify forms and direct call links after major edits
- Update `sitemap.xml` when pages are added or removed
- Keep canonical URLs aligned with the GitHub Pages custom domain
- Recheck GitHub Pages HTTPS status after DNS or domain changes

## Ownership

This repository is maintained under the `Screen-Team-LLC` GitHub organization for the business website and related deployment assets.

## License

This project is published with a proprietary, all-rights-reserved license. See `LICENSE` for details.