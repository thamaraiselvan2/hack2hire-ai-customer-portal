"""
streamlit_app.py — Streamlit entry point for the AI Customer Portal.

Strategy
--------
The original Flask app served one HTML page and answered /api/* calls
from the browser.  Streamlit cannot run Flask routes, so we:

1. Load the raw HTML template once.
2. Replace the two Jinja2 url_for() calls with inline <style> and <script> blocks.
3. Run every "API" function in pure Python (same logic as the old Flask routes).
4. Embed the computed data as a JSON blob inside the page so the existing
   script.js can read it WITHOUT making any fetch() calls.
5. Serve the final HTML string via st.components.v1.html().

No design changes are made — every class, colour, animation and layout
from the original index.html / style.css / script.js is preserved.
"""

import json
import os
import sqlite3
import pathlib
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR  = pathlib.Path(__file__).parent
DB_PATH   = BASE_DIR / "backend" / "customers.db"
CSV_PATH  = BASE_DIR / "data" / "customers.csv"
HTML_PATH = BASE_DIR / "frontend" / "templates" / "index.html"
CSS_PATH  = BASE_DIR / "frontend" / "static" / "style.css"
JS_PATH   = BASE_DIR / "frontend" / "static" / "script.js"

# ── Streamlit page config ────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Customer Management Portal",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide Streamlit chrome so the custom navbar looks clean
st.markdown(
    """
    <style>
    #MainMenu, header, footer { visibility: hidden; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Database helper ──────────────────────────────────────────────────────────
def get_connection() -> sqlite3.Connection:
    if not DB_PATH.exists():
        st.error(f"Database not found at: {DB_PATH}")
        st.stop()
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


# ── API functions (mirrors Flask routes) ────────────────────────────────────

def api_dashboard() -> dict:
    conn = get_connection()
    try:
        total     = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        healthy   = conn.execute("SELECT COUNT(*) FROM customers WHERE nps_score >= 8").fetchone()[0]
        warning   = conn.execute("SELECT COUNT(*) FROM customers WHERE nps_score BETWEEN 5 AND 7").fetchone()[0]
        high_risk = conn.execute("SELECT COUNT(*) FROM customers WHERE nps_score < 5").fetchone()[0]

        if total == 0:
            retention_status = "Unknown"
        else:
            risk_ratio = high_risk / total
            if risk_ratio > 0.4:
                retention_status = "High"
            elif risk_ratio > 0.2:
                retention_status = "Moderate"
            else:
                retention_status = "Low"

        return {
            "total": total,
            "healthy": healthy,
            "warning": warning,
            "high_risk": high_risk,
            "retention_status": retention_status,
        }
    finally:
        conn.close()


def api_customers() -> list:
    conn = get_connection()
    try:
        rows = conn.execute("""
            SELECT company_name, region, plan_tier,
                   monthly_usage, support_tickets, nps_score
            FROM customers
            ORDER BY nps_score ASC
        """).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def api_health() -> list:
    conn = get_connection()
    try:
        rows = conn.execute("""
            SELECT company_name, (nps_score * 10) AS health_score
            FROM customers
            ORDER BY health_score DESC
        """).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def api_churn() -> list:
    conn = get_connection()
    try:
        rows = conn.execute("""
            SELECT company_name,
                   (10 - nps_score) * 10 AS churn_probability
            FROM customers
            WHERE nps_score < 6
            ORDER BY churn_probability DESC
        """).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def api_weekly_report() -> dict:
    df = pd.read_csv(str(CSV_PATH))
    total     = len(df)
    high_risk = len(df[df["nps_score"] < 6])
    premium   = len(df[df["plan_tier"] == "Premium"])
    low_usage = len(df[df["monthly_usage"] == "Low"])

    parts = []
    if high_risk > 0:
        parts.append(f"{high_risk} customers currently show elevated churn risk.")
    if premium > 0:
        parts.append(f"{premium} customers are on Premium plans indicating strong enterprise adoption.")
    if low_usage > 0:
        parts.append(f"{low_usage} customers show low engagement levels requiring attention.")
    if not parts:
        parts.append("Customer engagement remains stable across segments this week.")

    return {
        "summary": " ".join(parts),
        "active_users": total - low_usage,
        "mrr_growth": premium * 2,
        "churn_risk_change": high_risk,
        "accounts_saved": total - high_risk,
    }


def api_dashboard_charts() -> dict:
    df = pd.read_csv(str(CSV_PATH))
    df["signup_date"] = pd.to_datetime(df["signup_date"])
    df["month"] = df["signup_date"].dt.month_name().str[:3]

    month_order = ["Jan","Feb","Mar","Apr","May","Jun",
                   "Jul","Aug","Sep","Oct","Nov","Dec"]
    monthly_counts    = df["month"].value_counts()
    new_customers     = [int(monthly_counts.get(m, 0)) for m in month_order]
    retained_customers = [int(max(n - 1, 0)) for n in new_customers]
    segment_counts    = df["plan_tier"].value_counts()

    return {
        "customer_growth": {
            "labels": month_order,
            "new": new_customers,
            "retained": retained_customers,
        },
        "segments": {
            "labels": segment_counts.index.tolist(),
            "values": [int(v) for v in segment_counts.values.tolist()],
        },
    }


def api_weekly_active_users() -> dict:
    df = pd.read_csv(str(CSV_PATH))
    df["last_active_date"] = pd.to_datetime(df["last_active_date"])
    df["weekday"] = df["last_active_date"].dt.day_name()
    order  = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    counts = df["weekday"].value_counts()
    return {"labels": order, "values": [int(counts.get(d, 0)) for d in order]}


def api_query(query: str) -> str:
    """Mirror of the Flask /api/query route."""
    q    = query.lower().strip()
    conn = get_connection()
    try:
        if "high risk" in q and "why" not in q:
            rows  = conn.execute("SELECT company_name FROM customers WHERE nps_score < 5").fetchall()
            names = [r["company_name"] for r in rows]
            return "High‑risk customers: " + ", ".join(names) if names else "No high‑risk customers found."

        if "enterprise" in q:
            rows  = conn.execute("SELECT company_name FROM customers WHERE plan_tier = 'Enterprise'").fetchall()
            names = [r["company_name"] for r in rows]
            return "Enterprise customers: " + ", ".join(names)

        if "low usage" in q:
            rows  = conn.execute("SELECT company_name FROM customers WHERE monthly_usage = 'Low'").fetchall()
            names = [r["company_name"] for r in rows]
            return "Customers with low usage: " + ", ".join(names)

        if "low nps" in q or "low score" in q:
            rows  = conn.execute("SELECT company_name FROM customers WHERE nps_score < 6").fetchall()
            names = [r["company_name"] for r in rows]
            return "Customers with low NPS score: " + ", ".join(names)

        for region in ["north", "south", "east", "west"]:
            if region in q:
                rows  = conn.execute(
                    f"SELECT company_name FROM customers WHERE region = '{region.capitalize()}'"
                ).fetchall()
                names = [r["company_name"] for r in rows]
                return f"{region.capitalize()} region customers: " + ", ".join(names)

        return "Try queries like: high risk customers, enterprise customers, customers with low usage, customers in south region."
    finally:
        conn.close()


# ── Chat query via Streamlit state ───────────────────────────────────────────
# We use a query-param trick: the JS sends the query via
# window.parent.postMessage and we pick it up in a Streamlit component.
# Simpler alternative used here: inject a hidden text_input watched by JS.

query_param = st.query_params.get("q", "")
query_answer = ""
if query_param:
    query_answer = api_query(query_param)


# ── Build the data blob to inject ────────────────────────────────────────────
data_blob = {
    "dashboard":        api_dashboard(),
    "customers":        api_customers(),
    "health":           api_health(),
    "churn":            api_churn(),
    "weeklyReport":     api_weekly_report(),
    "dashboardCharts":  api_dashboard_charts(),
    "weeklyActiveUsers": api_weekly_active_users(),
    "queryAnswer":      query_answer,
    "queryParam":       query_param,
}

injected_data_script = f"""
<script>
window.__PORTAL_DATA__ = {json.dumps(data_blob, ensure_ascii=False)};
</script>
"""


# ── Build the patched script.js ───────────────────────────────────────────────
# Replace every fetch("/api/...") with a function that reads from __PORTAL_DATA__.
patched_js = """
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
document.addEventListener("DOMContentLoaded", () => {
  loadDashboardStats();
  loadCustomers();
  safeRun(loadHealthScores);
  safeRun(loadChurnAlerts);
  safeRun(loadWeeklyReport);
  initChat();
  initFadeUpObserver();
  initActiveNavHighlight();
  loadChurnAlerts();
  loadWeeklyReport();
  loadDashboardCharts();
  loadWeeklyActiveUsers();
});

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
  if (!container) return;
  container.innerHTML = "";
  if (extra) extra.innerHTML = "";
  const first = customers.slice(0, 3);
  const rest = customers.slice(3);
  first.forEach(c => { container.innerHTML += buildCustomerCard(c); });
  if (rest.length > 0 && extra) {
    rest.forEach(c => { extra.innerHTML += buildCustomerCard(c); });
    if (btnWrap) btnWrap.style.display = "flex";
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
function expandCustomers() {
  const extra = document.getElementById("customersExtra");
  const btnWrap = document.getElementById("viewAllWrap");
  if (extra) {
    extra.style.display = "grid";
    Array.from(extra.children).forEach((card, i) => {
      card.style.opacity = "0"; card.style.transform = "translateY(20px)";
      card.style.transition = "opacity 0.4s ease, transform 0.4s ease";
      setTimeout(() => { card.style.opacity = "1"; card.style.transform = "translateY(0)"; }, i * 80);
    });
  }
  if (btnWrap) btnWrap.style.display = "none";
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

  // Reload the page with ?q= so Streamlit Python computes the answer
  const url = new URL(window.location.href);
  url.searchParams.set("q", q);
  window.location.href = url.toString();
  // The typing indicator will be replaced by the reload result
  removeTyping(typingId);
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

/* ---------- fade-up animation ---------- */
function initFadeUpObserver() {
  const fadeEls = document.querySelectorAll(".fade-up");
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add("visible"); });
  }, { threshold: 0.1 });
  fadeEls.forEach(el => observer.observe(el));
}

/* ---------- dashboard charts ---------- */
function loadDashboardCharts() {
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
"""


# ── Assemble final HTML ───────────────────────────────────────────────────────
raw_html   = HTML_PATH.read_text(encoding="utf-8")
css_text   = CSS_PATH.read_text(encoding="utf-8")
js_escaped = patched_js  # already a plain string

# 1. Replace Jinja url_for() references with inline assets
# The HTML uses single-quoted Jinja inside double-quoted HTML attrs, so we
# match the exact rendered strings from the template file.
final_html = raw_html.replace(
    """<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">""",
    f"<style>\n{css_text}\n</style>",
).replace(
    """<script src="{{ url_for('static', filename='script.js') }}"></script>""",
    f"{injected_data_script}\n<script>\n{js_escaped}\n</script>",
)

# Fallback: if the replacements above didn't match exactly, inject before </body>
if "window.__PORTAL_DATA__" not in final_html:
    final_html = final_html.replace(
        "</body>",
        f"{injected_data_script}\n<script>\n{js_escaped}\n</script>\n</body>",
        1,
    )


# ── Render ────────────────────────────────────────────────────────────────────
components.html(final_html, height=6000, scrolling=True)
