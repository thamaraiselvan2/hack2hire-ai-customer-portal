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
  initActiveNavHighlight(); // TASK 3: active nav scroll detection
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
   TASK 3: ACTIVE NAV-LINK HIGHLIGHT
   Highlights the navbar link matching the
   section currently visible in the viewport.
=============================== */

function initActiveNavHighlight() {
  // Map section IDs to their nav links via data-section attribute
  const navLinks = document.querySelectorAll(".nav-link[data-section]");
  if (!navLinks.length) return;

  // Build list of watched sections
  const sections = [];
  navLinks.forEach(link => {
    const id = link.getAttribute("data-section");
    const section = document.getElementById(id);
    if (section) sections.push({ id, section, link });
  });

  if (!sections.length) return;

  function updateActiveLink() {
    const scrollY = window.scrollY;
    const windowH = window.innerHeight;

    let activeSectionId = null;

    // Find which section's top is closest to (but above) 40% viewport height
    // This gives a natural feel — section activates as you scroll into it
    for (let i = sections.length - 1; i >= 0; i--) {
      const { section, id } = sections[i];
      const top = section.getBoundingClientRect().top + scrollY;
      if (scrollY + windowH * 0.4 >= top) {
        activeSectionId = id;
        break;
      }
    }

    // Apply/remove active class
    navLinks.forEach(link => {
      const isActive = link.getAttribute("data-section") === activeSectionId;
      link.classList.toggle("active", isActive);
    });
  }

  // Listen to scroll and call on load
  window.addEventListener("scroll", updateActiveLink, { passive: true });
  updateActiveLink();
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
   LOAD CUSTOMERS
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
      if (btnWrap) btnWrap.style.display = "flex";
    } else {
      if (btnWrap) btnWrap.style.display = "none";
    }

  } catch (err) {
    console.warn("Customers API missing");
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

/* ===============================
   WEEKLY REPORT
=============================== */

async function loadWeeklyReport() {
  try {
    const response = await fetch("/api/report/weekly");
    const data = await response.json();

    const summaryBlock = document.querySelector("#weeklyReportContainer p");
    if (summaryBlock) {
      summaryBlock.textContent = data.summary;
    }

    setText("activeUsersValue",   data.active_users);
    setText("mrrGrowthValue",     "+" + data.mrr_growth + "%");
    setText("churnRiskValue",     "+" + data.churn_risk_change + "%");
    setText("accountsSavedValue", data.accounts_saved);

  } catch (error) {
    console.error("Weekly report load error:", error);
  }
}

/* ===============================
   CHAT SYSTEM
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
  const chips = document.getElementById("chatSuggestions");
  if (chips) chips.style.display = "none";
}

/* Core query handler */
async function handleQuery() {
  const input = document.getElementById("queryInput");
  const q = input ? input.value.trim() : "";
  if (!q) return;

  if (input) input.value = "";

  const chips = document.getElementById("chatSuggestions");
  if (chips) chips.style.display = "none";

  appendBubble(q, "user");

  const typingId = showTyping();

  try {
    const res = await fetch("/api/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: q })
    });

    const data = await res.json();

    removeTyping(typingId);

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

/* Append a chat bubble — user = right, ai = left */
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

/* ===============================
   DASHBOARD CHARTS
=============================== */

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
        legend: { labels: { color: "#e2e8f0" } }
      },
      scales: {
        x: { ticks: { color: "#64748b" } },
        y: { ticks: { color: "#64748b" } }
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
        backgroundColor: ["#38bdf8", "#a78bfa", "#22d3ee", "#f43f5e"]
      }]
    },
    options: {
      plugins: {
        legend: { labels: { color: "#e2e8f0" } }
      }
    }
  });
}

loadDashboardCharts();

/* ===============================
   WEEKLY ACTIVE USERS CHART
=============================== */

async function loadWeeklyActiveUsers() {
  try {
    const res = await fetch("/api/weekly-active-users");
    if (!res.ok) return;
    const data = await res.json();

    const ctx = document.getElementById("reportChart");
    if (!ctx) return;

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
        responsive: true,
        plugins: {
          legend: { labels: { color: "#e2e8f0" } }
        },
        scales: {
          x: { ticks: { color: "#64748b" } },
          y: { ticks: { color: "#64748b" } }
        }
      }
    });

  } catch (err) {
    console.error("Weekly active users chart error:", err);
  }
}

loadWeeklyActiveUsers();

/* ===============================
   WEEKLY STATS
=============================== */

async function loadWeeklyReportStats() {
  try {
    const res = await fetch("/api/weekly-stats");

    if (!res.ok) return;

    const data = await res.json();

    // Existing stats
    setText("weeklyMRR", data.mrr_growth + "%");
    setText("weeklyChurnRisk", data.churn_risk + "%");
    setText("weeklyAccountsSaved", data.accounts_saved);

    // NEW stat (Contracts Expiring Soon)
    setText("contractsExpiringValue", data.contracts_expiring);

  } catch (err) {
    console.warn("Weekly stats API missing");
  }
}

// Run function
loadWeeklyReportStats();

/* ===============================
   AUTO REFRESH DASHBOARD EVERY 20 SECONDS
=============================== */

setInterval(() => {
  console.log("Refreshing dashboard data...");
  loadDashboardStats();
  loadCustomers();
  loadHealthScores();
  loadChurnAlerts();
  loadWeeklyReport();
}, 20000);