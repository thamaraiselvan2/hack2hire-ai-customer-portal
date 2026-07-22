/* ── Streamlit-patched script.js ── */
/* All fetch() calls are replaced by synchronous reads from window.__PORTAL_DATA__ */

console.log("script.js (Streamlit build) loaded.");

/* ---------- utilities ---------- */
function setText(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}
function safeRun(fn) {
  try { fn(); } catch(e) { console.warn("Optional module skipped:", e); }
}

/* ---------- boot ---------- */
function boot() {
  // Reveal the page immediately: initFadeUpObserver() goes FIRST, and every
  // call below is wrapped in safeRun(), so a failure anywhere (a missing
  // element, a CDN script that didn't load, etc.) can never again leave the
  // whole page stuck at opacity:0.
  safeRun(initFadeUpObserver);
  safeRun(initAnchorNavigation);
  safeRun(loadDashboardStats);
  safeRun(loadCustomers);
  safeRun(loadHealthScores);
  safeRun(loadChurnAlerts);
  safeRun(loadWeeklyReport);
  safeRun(initChat);
  safeRun(initActiveNavHighlight);
  safeRun(loadDashboardCharts);
  safeRun(loadWeeklyActiveUsers);
}
/* CRITICAL: Streamlit injects this HTML into its iframe AFTER the iframe
   document has already finished loading, so DOMContentLoaded has usually
   ALREADY FIRED by the time this script runs — a listener alone would never
   execute. Check readyState and run boot immediately in that case. */
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", boot);
} else {
  boot();
}

/* ---------- anchor navigation (iframe-safe) ---------- */
/* Inside Streamlit's iframe, plain href="#section" links resolve against the
   iframe's synthetic URL and often do nothing. Intercept clicks and scroll
   programmatically instead — works in every embedding scenario.
   NOTE: real cross-frame navigation links (login, logout, view-all-data) use
   target="_top" with a plain href instead of JS — browsers handle that
   natively even inside a sandboxed iframe, which is far more reliable than
   trying to set window.top.location from script. Those links are excluded
   here (they don't start with "#" so they never match the selector below). */
function initAnchorNavigation() {
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener("click", e => {
      const id = link.getAttribute("href").slice(1);
      e.preventDefault();
      // Immediately highlight the clicked nav link and lock the scroll-spy
      // briefly so it doesn't fight the smooth scroll and steal the underline.
      if (link.classList.contains("nav-link") && link.dataset.section) {
        document.querySelectorAll(".nav-link[data-section]")
          .forEach(l => l.classList.toggle("active", l === link));
        window.__navLockUntil = Date.now() + 1200;
      }
      if (!id) { window.scrollTo({ top: 0, behavior: "smooth" }); return; }
      const target = document.getElementById(id);
      if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
}

/* ---------- navbar ---------- */
window.addEventListener("scroll", () => {
  const navbar = document.getElementById("navbar");
  if (navbar) navbar.classList.toggle("scrolled", window.scrollY > 20);
});
function toggleMenu() {
  const menu = document.getElementById("mobile-menu");
  if (menu) menu.classList.toggle("open");
}

/* ---------- active nav ---------- */
function initActiveNavHighlight() {
  const navLinks = document.querySelectorAll(".nav-link[data-section]");
  if (!navLinks.length) return;
  const sections = [];
  navLinks.forEach(link => {
    const id = link.getAttribute("data-section");
    const section = document.getElementById(id);
    if (section) sections.push({ id, section, link });
  });
  if (!sections.length) return;
  function updateActiveLink() {
    if (window.__navLockUntil && Date.now() < window.__navLockUntil) return;
    const scrollY = window.scrollY, windowH = window.innerHeight;
    let activeSectionId = null;
    for (let i = sections.length - 1; i >= 0; i--) {
      const { section, id } = sections[i];
      const top = section.getBoundingClientRect().top + scrollY;
      if (scrollY + windowH * 0.4 >= top) { activeSectionId = id; break; }
    }
    navLinks.forEach(link => {
      link.classList.toggle("active", link.getAttribute("data-section") === activeSectionId);
    });
  }
  window.addEventListener("scroll", updateActiveLink, { passive: true });
  updateActiveLink();
}

/* ---------- dashboard stats ---------- */
function loadDashboardStats() {
  const data = window.__PORTAL_DATA__.dashboard;
  setText("statTotalCustomers", data.total);
  setText("statHealthyCustomers", data.healthy);
  setText("statWarningCustomers", data.warning);
  setText("statRiskCustomers", data.high_risk);
  setText("retentionRiskStatus", data.retention_status);
  setText("totalCustomers", data.total);
  setText("healthyCustomers", data.healthy);
  setText("warningCustomers", data.warning);
  setText("highRiskCustomers", data.high_risk);
}

/* ---------- customers ---------- */
let allCustomersData = [];
function loadCustomers() {
  const customers = window.__PORTAL_DATA__.customers;
  allCustomersData = customers;
  const container = document.getElementById("customersContainer");
  const extra = document.getElementById("customersExtra");
  const btnWrap = document.getElementById("viewAllWrap");
  const btn = document.getElementById("showMoreCustomersBtn");
  const btnLabel = document.getElementById("showMoreCustomersLabel");
  if (!container) return;
  container.innerHTML = "";
  if (extra) { extra.innerHTML = ""; extra.style.display = "none"; }
  const first = customers.slice(0, 3);
  const rest = customers.slice(3);
  first.forEach(c => { container.innerHTML += buildCustomerCard(c); });

  if (rest.length > 0 && extra && btn && btnLabel) {
    rest.forEach(c => { extra.innerHTML += buildCustomerCard(c); });
    if (btnWrap) btnWrap.style.display = "flex";
    btnLabel.textContent = `Show All Customers (${rest.length} more)`;

    // Avoid stacking duplicate listeners if loadCustomers ever re-runs.
    const newBtn = btn.cloneNode(true);
    btn.parentNode.replaceChild(newBtn, btn);
    newBtn.addEventListener("click", () => {
      const isHidden = extra.style.display === "none";
      extra.style.display = isHidden ? "grid" : "none";
      document.getElementById("showMoreCustomersLabel").textContent = isHidden
        ? "Show Less"
        : `Show All Customers (${rest.length} more)`;
    });
  } else {
    if (btnWrap) btnWrap.style.display = "none";
  }
}
function buildCustomerCard(customer) {
  return `
    <div class="glass-card" style="padding:20px;border-radius:14px;">
      <h3 style="font-weight:700;font-size:16px;margin-bottom:6px;">${customer.company_name}</h3>
      <div style="font-size:13px;color:var(--muted);">Region: ${customer.region}</div>
      <div style="font-size:13px;color:var(--muted);">Plan: ${customer.plan_tier}</div>
      <div style="font-size:13px;color:var(--muted);">Usage: ${customer.monthly_usage}</div>
      <div style="font-size:13px;color:var(--muted);">Support Tickets: ${customer.support_tickets}</div>
      <div style="font-size:13px;font-weight:600;">NPS Score: ${customer.nps_score}</div>
    </div>`;
}
/* ---------- health scores ---------- */
function loadHealthScores() {
  const data = window.__PORTAL_DATA__.health;
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
      </div>`;
    row.addEventListener("mouseenter", () => { row.style.borderColor = "rgba(56,189,248,0.3)"; });
    row.addEventListener("mouseleave", () => { row.style.borderColor = "var(--border)"; });
    container.appendChild(row);
  });
}

/* ---------- churn alerts ---------- */
function loadChurnAlerts() {
  const data = window.__PORTAL_DATA__.churn;
  const container = document.getElementById("churnAlertsContainer");
  if (!container) return;
  container.innerHTML = "";
  if (data.length === 0) {
    container.innerHTML = "<div style='color:var(--muted);font-size:13px;'>No churn risks detected.</div>";
    return;
  }
  data.forEach(customer => {
    const alertCard = document.createElement("div");
    alertCard.className = "churn-alert";
    alertCard.innerHTML = `<strong>${customer.company_name}</strong><br>Churn Probability: ${customer.churn_probability}%`;
    container.appendChild(alertCard);
  });
}

/* ---------- weekly report ---------- */
function loadWeeklyReport() {
  const data = window.__PORTAL_DATA__.weeklyReport;
  const summaryBlock = document.querySelector("#weeklyReportContainer p");
  if (summaryBlock) summaryBlock.textContent = data.summary;
  setText("activeUsersValue", data.active_users);
  setText("mrrGrowthValue", "+" + data.mrr_growth + "%");
  setText("churnRiskValue", "+" + data.churn_risk_change + "%");
  setText("accountsSavedValue", data.accounts_saved);
}

/* ---------- chat ---------- */
function initChat() {
  const queryButton = document.getElementById("queryButton");
  const queryInput = document.getElementById("queryInput");
  if (queryButton) queryButton.addEventListener("click", handleQuery);
  if (queryInput) queryInput.addEventListener("keydown", e => { if (e.key === "Enter") handleQuery(); });

  // If Streamlit already answered a query (page reload with ?q=...), show it
  const d = window.__PORTAL_DATA__;
  if (d.queryParam && d.queryAnswer) {
    appendBubble(d.queryParam, "user");
    const items = d.queryAnswer
      .replace(/High[\\-\\u2011]risk customers:/gi, "")
      .replace(/Customers with low usage:/gi, "")
      .replace(/Enterprise customers:/gi, "")
      .replace(/Customers with low NPS score:/gi, "")
      .trim()
      .split(",").map(s => s.trim()).filter(Boolean);
    items.forEach((item, i) => setTimeout(() => appendBubble(item, "ai"), i * 380));
  }
}
function sendSuggestion(el) {
  const text = el.textContent.trim();
  const input = document.getElementById("queryInput");
  if (input) { input.value = text; handleQuery(); }
  const chips = document.getElementById("chatSuggestions");
  if (chips) chips.style.display = "none";
}
async function handleQuery() {
  const input = document.getElementById("queryInput");
  const q = input ? input.value.trim() : "";
  if (!q) return;
  if (input) input.value = "";
  const chips = document.getElementById("chatSuggestions");
  if (chips) chips.style.display = "none";
  appendBubble(q, "user");
  const typingId = showTyping();
  // Answer instantly from the embedded data — no page reload needed.
  setTimeout(() => {
    removeTyping(typingId);
    const answers = answerQuery(q);
    answers.forEach((a, i) => setTimeout(() => appendBubble(a, "ai"), i * 300));
  }, 500);
}

/* ---------- client-side answer engine ---------- */
function answerQuery(raw) {
  const q = raw.toLowerCase();
  const customers = (window.__PORTAL_DATA__ && window.__PORTAL_DATA__.customers) || [];
  if (!customers.length) return ["I couldn't load the customer data. Please refresh the page."];

  const names = list => list.map(c => c.company_name);
  const fmt = list => list.length ? names(list).join(", ") : null;

  // 1. Specific company lookup — if the query mentions a company name
  const mentioned = customers.find(c => q.includes(c.company_name.toLowerCase()));
  if (mentioned) {
    const c = mentioned;
    const risk = c.nps_score < 5 ? "HIGH churn risk" : c.nps_score < 7 ? "medium churn risk" : "healthy";
    return [
      `${c.company_name} — ${c.plan_tier} plan, ${c.region} region.`,
      `Usage: ${c.monthly_usage} · Support tickets: ${c.support_tickets} · NPS: ${c.nps_score}/10 · Health score: ${c.nps_score * 10}/100.`,
      `Status: ${risk}.`
    ];
  }

  // 2. Counts
  if (q.includes("how many") || q.includes("count") || q.includes("total")) {
    if (q.includes("risk")) {
      const n = customers.filter(c => c.nps_score < 5).length;
      return [`There ${n === 1 ? "is" : "are"} ${n} high-risk customer${n === 1 ? "" : "s"} right now.`];
    }
    return [`You have ${customers.length} customers in total.`];
  }

  // 3. Risk / churn
  if (q.includes("high risk") || q.includes("at risk") || q.includes("churn")) {
    const r = customers.filter(c => c.nps_score < 5);
    return r.length
      ? [`⚠️ High-risk customers (likely to churn):`, ...r.map(c => `${c.company_name} — NPS ${c.nps_score}, ${c.support_tickets} open tickets, ${c.monthly_usage} usage`)]
      : ["Good news — no high-risk customers right now! 🎉"];
  }

  // 4. Healthy / best customers
  if (q.includes("best") || q.includes("healthy") || q.includes("happiest") || q.includes("top")) {
    const top = [...customers].sort((a, b) => b.nps_score - a.nps_score).slice(0, 3);
    return ["🏆 Your healthiest customers:", ...top.map(c => `${c.company_name} — NPS ${c.nps_score}, ${c.plan_tier} plan`)];
  }

  // 5. Usage
  if (q.includes("low usage")) {
    const r = fmt(customers.filter(c => c.monthly_usage === "Low"));
    return [r ? `Customers with low usage: ${r}. These may need re-engagement.` : "No customers with low usage."];
  }
  if (q.includes("high usage")) {
    const r = fmt(customers.filter(c => c.monthly_usage === "High"));
    return [r ? `Customers with high usage: ${r}. Great upsell candidates!` : "No customers with high usage."];
  }

  // 6. Plan tiers
  for (const tier of ["premium", "enterprise", "standard", "basic"]) {
    if (q.includes(tier)) {
      const r = fmt(customers.filter(c => (c.plan_tier || "").toLowerCase() === tier));
      return [r ? `${tier[0].toUpperCase() + tier.slice(1)} plan customers: ${r}.` : `No customers on the ${tier} plan.`];
    }
  }

  // 7. Regions
  for (const region of ["north", "south", "east", "west"]) {
    if (q.includes(region)) {
      const r = fmt(customers.filter(c => (c.region || "").toLowerCase() === region));
      return [r ? `${region[0].toUpperCase() + region.slice(1)} region customers: ${r}.` : `No customers in the ${region} region.`];
    }
  }

  // 8. Support tickets
  if (q.includes("ticket") || q.includes("support") || q.includes("complain")) {
    const sorted = [...customers].sort((a, b) => b.support_tickets - a.support_tickets).slice(0, 3);
    return ["Customers with the most support tickets:", ...sorted.map(c => `${c.company_name} — ${c.support_tickets} tickets`)];
  }

  // 9. NPS
  if (q.includes("nps") || q.includes("score")) {
    const low = customers.filter(c => c.nps_score < 6);
    return low.length
      ? ["Customers with low NPS scores:", ...low.map(c => `${c.company_name} — NPS ${c.nps_score}/10`)]
      : ["All customers have healthy NPS scores!"];
  }

  // 10. Greetings / help
  if (/\b(hi|hello|hey|help)\b/.test(q)) {
    return [
      "Hi! I can answer questions about your customers. Try asking:",
      "• Which customers are at high risk?",
      "• Show premium customers",
      "• Who has the most support tickets?",
      "• Tell me about " + customers[0].company_name
    ];
  }

  // Fallback
  return [
    "I'm not sure about that one. I can answer things like:",
    "• high risk customers  • customers in the south region",
    "• premium plan customers  • who has low usage",
    "• details about any specific company by name"
  ];
}
function appendBubble(text, type) {
  const messages = document.getElementById("chatMessages");
  if (!messages) return;
  const bubble = document.createElement("div");
  bubble.className = `chat-bubble ${type === "user" ? "bubble-user" : "bubble-ai"}`;
  bubble.textContent = text;
  messages.appendChild(bubble);
  scrollToBottom(messages);
}
function showTyping() {
  const messages = document.getElementById("chatMessages");
  if (!messages) return null;
  const id = "typing-" + Date.now();
  const el = document.createElement("div");
  el.className = "bubble-typing"; el.id = id;
  el.innerHTML = `<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>`;
  messages.appendChild(el);
  scrollToBottom(messages);
  return id;
}
function removeTyping(id) { if (id) { const el = document.getElementById(id); if (el) el.remove(); } }
function scrollToBottom(el) { if (el) requestAnimationFrame(() => { el.scrollTop = el.scrollHeight; }); }

/* ---------- fade-up animation (progressive enhancement) ---------- */
/* Content is visible by default via plain CSS (.fade-up{opacity:1}).
   This function ONLY adds the scroll-reveal animation on top — if anything
   here fails or never runs, the page still displays normally. */
function initFadeUpObserver() {
  const fadeEls = document.querySelectorAll(".fade-up");
  if (!fadeEls.length) return;
  try {
    document.documentElement.classList.add("js");
    fadeEls.forEach(el => el.classList.add("animate-pending"));

    if ("IntersectionObserver" in window) {
      const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.remove("animate-pending");
            entry.target.classList.add("visible");
          }
        });
      }, { threshold: 0.1 });
      fadeEls.forEach(el => observer.observe(el));
    } else {
      fadeEls.forEach(el => el.classList.remove("animate-pending"));
    }

    // Belt-and-braces: whatever happens, nothing stays hidden past 800ms.
    setTimeout(() => {
      document.querySelectorAll(".fade-up.animate-pending")
        .forEach(el => el.classList.remove("animate-pending"));
    }, 800);
  } catch (e) {
    console.warn("Fade-in animation disabled due to error (content still visible):", e);
    fadeEls.forEach(el => el.classList.remove("animate-pending"));
    document.documentElement.classList.remove("js");
  }
}

/* ---------- dashboard charts ---------- */
function loadDashboardCharts() {
  if (typeof Chart === "undefined") { console.warn("Chart.js did not load; skipping charts."); return; }
  const data = window.__PORTAL_DATA__.dashboardCharts;
  const ctxLine = document.getElementById("lineChart");
  if (ctxLine) {
    new Chart(ctxLine, {
      type: "line",
      data: {
        labels: data.customer_growth.labels,
        datasets: [
          { label: "New", data: data.customer_growth.new, borderColor: "#38bdf8", backgroundColor: "rgba(56,189,248,0.1)", tension: 0.4 },
          { label: "Retained", data: data.customer_growth.retained, borderColor: "#a78bfa", backgroundColor: "rgba(167,139,250,0.1)", tension: 0.4 }
        ]
      },
      options: {
        responsive: true,
        plugins: { legend: { labels: { color: "#e2e8f0" } } },
        scales: { x: { ticks: { color: "#64748b" } }, y: { ticks: { color: "#64748b" } } }
      }
    });
  }
  const ctxPie = document.getElementById("pieChart");
  if (ctxPie) {
    new Chart(ctxPie, {
      type: "doughnut",
      data: {
        labels: data.segments.labels,
        datasets: [{ data: data.segments.values, backgroundColor: ["#38bdf8", "#a78bfa", "#22d3ee", "#f43f5e"] }]
      },
      options: { plugins: { legend: { labels: { color: "#e2e8f0" } } } }
    });
  }
}

/* ---------- weekly active users chart ---------- */
function loadWeeklyActiveUsers() {
  if (typeof Chart === "undefined") { console.warn("Chart.js did not load; skipping chart."); return; }
  const data = window.__PORTAL_DATA__.weeklyActiveUsers;
  const ctx = document.getElementById("reportChart");
  if (!ctx) return;
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: data.labels,
      datasets: [{ label: "Active Users", data: data.values, backgroundColor: "#38bdf8" }]
    },
    options: {
      responsive: true,
      plugins: { legend: { labels: { color: "#e2e8f0" } } },
      scales: { x: { ticks: { color: "#64748b" } }, y: { ticks: { color: "#64748b" } } }
    }
  });
}

/* ---------- weekly stats (no-op stub — data already in weeklyReport) ---------- */
function loadWeeklyReportStats() {
  const data = window.__PORTAL_DATA__.weeklyReport;
  setText("weeklyMRR", data.mrr_growth + "%");
  setText("weeklyChurnRisk", data.churn_risk_change + "%");
  setText("weeklyAccountsSaved", data.accounts_saved);
}
loadWeeklyReportStats();