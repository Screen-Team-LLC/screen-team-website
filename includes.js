const SERVICE_PAGES = [
  "rescreens",
  "pool-enclosures",
  "pool-cage-repair",
  "screen-lanais",
  "lanai-screen-replacement",
  "screen-panel-repair",
  "window-screens",
  "garage-screens",
  "gutter-work",
  "gutters-and-screens",
  "pet-resistant-screen-mesh",
  "storm-screen-repair",
];

const AREA_PAGES = [
  "service-areas",
  "pinellas-county-screen-repair",
  "pasco-county-screen-repair",
  "hillsborough-county-screen-repair",
  "new-port-richey-screen-repair",
  "holiday-screen-repair",
  "hudson-screen-repair",
  "land-o-lakes-screen-repair",
  "wesley-chapel-screen-repair",
  "tarpon-springs-screen-repair",
  "clearwater-screen-repair",
  "st-petersburg-screen-repair",
  "largo-screen-repair",
  "palm-harbor-screen-repair",
  "safety-harbor-screen-repair",
  "dunedin-screen-repair",
  "oldsmar-screen-repair",
  "seminole-screen-repair",
  "pinellas-park-screen-repair",
  "gulfport-screen-repair",
  "belleair-screen-repair",
  "tampa-screen-repair",
  "brandon-screen-repair",
];

const NAV_ACTIVE_SELECTORS = {
  home: [".site-header .brand"],
  about: [".site-nav > a[href='about.html']", ".mobile-nav-links a[href='about.html']"],
  gallery: [".site-nav > a[href='gallery.html']", ".mobile-nav-links a[href='gallery.html']"],
  contact: [".site-nav > a[href='contact.html']", ".mobile-nav-links a[href='contact.html']"],
  pricing: [".site-nav > a[href='pricing.html']", ".mobile-nav-links a[href='pricing.html']"],
  rescreens: [
    ".nav-dropdown-menu a[href='rescreens.html']",
    ".mobile-services-sub a[href='rescreens.html']",
  ],
  "pool-enclosures": [
    ".nav-dropdown-menu a[href='pool-enclosures.html']",
    ".mobile-services-sub a[href='pool-enclosures.html']",
  ],
  "screen-lanais": [
    ".nav-dropdown-menu a[href='screen-lanais.html']",
    ".mobile-services-sub a[href='screen-lanais.html']",
  ],
  "window-screens": [
    ".nav-dropdown-menu a[href='window-screens.html']",
    ".mobile-services-sub a[href='window-screens.html']",
  ],
  "garage-screens": [
    ".nav-dropdown-menu a[href='garage-screens.html']",
    ".mobile-services-sub a[href='garage-screens.html']",
  ],
  "gutter-work": [
    ".nav-dropdown-menu a[href='gutter-work.html']",
    ".mobile-services-sub a[href='gutter-work.html']",
  ],
  "storm-screen-repair": [
    ".nav-dropdown-menu a[href='storm-screen-repair.html']",
    ".mobile-services-sub a[href='storm-screen-repair.html']",
  ],
  "pool-cage-repair": [
    ".nav-dropdown-menu a[href='pool-cage-repair.html']",
    ".mobile-services-sub a[href='pool-cage-repair.html']",
  ],
  "lanai-screen-replacement": [
    ".nav-dropdown-menu a[href='lanai-screen-replacement.html']",
    ".mobile-services-sub a[href='lanai-screen-replacement.html']",
  ],
  "screen-panel-repair": [
    ".nav-dropdown-menu a[href='screen-panel-repair.html']",
    ".mobile-services-sub a[href='screen-panel-repair.html']",
  ],
  "gutters-and-screens": [
    ".nav-dropdown-menu a[href='gutters-and-screens.html']",
    ".mobile-services-sub a[href='gutters-and-screens.html']",
  ],
  "pet-resistant-screen-mesh": [
    ".nav-dropdown-menu a[href='pet-resistant-screen-mesh.html']",
    ".mobile-services-sub a[href='pet-resistant-screen-mesh.html']",
  ],
  "service-areas": [
    ".nav-dropdown-wrap--areas .nav-dropdown-menu a[href='service-areas.html']",
    "#mobile-areas-sub a[href='service-areas.html']",
    ".footer-links a[href='service-areas.html']",
  ],
  "pinellas-county-screen-repair": [
    ".nav-dropdown-wrap--areas .nav-dropdown-menu a[href='pinellas-county-screen-repair.html']",
    "#mobile-areas-sub a[href='pinellas-county-screen-repair.html']",
  ],
  "pasco-county-screen-repair": [
    ".nav-dropdown-wrap--areas .nav-dropdown-menu a[href='pasco-county-screen-repair.html']",
    "#mobile-areas-sub a[href='pasco-county-screen-repair.html']",
  ],
  "hillsborough-county-screen-repair": [
    ".nav-dropdown-wrap--areas .nav-dropdown-menu a[href='hillsborough-county-screen-repair.html']",
    "#mobile-areas-sub a[href='hillsborough-county-screen-repair.html']",
  ],
  "clearwater-screen-repair": [
    ".nav-dropdown-wrap--areas .nav-dropdown-menu a[href='clearwater-screen-repair.html']",
    "#mobile-areas-sub a[href='clearwater-screen-repair.html']",
  ],
  "st-petersburg-screen-repair": [
    ".nav-dropdown-wrap--areas .nav-dropdown-menu a[href='st-petersburg-screen-repair.html']",
    "#mobile-areas-sub a[href='st-petersburg-screen-repair.html']",
  ],
  "palm-harbor-screen-repair": [
    ".nav-dropdown-wrap--areas .nav-dropdown-menu a[href='palm-harbor-screen-repair.html']",
    "#mobile-areas-sub a[href='palm-harbor-screen-repair.html']",
  ],
  "seminole-screen-repair": [
    ".nav-dropdown-wrap--areas .nav-dropdown-menu a[href='seminole-screen-repair.html']",
    "#mobile-areas-sub a[href='seminole-screen-repair.html']",
  ],
  "pinellas-park-screen-repair": [
    ".nav-dropdown-wrap--areas .nav-dropdown-menu a[href='pinellas-park-screen-repair.html']",
    "#mobile-areas-sub a[href='pinellas-park-screen-repair.html']",
  ],
  "gulfport-screen-repair": [
    ".footer-quicklinks-grid a[href='gulfport-screen-repair.html']",
  ],
  "brandon-screen-repair": [
    ".nav-dropdown-wrap--areas .nav-dropdown-menu a[href='brandon-screen-repair.html']",
    "#mobile-areas-sub a[href='brandon-screen-repair.html']",
  ],
  "wesley-chapel-screen-repair": [
    ".nav-dropdown-wrap--areas .nav-dropdown-menu a[href='wesley-chapel-screen-repair.html']",
    "#mobile-areas-sub a[href='wesley-chapel-screen-repair.html']",
  ],
  "holiday-screen-repair": [
    ".nav-dropdown-wrap--areas .nav-dropdown-menu a[href='holiday-screen-repair.html']",
    "#mobile-areas-sub a[href='holiday-screen-repair.html']",
  ],
  "hudson-screen-repair": [
    ".footer-quicklinks-grid a[href='hudson-screen-repair.html']",
  ],
  "land-o-lakes-screen-repair": [
    ".footer-quicklinks-grid a[href='land-o-lakes-screen-repair.html']",
  ],
  "belleair-screen-repair": [
    ".footer-quicklinks-grid a[href='belleair-screen-repair.html']",
  ],
  "tampa-screen-repair": [
    ".nav-dropdown-wrap--areas .nav-dropdown-menu a[href='tampa-screen-repair.html']",
    "#mobile-areas-sub a[href='tampa-screen-repair.html']",
  ],
  "largo-screen-repair": [
    ".nav-dropdown-wrap--areas .nav-dropdown-menu a[href='largo-screen-repair.html']",
    "#mobile-areas-sub a[href='largo-screen-repair.html']",
  ],
  "new-port-richey-screen-repair": [
    ".nav-dropdown-wrap--areas .nav-dropdown-menu a[href='new-port-richey-screen-repair.html']",
    "#mobile-areas-sub a[href='new-port-richey-screen-repair.html']",
  ],
  "tarpon-springs-screen-repair": [
    ".nav-dropdown-wrap--areas .nav-dropdown-menu a[href='tarpon-springs-screen-repair.html']",
    "#mobile-areas-sub a[href='tarpon-springs-screen-repair.html']",
  ],
  "dunedin-screen-repair": [
    ".nav-dropdown-wrap--areas .nav-dropdown-menu a[href='dunedin-screen-repair.html']",
    "#mobile-areas-sub a[href='dunedin-screen-repair.html']",
  ],
  "oldsmar-screen-repair": [
    ".nav-dropdown-wrap--areas .nav-dropdown-menu a[href='oldsmar-screen-repair.html']",
    "#mobile-areas-sub a[href='oldsmar-screen-repair.html']",
  ],
  "safety-harbor-screen-repair": [
    ".nav-dropdown-wrap--areas .nav-dropdown-menu a[href='safety-harbor-screen-repair.html']",
    "#mobile-areas-sub a[href='safety-harbor-screen-repair.html']",
  ],
  "service-guarantee": [".footer-links a[href='service-guarantee.html']"],
  "privacy-policy": [".footer-links a[href='privacy-policy.html']"],
  "thank-you": [],
  "404": [],
};

const HEADER_BLOCK_RE =
  /<header class="site-header"[\s\S]*?<\/header>\s*<div class="nav-overlay"[\s\S]*?<\/div>\s*<nav class="mobile-nav"[\s\S]*?<\/nav>/;

const FOOTER_BLOCK_RE = /<footer class="site-footer">[\s\S]*?<\/footer>/;

function getIncludeBase() {
  const script = document.querySelector('script[src*="includes.js"]');
  if (!script || !script.src) return "";
  return script.src.replace(/includes\.js(?:\?.*)?$/, "");
}

function getCurrentNavPage() {
  const path = window.location.pathname;
  const file = path.split("/").pop() || "index.html";
  if (!file || file === "index.html") return "home";
  return file.replace(/\.html$/, "");
}

function isHomePage() {
  return (
    document.body.classList.contains("home-landing") ||
    window.location.pathname === "/" ||
    window.location.pathname.endsWith("/index.html")
  );
}

function applyHeaderAdjustments() {
  const brand = document.querySelector(".site-header .brand");
  if (brand) {
    brand.setAttribute("href", isHomePage() ? "#top" : "/");
  }

  document.querySelectorAll('[aria-current="page"]').forEach((el) => {
    el.removeAttribute("aria-current");
  });

  const page = getCurrentNavPage();
  (NAV_ACTIVE_SELECTORS[page] || []).forEach((selector) => {
    document.querySelectorAll(selector).forEach((link) => {
      link.setAttribute("aria-current", "page");
    });
  });

  if (SERVICE_PAGES.includes(page)) {
    const servicesBtn = document.querySelector(
      ".nav-dropdown-wrap:not(.nav-dropdown-wrap--areas) .nav-dropdown-btn",
    );
    if (servicesBtn) servicesBtn.setAttribute("aria-current", "page");
  }

  if (AREA_PAGES.includes(page)) {
    const areasBtn = document.querySelector(".nav-dropdown-wrap--areas .nav-dropdown-btn");
    if (areasBtn) areasBtn.setAttribute("aria-current", "page");
  }
}

async function fetchInclude(path) {
  const response = await fetch(path, { cache: "no-cache" });
  if (!response.ok) {
    throw new Error(`Failed to load ${path} (${response.status})`);
  }
  return response.text();
}

function injectInclude(slot, html) {
  if (!slot || !html) return;
  slot.insertAdjacentHTML("afterend", html.trim());
  slot.remove();
}

async function loadSiteIncludes() {
  const base = getIncludeBase();
  const headerSlot = document.getElementById("site-header-include");
  const footerSlot = document.getElementById("site-footer-include");
  const tasks = [];

  if (headerSlot) {
    tasks.push(
      fetchInclude(`${base}header.html`).then((html) => injectInclude(headerSlot, html)),
    );
  }

  if (footerSlot) {
    tasks.push(
      fetchInclude(`${base}footer.html`).then((html) => injectInclude(footerSlot, html)),
    );
  }

  await Promise.all(tasks);

  if (!document.querySelector(".site-header")) {
    console.warn("Site header was not injected. Check header.html and includes.js.");
    return;
  }

  applyHeaderAdjustments();
  document.dispatchEvent(new CustomEvent("site:includes-loaded"));
}

function initSiteIncludes() {
  loadSiteIncludes().catch((error) => {
    console.error("Site includes failed to load:", error);
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initSiteIncludes);
} else {
  initSiteIncludes();
}
