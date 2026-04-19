/* ===============================
   CHURNIQ MAIN SCRIPT
   Backend Connected Version
=============================== */


/* ─────────────────────────────
   NAVBAR SCROLL EFFECT
───────────────────────────── */

const navbar = document.getElementById("navbar");

window.addEventListener("scroll", () => {
  if (navbar) {
    navbar.classList.toggle("scrolled", window.scrollY > 20);
  }
});


/* ─────────────────────────────
   MOBILE MENU
───────────────────────────── */

function toggleMenu() {
  const menu = document.getElementById("mobile-menu");
  if (menu) menu.classList.toggle("open");
}


/* ─────────────────────────────
   SCROLL ANIMATION OBSERVER
───────────────────────────── */

const observer = new IntersectionObserver(entries => {

  entries.forEach(entry => {

    if (entry.isIntersecting) {
      entry.target.classList.add("visible");
      observer.unobserve(entry.target);
    }

  });

}, { threshold: 0.12 });

document.querySelectorAll(".fade-up").forEach(el =>
  observer.observe(el)
);


/* ─────────────────────────────
   DASHBOARD LIVE DATA FETCH
   GET /api/dashboard
───────────────────────────── */

async function loadDashboardStats() {

  try {

    const res = await fetch("/api/dashboard");
    const data = await res.json();

    setText("totalCustomers", data.total);
    setText("healthyCustomers", data.healthy);
    setText("warningCustomers", data.warning);
    setText("highRiskCustomers", data.high_risk);

  }

  catch (err) {

    console.error("Dashboard API error:", err);

  }

}


/* helper */

function setText(id, value) {

  const el = document.getElementById(id);

  if (el) el.textContent = value;

}


/* run automatically */

loadDashboardStats();


/* ─────────────────────────────
   PARTICLE BACKGROUND
───────────────────────────── */

const canvas = document.getElementById("particles");

if (canvas) {

  const ctx = canvas.getContext("2d");

  let particles = [];

  function resizeCanvas() {

    canvas.width = canvas.parentElement.offsetWidth;
    canvas.height = canvas.parentElement.offsetHeight;

  }

  class Particle {

    constructor() {
      this.reset();
    }

    reset() {

      this.x = Math.random() * canvas.width;
      this.y = Math.random() * canvas.height;

      this.size = Math.random() * 1.5 + 0.5;

      this.speedX = (Math.random() - 0.5) * 0.3;
      this.speedY = (Math.random() - 0.5) * 0.3;

      this.opacity = Math.random() * 0.5 + 0.1;

      this.color = Math.random() > 0.5
        ? "#38bdf8"
        : "#a78bfa";

    }

    update() {

      this.x += this.speedX;
      this.y += this.speedY;

      if (
        this.x < 0 ||
        this.x > canvas.width ||
        this.y < 0 ||
        this.y > canvas.height
      ) this.reset();

    }

    draw() {

      ctx.save();

      ctx.globalAlpha = this.opacity;

      ctx.fillStyle = this.color;

      ctx.beginPath();

      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);

      ctx.fill();

      ctx.restore();

    }

  }


  function initParticles() {

    resizeCanvas();

    particles = [];

    const count =
      Math.min(
        120,
        Math.floor(canvas.width * canvas.height / 8000)
      );

    for (let i = 0; i < count; i++)
      particles.push(new Particle());

  }


  function animateParticles() {

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    particles.forEach(p => {

      p.update();

      p.draw();

    });

    requestAnimationFrame(animateParticles);

  }

  initParticles();

  animateParticles();

  window.addEventListener("resize", initParticles);

}


/* ─────────────────────────────
   AI QUERY ASSISTANT
   POST /api/query
───────────────────────────── */

const queryButton =
  document.getElementById("queryButton");

const queryInput =
  document.getElementById("queryInput");

const queryResults =
  document.getElementById("queryResults");


async function handleQuery() {

  const q = queryInput.value.trim();

  if (!q) return;

  queryResults.innerHTML =
    "Processing AI query...";


  try {

    const res = await fetch("/api/query", {

      method: "POST",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify({ query: q })

    });

    const data = await res.json();

    queryResults.innerHTML =
      `<div>${data.answer}</div>`;

  }

  catch (err) {

    queryResults.innerHTML =
      `<div style="color:red;">Error connecting backend</div>`;

  }

}


if (queryButton)
  queryButton.addEventListener("click", handleQuery);


if (queryInput)
  queryInput.addEventListener("keydown", e => {

    if (e.key === "Enter")
      handleQuery();

  });


/* ─────────────────────────────
   WEEKLY REPORT DATA
   GET /api/report/weekly
───────────────────────────── */

async function loadWeeklyReport() {

  try {

    const res =
      await fetch("/api/report/weekly");

    const data =
      await res.json();

    console.log("Weekly report:", data);

  }

  catch (err) {

    console.error("Weekly report error:", err);

  }

}

loadWeeklyReport();