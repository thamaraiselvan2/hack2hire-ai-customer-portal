/* ===============================
   MAIN SCRIPT (BACKEND CONNECTED)
=============================== */

console.log("script.js loaded successfully");

/* ===============================
   RUN AFTER PAGE LOADS
=============================== */

document.addEventListener("DOMContentLoaded", () => {

  loadDashboardStats();
  loadCustomers();

  // Only run if APIs exist
  safeRun(loadHealthScores);
  safeRun(loadChurnAlerts);
  safeRun(loadWeeklyReport);

});


/* ===============================
   SAFE FUNCTION RUNNER
=============================== */

function safeRun(fn) {
  try {
    fn();
  } catch (err) {
    console.warn("Optional module skipped:", err);
  }
}


/* ===============================
   NAVBAR SCROLL EFFECT
=============================== */

window.addEventListener("scroll", () => {

  const navbar = document.getElementById("navbar");

  if (navbar) {
    navbar.classList.toggle("scrolled", window.scrollY > 20);
  }

});


/* ===============================
   MOBILE MENU
=============================== */

function toggleMenu() {

  const menu = document.getElementById("mobile-menu");

  if (menu) menu.classList.toggle("open");

}


/* ===============================
   DASHBOARD STATS
=============================== */

async function loadDashboardStats() {

  try {

    const res = await fetch("/api/dashboard");

    if (!res.ok) return;

    const data = await res.json();

    setText("statTotalCustomers", data.total);
    setText("statHealthyCustomers", data.healthy);
    setText("statWarningCustomers", data.warning);
    setText("statRiskCustomers", data.high_risk);

    setText("totalCustomers", data.total);
    setText("healthyCustomers", data.healthy);
    setText("warningCustomers", data.warning);
    setText("highRiskCustomers", data.high_risk);

    console.log("Dashboard stats loaded");

  }

  catch (err) {

    console.warn("Dashboard API missing");

  }

}


/* ===============================
   CUSTOMERS LIST
=============================== */

// ===============================
// LOAD CUSTOMERS
// ===============================

fetch("/api/customers")
  .then(res => res.json())
  .then(customers => {

    console.log("Customers received:", customers.length);

    const container = document.getElementById("customersContainer");

    if (!container) {
      console.error("customersContainer not found!");
      return;
    }

    container.innerHTML = "";

    customers.forEach(customer => {

      const card = `
        <div class="glass-card" style="padding:20px;border-radius:14px;">
          <h3 style="font-weight:700;font-size:16px;margin-bottom:6px;">
            ${customer.company_name}
          </h3>

          <div style="font-size:13px;color:var(--muted);margin-bottom:6px;">
            Region: ${customer.region}
          </div>

          <div style="font-size:13px;color:var(--muted);margin-bottom:6px;">
            Plan: ${customer.plan_tier}
          </div>

          <div style="font-size:13px;color:var(--muted);margin-bottom:6px;">
            Usage: ${customer.monthly_usage}
          </div>

          <div style="font-size:13px;color:var(--muted);margin-bottom:6px;">
            Support Tickets: ${customer.support_tickets}
          </div>

          <div style="font-size:13px;font-weight:600;">
            NPS Score: ${customer.nps_score}
          </div>
        </div>
      `;

      container.innerHTML += card;

    });

  })
  .catch(err => console.error("Customers load error:", err));

/* ===============================
   HEALTH SCORES
=============================== */

async function loadHealthScores() {

  try {

    const res = await fetch("/api/health");

    if (!res.ok) return;

    const data = await res.json();

    const container =
      document.getElementById("healthScoreContainer");

    if (!container) return;

    container.innerHTML = "";

    data.forEach(c => {

      container.innerHTML += `
      <div style="padding:8px 0">

      ${c.company_name}

      — Health Score:
      <strong>${c.health_score}</strong>

      </div>
      `;

    });

  }

  catch (err) {

    console.warn("Health API missing");

  }

}


/* ===============================
   CHURN ALERTS
=============================== */

async function loadChurnAlerts() {

  try {

    const res = await fetch("/api/churn");

    if (!res.ok) return;

    const data = await res.json();

    const container =
      document.getElementById("churnAlertsContainer");

    if (!container) return;

    container.innerHTML = "";

    data.forEach(c => {

      container.innerHTML += `
      <div class="churn-alert">

      <strong>${c.company_name}</strong>

      <br>

      Churn Risk:
      ${c.churn_probability}

      </div>
      `;

    });

  }

  catch (err) {

    console.warn("Churn API missing");

  }

}


/* ===============================
   WEEKLY REPORT
=============================== */

async function loadWeeklyReport() {

  try {

    const res =
      await fetch("/api/report/weekly");

    if (!res.ok) return;

    const data =
      await res.json();

    const container =
      document.getElementById("weeklyReportContainer");

    if (!container) return;

    container.innerHTML = `
      <div>${data.summary}</div>
    `;

  }

  catch (err) {

    console.warn("Weekly report API missing");

  }

}


/* ===============================
   AI QUERY ASSISTANT
=============================== */

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

    const res =
      await fetch("/api/query", {

        method: "POST",

        headers: {
          "Content-Type": "application/json"
        },

        body: JSON.stringify({
          query: q
        })

      });

    if (!res.ok) return;

    const data =
      await res.json();

    queryResults.innerHTML =
      `<div>${data.answer}</div>`;

  }

  catch (err) {

    queryResults.innerHTML =
      `<div style="color:red">
      Backend query not ready yet
      </div>`;

  }

}


if (queryButton)
  queryButton.addEventListener(
    "click",
    handleQuery
  );


if (queryInput)
  queryInput.addEventListener(
    "keydown",
    e => {

      if (e.key === "Enter")
        handleQuery();

    }
  );


/* ===============================
   SAFE TEXT SETTER
=============================== */

function setText(id, value) {

  const el = document.getElementById(id);

  if (el)
    el.innerText = value;

}
/* ===============================
   FADE-UP SCROLL ANIMATION FIX
=============================== */

document.addEventListener("DOMContentLoaded", () => {

  const fadeEls = document.querySelectorAll(".fade-up");

  const observer = new IntersectionObserver(entries => {

    entries.forEach(entry => {

      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
      }

    });

  }, { threshold: 0.1 });

  fadeEls.forEach(el => observer.observe(el));

});