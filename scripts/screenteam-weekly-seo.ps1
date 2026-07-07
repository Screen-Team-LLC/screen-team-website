# Weekly Screen Team SEO: Serper meta refresh (reuse last SERP research if present).
$ErrorActionPreference = "Stop"

$siteRoot = Split-Path -Parent $PSScriptRoot
$date = Get-Date -Format "yyyy-MM-dd"
$auditDir = Join-Path $siteRoot "seo-audit\$date"
New-Item -ItemType Directory -Force -Path $auditDir | Out-Null

Write-Host "Screen Team weekly SEO"
Write-Host "  Site root: $siteRoot"
Write-Host "  Audit dir: $auditDir"

Push-Location $siteRoot
try {
    $serpJson = Join-Path $siteRoot "seo\serp-meta-research.json"
    if (Test-Path $serpJson) {
        Write-Host "Reusing existing Serper research (--skip-research)"
        python scripts/run-serp-workflow.py --skip-research
    } else {
        Write-Host "No prior Serper research — running full workflow"
        python scripts/run-serp-workflow.py
    }
    if ($LASTEXITCODE -ne 0) { throw "run-serp-workflow.py failed" }

    Copy-Item -Force $serpJson (Join-Path $auditDir "serp-meta-research.json") -ErrorAction SilentlyContinue
    Copy-Item -Force (Join-Path $siteRoot "seo\meta-descriptions.json") (Join-Path $auditDir "meta-descriptions.json") -ErrorAction SilentlyContinue
}
finally {
    Pop-Location
}

Write-Host "Done. Review seo/serp-meta-research.md and seo-audit\$date"
