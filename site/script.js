// MSH Photovoltaik – interactions
(() => {
  const header = document.getElementById("header");
  const nav = document.getElementById("nav");
  const burger = document.getElementById("burger");

  // Header shadow on scroll
  const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 10);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  // Mobile navigation
  const setNav = (open) => {
    nav.classList.toggle("is-open", open);
    burger.setAttribute("aria-expanded", String(open));
    burger.setAttribute("aria-label", open ? "Menü schließen" : "Menü öffnen");
    document.body.classList.toggle("nav-open", open);
  };
  burger.addEventListener("click", () => setNav(!nav.classList.contains("is-open")));
  nav.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => setNav(false)));

  // Active nav link by section in view
  const links = [...document.querySelectorAll(".nav__link")];
  const sections = links
    .map((l) => document.querySelector(l.getAttribute("href")))
    .filter(Boolean);
  const spy = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        const id = "#" + e.target.id;
        links.forEach((l) => l.classList.toggle("is-active", l.getAttribute("href") === id));
      });
    },
    { rootMargin: "-45% 0px -50% 0px" }
  );
  sections.forEach((s) => spy.observe(s));

  // Reveal on scroll (staggered within a group)
  const revealEls = document.querySelectorAll(".reveal");
  const revealer = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        const siblings = [...e.target.parentElement.children].filter((c) => c.classList.contains("reveal"));
        const i = Math.max(0, siblings.indexOf(e.target));
        e.target.style.transitionDelay = `${Math.min(i, 5) * 80}ms`;
        e.target.classList.add("is-visible");
        revealer.unobserve(e.target);
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
  );
  revealEls.forEach((el) => revealer.observe(el));

  // Stats: count up once when they scroll into view
  const counters = document.querySelectorAll("[data-count]");
  const countUp = (el) => {
    const target = Number(el.dataset.count);
    const start = performance.now();
    const dur = 1400;
    const tick = (now) => {
      const p = Math.min((now - start) / dur, 1);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const counterObs = new IntersectionObserver(
      (entries) => entries.forEach((e) => {
        if (!e.isIntersecting) return;
        countUp(e.target);
        counterObs.unobserve(e.target);
      }),
      { threshold: 0.6 }
    );
    counters.forEach((el) => { el.textContent = "0"; counterObs.observe(el); });
  }

  // Hero video: loops (empty roof -> finished PV array)
  const heroVideo = document.getElementById("heroVideo");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduceMotion) {
    heroVideo.removeAttribute("autoplay");
    heroVideo.pause();
  } else {
    const playHero = () => { if (heroVideo.paused) heroVideo.play().catch(() => {}); };
    playHero();
    heroVideo.addEventListener("canplay", playHero);
    document.addEventListener("visibilitychange", () => { if (!document.hidden) playHero(); });
  }

  // Close mobile nav with Escape
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && nav.classList.contains("is-open")) setNav(false);
  });

  // FAQ: only one open at a time
  const faqItems = document.querySelectorAll(".faq__item");
  faqItems.forEach((item) =>
    item.addEventListener("toggle", () => {
      if (item.open) faqItems.forEach((o) => o !== item && (o.open = false));
    })
  );

  // Quick request form (client-side only – no backend connected yet)
  const form = document.getElementById("quickForm");
  const msg = document.getElementById("formMsg");
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const fields = [...form.querySelectorAll("input[required]")];
    let valid = true;
    fields.forEach((f) => {
      let ok = f.value.trim().length > 1;
      if (f.type === "tel") ok = /^[+\d][\d\s/()-]{5,}$/.test(f.value.trim());
      f.classList.toggle("is-invalid", !ok);
      f.setAttribute("aria-invalid", String(!ok));
      if (!ok) valid = false;
    });
    msg.className = "quick-form__msg";
    if (!valid) {
      msg.textContent = "Bitte füllen Sie alle Felder korrekt aus.";
      msg.classList.add("is-error");
      form.querySelector(".is-invalid")?.focus();
      return;
    }
    msg.textContent = "Vielen Dank! Wir melden uns zeitnah bei Ihnen.";
    msg.classList.add("is-success");
    form.reset();
  });
  form.querySelectorAll("input").forEach((f) =>
    f.addEventListener("input", () => f.classList.remove("is-invalid"))
  );
})();
