const currentYear = document.querySelector("#current-year");

if (currentYear) {
  currentYear.textContent = new Date().getFullYear();
}

const revealItems = document.querySelectorAll("[data-reveal]");

if ("IntersectionObserver" in window && revealItems.length > 0) {
  const observer = new IntersectionObserver(
    (entries, activeObserver) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }

        entry.target.classList.add("is-visible");
        activeObserver.unobserve(entry.target);
      });
    },
    {
      threshold: 0.18,
      rootMargin: "0px 0px -40px 0px",
    },
  );

  revealItems.forEach((item) => observer.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add("is-visible"));
}

// ---- Formspree AJAX submission ----
const heroForm    = document.getElementById("hero-contact-form");
const formSuccess = document.getElementById("form-success");

if (heroForm && formSuccess) {
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
        heroForm.hidden = true;
        formSuccess.hidden = false;
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

// ---- Services nav dropdown ----
const dropdownBtn  = document.querySelector('.nav-dropdown-btn');
const dropdownMenu = document.querySelector('.nav-dropdown-menu');

if (dropdownBtn && dropdownMenu) {
  dropdownBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    const expanded = dropdownBtn.getAttribute('aria-expanded') === 'true';
    dropdownBtn.setAttribute('aria-expanded', String(!expanded));
  });

  dropdownMenu.addEventListener('click', (e) => e.stopPropagation());

  document.addEventListener('click', () => {
    dropdownBtn.setAttribute('aria-expanded', 'false');
  });
}

// ---- FAQ accordion ----
document.querySelectorAll('.faq-question').forEach((btn) => {
  btn.addEventListener('click', () => {
    const expanded = btn.getAttribute('aria-expanded') === 'true';
    const answer   = document.getElementById(btn.getAttribute('aria-controls'));

    // Close all others
    document.querySelectorAll('.faq-question').forEach((otherBtn) => {
      const otherAnswer = document.getElementById(otherBtn.getAttribute('aria-controls'));
      otherBtn.setAttribute('aria-expanded', 'false');
      if (otherAnswer) otherAnswer.setAttribute('aria-hidden', 'true');
    });

    // Toggle clicked
    btn.setAttribute('aria-expanded', String(!expanded));
    if (answer) answer.setAttribute('aria-hidden', String(expanded));
  });
});