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

  safeRun(loadHealthScores);
  safeRun(loadChurnAlerts);
  safeRun(loadWeeklyReport);

  initChat();
  initFadeUpObserver();
  loadChurnAlerts();
  loadWeeklyReport();

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
    setText("retentionRiskStatus", data.retention_status);

    setText("totalCustomers", data.total);
    setText("healthyCustomers", data.healthy);
    setText("warningCustomers", data.warning);
    setText("highRiskCustomers", data.high_risk);

  } catch (err) {
    console.warn("Dashboard API missing");
  }
}

/* ===============================
   LOAD CUSTOMERS — TASK 8
   Show first 3 initially, rest on "View All"
=============================== */

let allCustomersData = [];

async function loadCustomers() {
  try {
    const res = await fetch("/api/customers");
    const customers = await res.json();
    allCustomersData = customers;

    const container = document.getElementById("customersContainer");
    const extra     = document.getElementById("customersExtra");
    const btnWrap   = document.getElementById("viewAllWrap");

    if (!container) return;

    container.innerHTML = "";
    if (extra) extra.innerHTML = "";

    // First 3 always visible
    const first  = customers.slice(0, 3);
    const rest   = customers.slice(3);

    first.forEach(customer => {
      container.innerHTML += buildCustomerCard(customer);
    });

    // If there are more, populate hidden container
    if (rest.length > 0 && extra) {
      rest.forEach(customer => {
        extra.innerHTML += buildCustomerCard(customer);
      });
      // Show View All button
      if (btnWrap) btnWrap.style.display = "flex";
    } else {
      // No extra customers — hide button
      if (btnWrap) btnWrap.style.display = "none";
    }

  } catch (err) {
    console.warn("Customers API missing");
    // Hide View All button if API fails
    const btnWrap = document.getElementById("viewAllWrap");
    if (btnWrap) btnWrap.style.display = "none";
  }
}

function buildCustomerCard(customer) {
  return `
    <div class="glass-card" style="padding:20px;border-radius:14px;">
      <h3 style="font-weight:700;font-size:16px;margin-bottom:6px;">
        ${customer.company_name}
      </h3>
      <div style="font-size:13px;color:var(--muted);">Region: ${customer.region}</div>
      <div style="font-size:13px;color:var(--muted);">Plan: ${customer.plan_tier}</div>
      <div style="font-size:13px;color:var(--muted);">Usage: ${customer.monthly_usage}</div>
      <div style="font-size:13px;color:var(--muted);">Support Tickets: ${customer.support_tickets}</div>
      <div style="font-size:13px;font-weight:600;">NPS Score: ${customer.nps_score}</div>
    </div>
  `;
}

/* Expand to show all customers — called by View All button */
function expandCustomers() {
  const extra   = document.getElementById("customersExtra");
  const btnWrap = document.getElementById("viewAllWrap");

  if (extra) {
    extra.style.display = "grid";
    // Animate cards in
    Array.from(extra.children).forEach((card, i) => {
      card.style.opacity = "0";
      card.style.transform = "translateY(20px)";
      card.style.transition = "opacity 0.4s ease, transform 0.4s ease";
      setTimeout(() => {
        card.style.opacity = "1";
        card.style.transform = "translateY(0)";
      }, i * 80);
    });
  }

  // Remove the button after expanding
  if (btnWrap) btnWrap.style.display = "none";
}

/* ===============================
   HEALTH SCORES
=============================== */

async function loadHealthScores() {
  try {
    const res = await fetch("/api/health");
    if (!res.ok) return;
    const data = await res.json();

    const container = document.getElementById("healthScoreContainer");
    if (!container) return;

    // Keep the legend row, then append scores
    const legend = container.querySelector("div");
    container.innerHTML = "";
    if (legend) container.appendChild(legend);

    data.forEach(c => {
      const score = parseInt(c.health_score) || 0;
      let color = "#22c55e";
      if (score < 40) color = "#f43f5e";
      else if (score < 75) color = "#fbbf24";

      const row = document.createElement("div");
      row.style.cssText = "display:flex;align-items:center;justify-content:space-between;padding:10px 12px;background:var(--surface2);border:1px solid var(--border);border-radius:8px;transition:all 0.2s;";
      row.innerHTML = `
        <div style="font-size:13px;font-weight:500;">${c.company_name}</div>
        <div style="display:flex;align-items:center;gap:10px;">
          <div style="width:80px;height:5px;border-radius:3px;background:rgba(255,255,255,0.06);overflow:hidden;">
            <div style="width:${score}%;height:100%;background:${color};border-radius:3px;transition:width 0.8s ease;"></div>
          </div>
          <span style="font-family:'Syne',sans-serif;font-weight:700;font-size:14px;color:${color};min-width:26px;text-align:right;">${score}</span>
        </div>
      `;
      row.addEventListener("mouseenter", () => { row.style.borderColor = "rgba(56,189,248,0.3)"; });
      row.addEventListener("mouseleave", () => { row.style.borderColor = "var(--border)"; });
      container.appendChild(row);
    });

  } catch (err) {
    console.warn("Health API missing");
  }
}

/* ===============================
   CHURN ALERTS
=============================== */


async function loadChurnAlerts() {

  const res = await fetch("/api/churn");
  const data = await res.json();

  const container = document.getElementById("churnAlertsContainer");

  if (!container) return;

  container.innerHTML = "";

  data.forEach(customer => {

    const row = document.createElement("div");

    row.style.marginBottom = "8px";

    row.innerHTML =
      `<strong>${customer.company_name}</strong> — Risk: ${customer.churn_probability}%`;

    container.appendChild(row);

  });

}

loadChurnAlerts();

/* ===============================
   WEEKLY REPORT
=============================== */

async function loadWeeklyReport() {

  try {

    const response = await fetch("/api/report/weekly");

    const data = await response.json();

    // Update summary text
    const summaryBlock =
      document.querySelector("#weeklyReportContainer p");

    if (summaryBlock) {
      summaryBlock.textContent = data.summary;
    }

    // Update KPI values

    document.getElementById("activeUsersValue").textContent =
      data.active_users;

    document.getElementById("mrrGrowthValue").textContent =
      "+" + data.mrr_growth + "%";

    document.getElementById("churnRiskValue").textContent =
      "+" + data.churn_risk_change + "%";

    document.getElementById("accountsSavedValue").textContent =
      data.accounts_saved;

  }

  catch (error) {

    console.error("Weekly report load error:", error);

  }

}

/* ===============================
   CHAT SYSTEM — TASKS 5, 6, 7
=============================== */

function initChat() {
  const queryButton = document.getElementById("queryButton");
  const queryInput  = document.getElementById("queryInput");

  if (queryButton) queryButton.addEventListener("click", handleQuery);

  if (queryInput) {
    queryInput.addEventListener("keydown", e => {
      if (e.key === "Enter") handleQuery();
    });
  }
}

/* Send a suggestion chip */
function sendSuggestion(el) {
  const text = el.textContent.trim();
  const input = document.getElementById("queryInput");
  if (input) {
    input.value = text;
    handleQuery();
  }
  // Hide chips after first use for cleaner UI
  const chips = document.getElementById("chatSuggestions");
  if (chips) chips.style.display = "none";
}

/* Core query handler */
async function handleQuery() {
  const input = document.getElementById("queryInput");
  const q = input ? input.value.trim() : "";
  if (!q) return;

  // Clear input
  if (input) input.value = "";

  // Hide suggestion chips after first real message
  const chips = document.getElementById("chatSuggestions");
  if (chips) chips.style.display = "none";

  // Append user bubble — TASK 7: right-aligned
  appendBubble(q, "user");

  // Show typing indicator
  const typingId = showTyping();

  try {
    const res = await fetch("/api/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: q })
    });

    const data = await res.json();

    // Remove typing indicator
    removeTyping(typingId);

    // Clean the answer — remove any prefix labels
    let cleaned = (data.answer || "")
      .replace(/High[\-‑]risk customers:/gi, "")
      .replace(/Customers with low usage:/gi, "")
      .replace(/Enterprise customers:/gi, "")
      .replace(/Customers with low NPS score:/gi, "")
      .trim();

    const items = cleaned.split(",").map(s => s.trim()).filter(Boolean);

    if (items.length === 0) {
      appendBubble("No results found.", "ai");
      return;
    }

    // TASK 7: Animate each item in with staggered delay — left-aligned bubbles
    items.forEach((item, index) => {
      setTimeout(() => {
        appendBubble(item, "ai");
      }, index * 380);
    });

  } catch (err) {
    removeTyping(typingId);
    appendBubble("Could not connect to the backend. Please check your server.", "ai");
    console.warn("Query API error:", err);
  }
}

/* Append a chat bubble — TASK 7: user = right, ai = left */
function appendBubble(text, type) {
  const messages = document.getElementById("chatMessages");
  if (!messages) return;

  const bubble = document.createElement("div");
  bubble.className = `chat-bubble ${type === "user" ? "bubble-user" : "bubble-ai"}`;
  bubble.textContent = text;

  messages.appendChild(bubble);
  scrollToBottom(messages);
}

/* Show typing indicator, return unique id */
function showTyping() {
  const messages = document.getElementById("chatMessages");
  if (!messages) return null;

  const id = "typing-" + Date.now();
  const el = document.createElement("div");
  el.className = "bubble-typing";
  el.id = id;
  el.innerHTML = `
    <div class="typing-dot"></div>
    <div class="typing-dot"></div>
    <div class="typing-dot"></div>
  `;

  messages.appendChild(el);
  scrollToBottom(messages);
  return id;
}

/* Remove typing indicator by id */
function removeTyping(id) {
  if (!id) return;
  const el = document.getElementById(id);
  if (el) el.remove();
}

/* Smooth scroll chat to bottom */
function scrollToBottom(el) {
  if (el) {
    requestAnimationFrame(() => {
      el.scrollTop = el.scrollHeight;
    });
  }
}

/* ===============================
   FADE-UP SCROLL ANIMATION
=============================== */

function initFadeUpObserver() {
  const fadeEls = document.querySelectorAll(".fade-up");

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
      }
    });
  }, { threshold: 0.1 });

  fadeEls.forEach(el => observer.observe(el));
}

/* ===============================
   SAFE TEXT SETTER
=============================== */

function setText(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}
// ===============================
// LOAD CHURN ALERTS
// ===============================

async function loadChurnAlerts() {

  try {

    const response = await fetch("/api/churn");
    const data = await response.json();

    const container = document.getElementById("churnAlertsContainer");

    if (!container) return;

    container.innerHTML = "";

    if (data.length === 0) {

      container.innerHTML =
        "<div style='color:var(--muted);font-size:13px;'>No churn risks detected.</div>";

      return;
    }

    data.forEach(customer => {

      const alertCard = document.createElement("div");

      alertCard.className = "churn-alert";

      alertCard.innerHTML = `
        <strong>${customer.company_name}</strong><br>
        Churn Probability: ${customer.churn_probability}%
      `;

      container.appendChild(alertCard);

    });

  } catch (error) {

    console.error("Error loading churn alerts:", error);

  }

}
// ===============================
// LOAD WEEKLY REPORT DATA
// ===============================

async function loadWeeklyReport() {

  try {

    const response = await fetch("/api/report/weekly");
    const data = await response.json();

    // Executive summary
    const summaryBlock = document.querySelector(
      "#weeklyReportContainer p"
    );

    if (summaryBlock) {
      summaryBlock.textContent = data.summary;
    }

    // KPI values
    const kpiCards = document.querySelectorAll(
      "#weeklyReportContainer .surface2 div"
    );

  } catch (error) {

    console.error("Error loading weekly report:", error);

  }

}
// ===============================
// AUTO REFRESH DASHBOARD EVERY 20 SECONDS
// ===============================

setInterval(() => {

  console.log("Refreshing dashboard data...");

  loadDashboardStats();
  loadCustomers();
  loadHealthScores();
  loadChurnAlerts();
  loadWeeklyReport();

}, 20000);
async function loadWeeklyReportStats() {
  const res = await fetch("/api/weekly-stats");
  const data = await res.json();

  document.getElementById("weeklyMRR").textContent =
    data.mrr_growth + "%";

  document.getElementById("weeklyChurnRisk").textContent =
    data.churn_risk + "%";

  document.getElementById("weeklyAccountsSaved").textContent =
    data.accounts_saved;
}

loadWeeklyReportStats();
async function loadDashboardCharts() {

  const res = await fetch("/api/dashboard-charts");
  const data = await res.json();


  // Customer Growth Line Chart
  const ctxLine = document.getElementById("lineChart");

  new Chart(ctxLine, {
    type: "line",
    data: {
      labels: data.customer_growth.labels,
      datasets: [
        {
          label: "New",
          data: data.customer_growth.new,
          borderColor: "#38bdf8",
          backgroundColor: "rgba(56,189,248,0.1)",
          tension: 0.4
        },
        {
          label: "Retained",
          data: data.customer_growth.retained,
          borderColor: "#a78bfa",
          backgroundColor: "rgba(167,139,250,0.1)",
          tension: 0.4
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          labels: {
            color: "#e2e8f0"
          }
        }
      },
      scales: {
        x: {
          ticks: { color: "#64748b" }
        },
        y: {
          ticks: { color: "#64748b" }
        }
      }
    }
  });


  // User Segments Pie Chart
  const ctxPie = document.getElementById("pieChart");

new Chart(ctxPie, {
  type: "doughnut",
  data: {
    labels: data.segments.labels,
    datasets: [{
      data: data.segments.values,
        backgroundColor: [
          "#38bdf8",
          "#a78bfa",
          "#22d3ee",
          "#f43f5e"
        ]
      }]
    },
    options: {
      plugins: {
        legend: {
          labels: {
            color: "#e2e8f0"
          }
        }
      }
    }
  });

}

loadDashboardCharts();
async function loadWeeklyActiveUsers() {

  const res = await fetch("/api/weekly-active-users");
  const data = await res.json();

  const ctx = document.getElementById("reportChart");

  new Chart(ctx, {
    type: "bar",
    data: {
      labels: data.labels,
      datasets: [{
        label: "Active Users",
        data: data.values,
        backgroundColor: "#38bdf8"
      }]
    },
    options: {
      plugins: {
        legend: {
          labels: { color: "#e2e8f0" }
        }
      },
      scales: {
        x: {
          ticks: { color: "#64748b" }
        },
        y: {
          ticks: { color: "#64748b" }
        }
      }
    }
  });

}

loadWeeklyActiveUsers();