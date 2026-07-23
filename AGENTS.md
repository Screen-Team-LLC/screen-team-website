# Screen Team LLC — Agent Instructions

**Domain:** `screenteamllc.com`  
**Site folder:** `E:\All Client Websites\Screen-Team-LLC-screen-team-website`

## Website Audit / GSC

Umbrella: `E:\Website Audit`  
GSC module: `E:\Website Audit\GSC`  
Config: `E:\Website Audit\GSC\sites\screenteamllc.com.json`

Site config: `E:\Website Audit\sites\screenteamllc.com.json`

Trigger phrases: GSC audit, Full Website Audit via API / with Playwright, SEO/AEO/GEO/a11y/perf/visibility, submit indexing.

```powershell
node E:\Website Audit\tools\run-visibility-audit.mjs --site screenteamllc.com --pack full-api
node E:\Website Audit\GSC\tools\audit.mjs --full
node E:\Website Audit\GSC\tools\submit-indexing.mjs --failed
```

Outputs: `website-audit\<date>\`, `gsc-audit\<date>\`, latest JSON pointers in this folder.
