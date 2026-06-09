const NAV_ACTIVE_SELECTORS = {
  home: ['.site-nav a[href="/"]', '.mobile-nav-links > a[href="/"]'],
  about: ['.site-nav a[href="about.html"]', '.mobile-nav-links a[href="about.html"]'],
  gallery: ['.site-nav a[href="gallery.html"]', '.mobile-nav-links a[href="gallery.html"]'],
  contact: ['.site-nav a[href="contact.html"]', '.mobile-nav-links a[href="contact.html"]'],
  rescreens: ['.nav-dropdown-menu a[href="rescreens.html"]', '.mobile-services-sub a[href="rescreens.html"]'],
  "pool-enclosures": ['.nav-dropdown-menu a[href="pool-enclosures.html"]', '.mobile-services-sub a[href="pool-enclosures.html"]'],
  "screen-lanais": ['.nav-dropdown-menu a[href="screen-lanais.html"]', '.mobile-services-sub a[href="screen-lanais.html"]'],
  "window-screens": ['.nav-dropdown-menu a[href="window-screens.html"]', '.mobile-services-sub a[href="window-screens.html"]'],
  "garage-screens": ['.nav-dropdown-menu a[href="garage-screens.html"]', '.mobile-services-sub a[href="garage-screens.html"]'],
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

async function loadSiteIncludes() {
  const headerMount = document.getElementById("site-header-mount");
  const footerMount = document.getElementById("site-footer-mount");
  if (!headerMount && !footerMount) return;

  try {
    const requests = [];

    if (headerMount) {
      requests.push(
        fetch("header.html").then((response) => {
          if (!response.ok) throw new Error("header.html");
          return response.text();
        }),
      );
    } else {
      requests.push(Promise.resolve(null));
    }

    if (footerMount) {
      requests.push(
        fetch("footer.html").then((response) => {
          if (!response.ok) throw new Error("footer.html");
          return response.text();
        }),
      );
    } else {
      requests.push(Promise.resolve(null));
    }

    const [headerHtml, footerHtml] = await Promise.all(requests);

    if (headerHtml && headerMount) {
      headerMount.insertAdjacentHTML("afterend", headerHtml);
      headerMount.remove();
      applyHeaderAdjustments();
    }

    if (footerHtml && footerMount) {
      footerMount.insertAdjacentHTML("afterend", footerHtml);
      footerMount.remove();
    }

    document.dispatchEvent(new CustomEvent("site:includes-loaded"));
  } catch (error) {
    console.error("Failed to load site header/footer includes:", error);
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", loadSiteIncludes);
} else {
  loadSiteIncludes();
}
