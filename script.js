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
    ".reveal, .reveal-left, .reveal-right, .reveal-scale, .reveal-photo, .slide-enter, [data-reveal], .eyebrow:not(.hero-enter), .card-eyebrow:not(.hero-enter)",
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

function initHomeStripEntrance() {
  if (!document.body.classList.contains("home-landing")) return;

  const items = document.querySelectorAll(
    ".trust-strip .strip-slide, .st-intent-strip .strip-slide",
  );
  if (!items.length) return;

  const reveal = () => {
    items.forEach((item) => item.classList.add("is-visible"));
  };

  if (prefersReducedMotion()) {
    reveal();
    return;
  }

  const start = () => setTimeout(reveal, 1850);
  const hero = document.querySelector(".hero");

  if (hero?.classList.contains("hero-panels-ready")) {
    start();
    return;
  }

  if (!hero) {
    start();
    return;
  }

  const observer = new MutationObserver(() => {
    if (!hero.classList.contains("hero-panels-ready")) return;
    observer.disconnect();
    start();
  });

  observer.observe(hero, { attributes: true, attributeFilter: ["class"] });
}

function prefersReducedMotion() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

function initHeroParallax() {
  if (prefersReducedMotion()) return;

  const hero = document.querySelector("body.home-landing .hero");
  if (!hero) return;

  const layers = hero.querySelectorAll(".hero-panels, .hero-cutout-wrap, .hero-overlay");
  if (!layers.length) return;

  let ticking = false;

  function update() {
    ticking = false;

    const heroTop = hero.offsetTop;
    const heroHeight = hero.offsetHeight;
    const offset = Math.max(0, window.scrollY - heroTop);
    const shift = Math.min(offset * 0.4, heroHeight);

    layers.forEach((layer) => {
      layer.style.setProperty("--st-hero-shift", `${Math.round(shift)}px`);
    });
  }

  function queue() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(update);
  }

  update();
  window.addEventListener("scroll", queue, { passive: true });
  window.addEventListener("resize", queue, { passive: true });
}

function initParallaxBands() {
  if (prefersReducedMotion()) return;

  const backgrounds = document.querySelectorAll(".st-parallax-bg");
  const contactBands = document.querySelectorAll(".contact-section--parallax");
  if (!backgrounds.length && !contactBands.length) return;

  let ticking = false;

  function getOverscanPx(band) {
    if (band.dataset.parallaxOverscan) {
      return band.offsetHeight * Number(band.dataset.parallaxOverscan);
    }
    if (band.classList.contains("st-process-band")) {
      return band.offsetHeight * 0.08;
    }
    if (band.classList.contains("st-route-band--parallax")) {
      return band.offsetHeight * 0.28;
    }
    return band.offsetHeight * 0.3;
  }

  function clampShift(shift, maxShift) {
    return Math.round(Math.max(-maxShift, Math.min(maxShift, shift)));
  }

  /** Scroll progress 0→1 as the band travels through the viewport */
  function bandScrollProgress(band, vh) {
    const rect = band.getBoundingClientRect();
    const range = vh + band.offsetHeight;
    const scrolled = Math.max(0, Math.min(range, vh - rect.top));
    return scrolled / range;
  }

  function applySymmetricParallax(target, band, { intensity = 0.6, baseOffset = 0 } = {}) {
    const vh = Math.max(window.innerHeight, 1);
    const rect = band.getBoundingClientRect();
    if (rect.bottom < 0 || rect.top > vh) return;

    const maxShift = getOverscanPx(band);
    const t = bandScrollProgress(band, vh);
    const shift = clampShift((t - 0.5) * 2 * maxShift * intensity + baseOffset, maxShift);

    target.style.setProperty("--st-band-shift", `${shift}px`);
  }

  function applyParallax(target, band) {
    const vh = Math.max(window.innerHeight, 1);
    const rect = band.getBoundingClientRect();
    if (rect.bottom < 0 || rect.top > vh) return;

    if (
      band.classList.contains("work-teaser--parallax") ||
      band.classList.contains("contact-section--parallax")
    ) {
      applySymmetricParallax(target, band, { intensity: 0.55 });
      return;
    }

    const maxShift = getOverscanPx(band);
    let shift;

    if (band.classList.contains("st-process-band")) {
      shift = (rect.top - vh) * 0.35 + 56;
    } else if (band.classList.contains("st-route-band--parallax")) {
      shift = (rect.top - vh) * 0.28;
    } else {
      shift = (rect.top - vh) * 0.45;
    }

    target.style.setProperty("--st-band-shift", `${clampShift(shift, maxShift)}px`);
  }

  function update() {
    ticking = false;

    backgrounds.forEach((bg) => {
      const band = bg.closest(
        ".work-teaser--parallax, .st-process-band, .st-route-band--parallax",
      );
      if (!band) return;
      applyParallax(bg, band);
    });

    contactBands.forEach((band) => {
      applyParallax(band, band);
    });
  }

  function queue() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(update);
  }

  update();
  window.addEventListener("scroll", queue, { passive: true });
  window.addEventListener("resize", queue, { passive: true });
}

function initSiteNav() {
  function closeAllDropdowns() {
    document.querySelectorAll(".nav-dropdown-btn").forEach((btn) => {
      btn.setAttribute("aria-expanded", "false");
    });
  }

  document.querySelectorAll(".nav-dropdown-wrap").forEach((wrap) => {
    const dropdownBtn = wrap.querySelector(".nav-dropdown-btn");
    const dropdownMenu = wrap.querySelector(".nav-dropdown-menu");
    if (!dropdownBtn || !dropdownMenu) return;

    dropdownBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      const expanded = dropdownBtn.getAttribute("aria-expanded") === "true";
      closeAllDropdowns();
      dropdownBtn.setAttribute("aria-expanded", String(!expanded));
    });

    dropdownMenu.addEventListener("click", (e) => e.stopPropagation());
  });

  document.addEventListener("click", closeAllDropdowns);

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

  const mobileAreasToggle = document.getElementById("mobile-areas-toggle");
  const mobileAreasSub = document.getElementById("mobile-areas-sub");
  if (mobileAreasToggle && mobileAreasSub) {
    mobileAreasToggle.addEventListener("click", () => {
      const open = mobileAreasToggle.classList.toggle("is-open");
      mobileAreasSub.classList.toggle("is-open", open);
      mobileAreasToggle.setAttribute("aria-expanded", String(open));
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

function initStGoogleReviews() {
  const carousels = document.querySelectorAll("[data-st-review-carousel]");
  if (!carousels.length) return;

  carousels.forEach((carousel) => {
    const track = carousel.querySelector(".st-review-carousel-track");
    const prevBtn = carousel.querySelector(".st-review-carousel-btn.prev");
    const nextBtn = carousel.querySelector(".st-review-carousel-btn.next");
    const showcase = carousel.closest(".st-google-reviews-showcase");
    const dotsContainer = showcase
      ? showcase.querySelector(".st-review-carousel-dots")
      : null;
    const summaryEl = document.getElementById("st-review-summary");
    const mapRatingEl = document.getElementById("st-map-rating");
    const seedEl = showcase ? showcase.querySelector("#google-reviews-seed") : null;

    if (!track || !prevBtn || !nextBtn || !dotsContainer || !showcase) return;

    let cards = [];
    let currentIndex = 0;
    let reviews = [];

    function escapeHtml(value) {
      return String(value || "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
    }

    function getInitial(name) {
      const clean = String(name || "").trim();
      return clean ? clean.charAt(0).toUpperCase() : "?";
    }

    function formatStars(count) {
      const stars = Math.max(1, Math.min(5, Number(count) || 5));
      return "\u2605".repeat(stars);
    }

    function reviewCardMarkup(review) {
      return (
        '<article class="st-review-card">' +
        '<div class="st-review-card-header">' +
        '<span class="st-review-avatar" style="background:' +
        escapeHtml(review.avatarColor || "#1a56c4") +
        ';" aria-hidden="true">' +
        escapeHtml(getInitial(review.name)) +
        "</span>" +
        "<div>" +
        '<div class="st-review-name">' +
        escapeHtml(review.name) +
        "</div>" +
        '<div class="st-review-meta">' +
        escapeHtml(review.meta || "") +
        "</div>" +
        "</div>" +
        "</div>" +
        '<div class="st-review-card-stars" role="img" aria-label="' +
        escapeHtml(String(Number(review.stars) || 5)) +
        ' stars">' +
        formatStars(review.stars) +
        "</div>" +
        '<p class="st-review-text">' +
        escapeHtml(review.text || "") +
        "</p>" +
        '<div class="st-review-date">' +
        escapeHtml(review.date || "") +
        "</div>" +
        "</article>"
      );
    }

    function applySummary(payload) {
      const rating = Number(payload.ratingValue || 5).toFixed(1);
      const count = Number(payload.reviewCount || reviews.length || 0);
      const label = count === 1 ? " review" : " reviews";
      const summaryText = rating + " \u00b7 " + count + label;
      if (summaryEl) summaryEl.textContent = summaryText;
      if (mapRatingEl) {
        mapRatingEl.textContent =
          formatStars(payload.ratingValue || 5) +
          " " +
          rating +
          " \u00b7 " +
          count +
          " Google review" +
          (count === 1 ? "" : "s");
        mapRatingEl.setAttribute(
          "aria-label",
          rating + " out of 5 stars, " + count + " Google reviews",
        );
      }
    }

    function visibleCount() {
      if (window.innerWidth <= 720) return 1;
      if (window.innerWidth <= 1060) return 2;
      return 3;
    }

    function pageCount() {
      return Math.max(1, Math.ceil(cards.length / visibleCount()));
    }

    function maxIndex() {
      return Math.max(0, cards.length - visibleCount());
    }

    function cardSpan() {
      if (!cards.length) return 0;
      const styles = window.getComputedStyle(track);
      const gap = parseFloat(styles.columnGap || styles.gap || "0");
      return cards[0].getBoundingClientRect().width + gap;
    }

    function updateButtons() {
      const singlePage = pageCount() <= 1 || cards.length === 0;
      prevBtn.disabled = singlePage || currentIndex <= 0;
      nextBtn.disabled = singlePage || currentIndex >= maxIndex();
    }

    function update() {
      currentIndex = Math.max(0, Math.min(currentIndex, maxIndex()));
      track.style.transform = "translateX(" + -currentIndex * cardSpan() + "px)";

      const activePage = Math.floor(currentIndex / visibleCount());
      dotsContainer.querySelectorAll(".st-review-carousel-dot").forEach((dot, index) => {
        const isActive = index === activePage;
        dot.classList.toggle("active", isActive);
        if (isActive) {
          dot.setAttribute("aria-current", "true");
        } else {
          dot.removeAttribute("aria-current");
        }
      });

      updateButtons();
    }

    function buildDots() {
      dotsContainer.innerHTML = "";
      for (let index = 0; index < pageCount(); index += 1) {
        const dot = document.createElement("button");
        dot.type = "button";
        dot.className = "st-review-carousel-dot" + (index === 0 ? " active" : "");
        dot.setAttribute("aria-label", "Go to review page " + (index + 1));
        if (index === 0) dot.setAttribute("aria-current", "true");
        dot.addEventListener("click", () => {
          currentIndex = index * visibleCount();
          update();
        });
        dotsContainer.appendChild(dot);
      }
    }

    function renderReviews(payload) {
      reviews = Array.isArray(payload.reviews) ? payload.reviews.slice() : [];
      applySummary(payload);

      if (!reviews.length) {
        track.innerHTML =
          '<article class="st-review-card"><p class="st-review-text">Reviews will appear here once posted on Google.</p></article>';
      } else {
        track.innerHTML = reviews.map(reviewCardMarkup).join("");
      }

      cards = Array.from(track.querySelectorAll(".st-review-card"));
      currentIndex = 0;
      carousel.classList.toggle("single-review", cards.length <= 1);
      buildDots();
      update();
    }

    function parseSeedPayload() {
      if (!seedEl) return null;
      try {
        return JSON.parse(seedEl.textContent || "{}");
      } catch (error) {
        console.warn("Google review seed parse failed:", error);
        return null;
      }
    }

    async function loadReviews() {
      let payload = null;
      try {
        const response = await fetch("./data/google-reviews.json", { cache: "no-store" });
        if (response.ok) {
          payload = await response.json();
        }
      } catch (error) {
        console.warn("Google review feed fetch failed, using seed data:", error);
      }

      if (!payload) payload = parseSeedPayload();
      if (!payload || !Array.isArray(payload.reviews)) {
        payload = { ratingValue: 5, reviewCount: 0, reviews: [] };
      }

      renderReviews(payload);
    }

    prevBtn.addEventListener("click", () => {
      currentIndex -= 1;
      update();
    });
    nextBtn.addEventListener("click", () => {
      currentIndex += 1;
      update();
    });
    window.addEventListener("resize", () => {
      buildDots();
      update();
    });

    loadReviews();
  });
}

function initPage() {
  initScrollReveal();
  initHeroPanels();
  initHomeStripEntrance();
  initHeroParallax();
  initParallaxBands();
  initStGoogleReviews();
  initFormHandlers();
  initGalleryFilters();
  initFaqAccordion();

  if (
    document.querySelector(".site-header") &&
    !document.getElementById("site-header-include")
  ) {
    initSiteChrome();
  }
}

document.addEventListener("site:includes-loaded", initSiteChrome, { once: true });

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initPage);
} else {
  initPage();
}
