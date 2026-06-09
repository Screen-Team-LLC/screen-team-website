const NAV_ACTIVE_SELECTORS = {
  home: ['.site-nav a[href="/"]', '.mobile-nav-links > a[href="/"]'],
  about: ['.site-nav a[href="about.html"]', '.mobile-nav-links a[href="about.html"]'],
  gallery: ['.site-nav a[href="gallery.html"]', '.mobile-nav-links a[href="gallery.html"]'],
  contact: ['.site-nav a[href="contact.html"]', '.mobile-nav-links a[href="contact.html"]'],
  rescreens: ['.nav-dropdown-menu a[href="rescreens.html"]', '.mobile-services-sub a[href="rescreens.html"]'],
  "pool-enclosures": ['.nav-dropdown-menu a[href="pool-enclosures.html"]', '.mobile-services-sub a[href="pool-enclosures.html"]'],
  "screen-lanais": ['.nav-dropdown-menu a[href="screen-lanais.html"]', '.mobile-services-sub a[href="screen-lanais.html"]'],
  "window-screens": ['.nav-dropdown-menu a[href="window-screens.html"]', '.mobile-services-sub a[href="window-screens.html"]'],
  "garage-screens": ['.nav-dropdown-menu a[href="garage-screens.html"]', ".mobile-services-sub a[href=\"garage-screens.html\"]"],
  "gutter-work": ['.nav-dropdown-menu a[href="gutter-work.html"]', '.mobile-services-sub a[href="gutter-work.html"]'],
  "service-areas": ['.footer-links a[href="service-areas.html"]'],
  "service-guarantee": ['.footer-links a[href="service-guarantee.html"]'],
  "privacy-policy": ['.footer-links a[href="privacy-policy.html"]'],
};

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

  document.querySelectorAll('[aria-current="page"]').forEach((link) => {
    link.removeAttribute("aria-current");
  });

  const page = getCurrentNavPage();
  (NAV_ACTIVE_SELECTORS[page] || []).forEach((selector) => {
    document.querySelectorAll(selector).forEach((link) => {
      link.setAttribute("aria-current", "page");
    });
  });
}

function initSiteIncludes() {
  if (!document.querySelector(".site-header")) return;

  applyHeaderAdjustments();
  document.dispatchEvent(new CustomEvent("site:includes-loaded"));
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initSiteIncludes);
} else {
  initSiteIncludes();
}
