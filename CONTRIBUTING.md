# Contributing

This repository powers a live business website. Treat every change as a production change.

## Before You Start

- Confirm the business goal of the change: conversion, SEO, trust, content accuracy, or deployment reliability.
- Keep the site static unless there is a clear reason to introduce additional complexity.
- Preserve the custom-domain deployment model used by GitHub Pages.

## Local Workflow

1. Create a branch from `main`.
2. Preview the site locally with a static server.
3. Test all pages you touched on desktop and mobile widths.
4. Confirm forms, links, metadata, and structured data still make sense.
5. Open a pull request with a focused summary.

## Content Standards

- Keep copy direct, local, and service-oriented.
- Do not add claims that cannot be supported.
- Use the configured apex domain `https://screenteamllc.com` for canonical and structured-data URLs.
- Prefer updating existing pages over adding unnecessary new pages.

## Technical Standards

- Keep CSS and JavaScript lightweight.
- Avoid introducing frameworks or build tooling without a strong operational reason.
- Validate relative links, phone links, forms, and image paths before merging.
- Keep `robots.txt`, `sitemap.xml`, and `CNAME` in sync with the live site.

## Pull Request Checklist

- The purpose of the change is clear.
- The affected pages were previewed locally.
- No broken internal links were introduced.
- Metadata still reflects the live canonical domain.
- Search/indexing assets remain correct.
- Screenshots are included for visible UI changes.