function initCurrentYear() {
  document.querySelectorAll("#current-year").forEach((el) => {
    el.textContent = new Date().getFullYear();
  });
}

function initHeaderScroll() {
  const header = document.querySelector(".site-header");
  if (!header) return;

  window.addEventListener(
    "scroll",
    () => header.classList.toggle("scrolled", window.scrollY > 40),
    { passive: true },
  );
}

function initScrollReveal() {
  const revealEls = document.querySelectorAll(
    ".reveal, .reveal-left, .reveal-right, .reveal-scale, .reveal-photo, [data-reveal]",
  );
  if (!revealEls.length) return;

  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries, activeObserver) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;

          entry.target.classList.add("visible", "is-visible");
          activeObserver.unobserve(entry.target);
        });
      },
      {
        threshold: 0.12,
        rootMargin: "0px 0px -40px 0px",
      },
    );

    revealEls.forEach((item) => observer.observe(item));
  } else {
    revealEls.forEach((item) => item.classList.add("visible", "is-visible"));
  }
}

function initHeroPanels() {
  document.querySelectorAll(".hero-panels").forEach((panels) => {
    const hero = panels.closest(".hero");
    if (!hero || hero.dataset.panelsInit) return;
    hero.dataset.panelsInit = "1";
    requestAnimationFrame(() => hero.classList.add("hero-panels-ready"));
  });
}

function initSiteNav() {
  const dropdownBtn = document.querySelector(".nav-dropdown-btn");
  const dropdownMenu = document.querySelector(".nav-dropdown-menu");

  if (dropdownBtn && dropdownMenu) {
    dropdownBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      const expanded = dropdownBtn.getAttribute("aria-expanded") === "true";
      dropdownBtn.setAttribute("aria-expanded", String(!expanded));
    });

    dropdownMenu.addEventListener("click", (e) => e.stopPropagation());

    document.addEventListener("click", () => {
      dropdownBtn.setAttribute("aria-expanded", "false");
    });
  }

  const hamburgerBtn = document.getElementById("hamburger-btn");
  const mobileNav = document.getElementById("mobile-nav");
  const navOverlay = document.getElementById("nav-overlay");
  const mobileNavClose = document.getElementById("mobile-nav-close");
  const mobileServToggle = document.getElementById("mobile-services-toggle");
  const mobileServicesSub = document.getElementById("mobile-services-sub");

  function openMobileNav() {
    if (!mobileNav || !navOverlay || !hamburgerBtn) return;
    mobileNav.classList.add("is-open");
    navOverlay.classList.add("is-open");
    hamburgerBtn.classList.add("is-open");
    hamburgerBtn.setAttribute("aria-expanded", "true");
    mobileNav.setAttribute("aria-hidden", "false");
    mobileNav.removeAttribute("inert");
    document.body.style.overflow = "hidden";
  }

  function closeMobileNav() {
    if (!mobileNav || !navOverlay || !hamburgerBtn) return;
    mobileNav.classList.remove("is-open");
    navOverlay.classList.remove("is-open");
    hamburgerBtn.classList.remove("is-open");
    hamburgerBtn.setAttribute("aria-expanded", "false");
    mobileNav.setAttribute("aria-hidden", "true");
    mobileNav.setAttribute("inert", "");
    document.body.style.overflow = "";
  }

  if (hamburgerBtn) {
    hamburgerBtn.addEventListener("click", () => {
      hamburgerBtn.classList.contains("is-open") ? closeMobileNav() : openMobileNav();
    });
  }
  if (mobileNavClose) mobileNavClose.addEventListener("click", closeMobileNav);
  if (navOverlay) navOverlay.addEventListener("click", closeMobileNav);

  if (mobileNav) {
    mobileNav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", closeMobileNav);
    });
  }

  if (mobileServToggle && mobileServicesSub) {
    mobileServToggle.addEventListener("click", () => {
      const open = mobileServToggle.classList.toggle("is-open");
      mobileServicesSub.classList.toggle("is-open", open);
      mobileServToggle.setAttribute("aria-expanded", String(open));
    });
  }
}

function initSiteChrome() {
  initCurrentYear();
  initHeaderScroll();
  initSiteNav();
}

function initFormHandlers() {
  const heroForm = document.getElementById("hero-contact-form");
  const formSuccess = document.getElementById("form-success");

  if (!heroForm || !formSuccess) return;

  heroForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    const submitBtn = heroForm.querySelector("[type='submit']");
    const originalText = submitBtn.textContent;

    submitBtn.disabled = true;
    submitBtn.textContent = "Sending...";

    try {
      const res = await fetch(heroForm.action, {
        method: "POST",
        body: new FormData(heroForm),
        headers: { Accept: "application/json" },
      });

      if (res.ok) {
        submitBtn.textContent = "Sent! ✓";
        setTimeout(() => {
          heroForm.hidden = true;
          formSuccess.hidden = false;
          submitBtn.disabled = false;
          submitBtn.textContent = originalText;
        }, 1800);
      } else {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
        alert("Something went wrong. Please call (727) 386-6562 directly.");
      }
    } catch {
      submitBtn.disabled = false;
      submitBtn.textContent = originalText;
      alert("Could not send. Please call (727) 386-6562 directly.");
    }
  });
}

function initGalleryFilters() {
  const galleryFilters = document.querySelectorAll(".gallery-filter");
  const galleryItems = document.querySelectorAll(".gallery-item[data-category]");

  if (!galleryFilters.length || !galleryItems.length) return;

  const validFilters = new Set(Array.from(galleryFilters, (button) => button.dataset.filter));

  function applyGalleryFilter(filter, updateUrl) {
    const activeFilter = validFilters.has(filter) ? filter : "all";

    galleryFilters.forEach((button) => {
      const isActive = button.dataset.filter === activeFilter;
      button.classList.toggle("active", isActive);
      button.setAttribute("aria-selected", String(isActive));
    });

    galleryItems.forEach((item) => {
      const isVisible = activeFilter === "all" || item.dataset.category === activeFilter;
      item.hidden = !isVisible;
    });

    if (!updateUrl) return;

    const currentUrl = new URL(window.location.href);
    if (activeFilter === "all") {
      currentUrl.searchParams.delete("filter");
    } else {
      currentUrl.searchParams.set("filter", activeFilter);
    }

    window.history.replaceState({}, "", currentUrl);
  }

  const initialFilter = new URLSearchParams(window.location.search).get("filter") || "all";
  applyGalleryFilter(initialFilter, false);

  galleryFilters.forEach((button) => {
    button.addEventListener("click", () => {
      applyGalleryFilter(button.dataset.filter, true);
    });
  });
}

function initFaqAccordion() {
  document.querySelectorAll(".faq-question").forEach((btn) => {
    btn.addEventListener("click", () => {
      const expanded = btn.getAttribute("aria-expanded") === "true";
      const answer = document.getElementById(btn.getAttribute("aria-controls"));

      document.querySelectorAll(".faq-question").forEach((otherBtn) => {
        const otherAnswer = document.getElementById(otherBtn.getAttribute("aria-controls"));
        otherBtn.setAttribute("aria-expanded", "false");
        if (otherAnswer) {
          otherAnswer.setAttribute("aria-hidden", "true");
          otherAnswer.setAttribute("inert", "");
        }
      });

      btn.setAttribute("aria-expanded", String(!expanded));
      if (answer) {
        answer.setAttribute("aria-hidden", String(expanded));
        if (expanded) {
          answer.setAttribute("inert", "");
        } else {
          answer.removeAttribute("inert");
        }
      }
    });
  });
}

function initPage() {
  initScrollReveal();
  initHeroPanels();
  initFormHandlers();
  initGalleryFilters();
  initFaqAccordion();

  if (document.querySelector(".site-header")) {
    initSiteChrome();
  }
}

document.addEventListener("site:includes-loaded", initSiteChrome, { once: true });

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initPage);
} else {
  initPage();
}
