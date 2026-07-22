"""
streamlit_app.py — Streamlit entry point for the AI Customer Portal.

Strategy
--------
The original Flask app served one HTML page and answered /api/* calls
from the browser.  Streamlit cannot run Flask routes, so we:

1. Load the raw HTML template once.
2. Replace the two Jinja2 url_for() calls with inline <style> and <script> blocks.
3. Run every "API" function in pure Python (same logic as the old Flask routes),
   all defined in backend/portal_api.py and backend/auth.py.
4. Embed the computed data as a JSON blob inside the page so script.js can
   read it WITHOUT making any fetch() calls.
5. Serve the final HTML string via st.components.v1.html().

No design changes are made — every class, colour, animation and layout
from the original index.html / style.css / script.js is preserved.
"""

import json
import pathlib
import streamlit as st
import streamlit.components.v1 as components

from backend.auth import init_app_tables, check_login, register_user
from backend.portal_api import (
    api_dashboard, api_customers, api_health, api_churn,
    api_weekly_report, api_dashboard_charts, api_weekly_active_users, api_query,
    list_customer_names, get_customer, add_customer, update_customer, delete_customer,
    submit_feedback, recent_complaints, get_at_risk_customers, get_all_customers_df,
)

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
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# AUTH + COMPLAINTS SETUP  (logic lives in backend/auth.py)
# ══════════════════════════════════════════════════════════════════════════════
init_app_tables(DB_PATH)


# ══════════════════════════════════════════════════════════════════════════════
# HTML ASSEMBLY — shared by both the public page and the logged-in portal
# ══════════════════════════════════════════════════════════════════════════════
_raw_html   = HTML_PATH.read_text(encoding="utf-8")
_css_text   = CSS_PATH.read_text(encoding="utf-8")
_js_escaped = JS_PATH.read_text(encoding="utf-8")

TOP_BAR_HEIGHT = 80  # px — matches the custom navbar's own height inside the iframe


def build_portal_html(data_blob: dict, extra_css: str = "") -> str:
    """Inject a data blob + script.js into the original index.html template,
    returning one self-contained HTML string ready for components.html().
    `extra_css` is appended after the template's own stylesheet (used to
    hide sections on the public page)."""
    injected_data_script = f"""
<script>
window.__PORTAL_DATA__ = {json.dumps(data_blob, ensure_ascii=False)};
</script>
"""
    style_block = f"<style>\n{_css_text}\n{extra_css}\n</style>"
    html = _raw_html.replace(
        """<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">""",
        style_block,
    ).replace(
        """<script src="{{ url_for('static', filename='script.js') }}"></script>""",
        f"{injected_data_script}\n<script>\n{_js_escaped}\n</script>",
    )
    if "window.__PORTAL_DATA__" not in html:
        html = html.replace(
            "</body>",
            f"{injected_data_script}\n<script>\n{_js_escaped}\n</script>\n</body>",
            1,
        )
    return html


def overlay_css(show_sidebar_arrow: bool) -> str:
    """CSS that hides Streamlit chrome, stretches the iframe to the full
    viewport, and floats the native Login/Account bar over the custom
    navbar's own row, right-aligned.

    NOTE on technique: NOT position:fixed — Streamlit nests every element
    inside divs that use CSS transforms internally, which breaks fixed
    positioning (it silently anchors to that ancestor instead of the real
    browser viewport). NOT flexbox-in-normal-flow either — Streamlit's
    st.container(key=...) class can land on an inner wrapper rather than
    the outer element (a known Streamlit quirk), so a flex row built on
    that class doesn't reliably span the full width, which is why the
    button previously drifted to the middle instead of the right edge.
    What actually works: make .block-container itself `position: relative`,
    then give the overlay `position: absolute; top; right`. That resolves
    relative to .block-container regardless of which exact div gets the
    st-key class, since position:absolute always walks up to the nearest
    positioned ancestor.
    """
    sidebar_css = (
        '[data-testid="stSidebarCollapsedControl"] { visibility: visible !important; display: block !important; }'
        if show_sidebar_arrow else
        '[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] { display: none; }'
    )
    return f"""
    <style>
    #MainMenu, header, footer {{ visibility: hidden; }}
    {sidebar_css}
    .block-container {{
        position: relative !important;
        padding: 0 !important;
        max-width: 100% !important;
    }}
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
        overflow: hidden !important;
        height: 100vh !important;
    }}
    .block-container iframe, [data-testid="element-container"] iframe, iframe {{
        height: 100vh !important;
        min-height: 100vh !important;
        width: 100% !important;
        display: block;
        border: none;
    }}
    /* Anchored to the top-right corner of .block-container, floating on top
       of the iframe below it. pointer-events:none on the bar itself lets
       clicks pass THROUGH to the navbar's own links underneath everywhere
       except the button, which re-enables pointer events just for itself. */
    div.st-key-auth_overlay {{
        position: absolute !important;
        top: 0 !important;
        right: 32px !important;
        left: auto !important;
        width: auto !important;
        z-index: 1000;
        height: {TOP_BAR_HEIGHT}px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        pointer-events: none;
    }}
    div.st-key-auth_overlay > div {{ margin: 0 !important; }}
    div.st-key-auth_overlay * {{ pointer-events: auto; }}
    div.st-key-auth_overlay button {{ border-radius: 8px !important; }}
    </style>
"""


# Empty/zeroed data for the PUBLIC (logged-out) page — real customer data
# must never be embedded in the page source before login, since hiding a
# section with CSS does not stop it being read via view-source / devtools.
PUBLIC_DATA_BLOB = {
    "dashboard": {"total": 0, "healthy": 0, "warning": 0, "high_risk": 0, "retention_status": "Unknown"},
    "customers": [],
    "health": [],
    "churn": [],
    "weeklyReport": {"summary": "", "active_users": 0, "mrr_growth": 0, "churn_risk_change": 0, "accounts_saved": 0},
    "dashboardCharts": {"customer_growth": {"labels": [], "new": [], "retained": []},
                        "segments": {"labels": [], "values": []}},
    "weeklyActiveUsers": {"labels": [], "values": []},
    "queryAnswer": "",
    "queryParam": "",
    "loggedIn": False,
    "username": "",
    "role": "",
}

# Hide the internal nav links and every data-driven section on the public
# page — only the marketing sections (hero / features / insights) and the
# footer stay visible. Combined with PUBLIC_DATA_BLOB having no real data at
# all, there's nothing sensitive to see even via devtools.
PUBLIC_SECTION_CSS = """
.nav-links { display: none !important; }
#dashboard, #healthscore, #customers, #churnprediction, #aiquery, #weeklyreport {
    display: none !important;
}
.login-badge { display: none !important; }
"""


# ══════════════════════════════════════════════════════════════════════════════
# ROUTING: logout → auth page → public page → logged-in mode
# ══════════════════════════════════════════════════════════════════════════════

# Handle logout FIRST, before anything else renders.
if st.query_params.get("logout") == "1" and "user" in st.session_state:
    del st.session_state["user"]
    st.query_params.clear()
    st.rerun()

logged_in = "user" in st.session_state

# ── Auth page (Login / Register) — reached via the navbar Login button ────────
if st.query_params.get("auth") == "login" and not logged_in:
    st.markdown(
        """
        <style>
        #MainMenu, header, footer { visibility: hidden; }
        [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] { display: none; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("## 🤖 AI Customer Management Portal")
        tab_login, tab_register = st.tabs(["🔑 Login", "🆕 Register"])

        with tab_login:
            with st.form("login_form"):
                u = st.text_input("Username")
                p = st.text_input("Password", type="password")
                if st.form_submit_button("Sign in", use_container_width=True):
                    role = check_login(u, p, DB_PATH)
                    if role:
                        st.session_state.user = {"username": u.strip(), "role": role}
                        st.query_params.clear()
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")
            st.caption("Demo accounts — admin / admin123 · viewer / viewer123")

        with tab_register:
            with st.form("register_form"):
                nu  = st.text_input("Choose a username")
                np1 = st.text_input("Choose a password", type="password")
                np2 = st.text_input("Confirm password", type="password")
                if st.form_submit_button("Create account", use_container_width=True):
                    success, message = register_user(nu, np1, np2, DB_PATH)
                    (st.success if success else st.error)(message)

        if st.button("← Back to home", use_container_width=True):
            st.query_params.clear()
            st.rerun()
    st.stop()

# ── Public (logged-out) page: the real custom-designed landing page, minus
#    the internal nav links and every data-driven section — those need a
#    login. Only marketing sections (hero/features/insights) + footer show. ──
if not logged_in:
    st.markdown(overlay_css(show_sidebar_arrow=False), unsafe_allow_html=True)

    with st.container(key="auth_overlay"):
        if st.button("🔑  Login", key="gate_login_btn"):
            st.query_params["auth"] = "login"
            st.rerun()

    public_html = build_portal_html(PUBLIC_DATA_BLOB, extra_css=PUBLIC_SECTION_CSS)
    components.html(public_html, height=800, scrolling=True)
    st.stop()

# ── Logged-in mode: real data, sidebar, full features ─────────────────────────
USER = st.session_state.user
IS_ADMIN = USER["role"] == "admin"

with st.sidebar:
    st.markdown(f"**👤 {USER['username']}**  \n`{USER['role']}`")
    st.divider()

    _at_risk = get_at_risk_customers(DB_PATH)
    if _at_risk:
        st.markdown("**🚨 Health alerts**")
        for name, health_score in _at_risk:
            st.error(f"{name} — health {health_score}/100", icon="⚠️")
        st.divider()

    _pages = ["📊 Portal", "📋 All Customer Data", "📝 Customer Feedback"]
    if IS_ADMIN:
        _pages.insert(1, "👥 Manage Customers")
    page = st.radio("Navigate", _pages, label_visibility="collapsed")
    st.divider()
    if st.button("Log out", use_container_width=True):
        del st.session_state.user
        st.query_params.clear()
        st.rerun()

# The portal's "Show All Customer Data" button navigates here via ?view=customers
if st.query_params.get("view") == "customers":
    page = "📋 All Customer Data"

# ── Chat query via Streamlit state ───────────────────────────────────────────
query_param = st.query_params.get("q", "")
query_answer = ""
if query_param:
    query_answer = api_query(query_param, DB_PATH)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE ROUTER
# ══════════════════════════════════════════════════════════════════════════════

if page == "📊 Portal":
    data_blob = {
        "dashboard":        api_dashboard(DB_PATH),
        "customers":        api_customers(DB_PATH),
        "health":           api_health(DB_PATH),
        "churn":            api_churn(DB_PATH),
        "weeklyReport":     api_weekly_report(CSV_PATH),
        "dashboardCharts":  api_dashboard_charts(CSV_PATH),
        "weeklyActiveUsers": api_weekly_active_users(CSV_PATH),
        "queryAnswer":      query_answer,
        "queryParam":       query_param,
        "loggedIn":         True,
        "username":         USER["username"],
        "role":             USER["role"],
    }
    final_html = build_portal_html(data_blob)

    st.markdown(overlay_css(show_sidebar_arrow=True), unsafe_allow_html=True)

    # Native top bar — sits directly above the iframe, same dark background,
    # right-aligned to land visually next to "Weekly Report" at the far right
    # of the navbar row. These widgets are OUTSIDE the iframe, so — unlike
    # anything in final_html — they can freely change session_state and rerun.
    with st.container(key="auth_overlay"):
        with st.popover(f"👤 {USER['username']}"):
            st.caption(f"Signed in as **{USER['username']}** · role: `{USER['role']}`")
            if st.button("🚪  Log out", key="portal_logout_btn", use_container_width=True):
                del st.session_state["user"]
                st.query_params.clear()
                st.rerun()

    # The custom-designed dashboard, rendered inside a full-viewport iframe.
    components.html(final_html, height=800, scrolling=True)

    # "Show All Customer Data" — kept as a normal (non-floating) button right
    # under the portal, always visible without needing to scroll the iframe.
    _, mid_col, _ = st.columns([1, 1, 1])
    with mid_col:
        if st.button("📋  Show All Customer Data", key="portal_viewall_btn", use_container_width=True):
            st.query_params["view"] = "customers"
            st.rerun()


elif page == "📋 All Customer Data":
    st.title("📋 All Customer Data")
    col_a, col_b = st.columns([3, 1])
    search = col_a.text_input("🔍 Search by company name", placeholder="Type to filter...")
    if col_b.button("← Back to Portal", use_container_width=True):
        st.query_params.clear()
        st.rerun()

    df = get_all_customers_df(DB_PATH)

    if search.strip():
        df = df[df["company_name"].str.contains(search.strip(), case=False, na=False)]

    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption(f"{len(df)} customer{'s' if len(df) != 1 else ''} shown · sorted by NPS (lowest first)")


elif page == "👥 Manage Customers":
    st.title("👥 Manage Customers")
    st.caption("Admin only — changes are saved to the database and appear on the Portal immediately.")

    REGIONS = ["North", "South", "East", "West"]
    TIERS   = ["Basic", "Standard", "Premium", "Enterprise"]
    USAGE   = ["Low", "Medium", "High"]

    tab_add, tab_edit, tab_delete = st.tabs(["➕ Add customer", "✏️ Edit customer", "🗑️ Delete customer"])

    all_names = list_customer_names(DB_PATH)

    with tab_add:
        with st.form("add_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            name   = c1.text_input("Company name")
            region = c2.selectbox("Region", REGIONS)
            tier   = c1.selectbox("Plan tier", TIERS)
            usage  = c2.selectbox("Monthly usage", USAGE)
            devices = c1.number_input("Devices count", 0, 10000, 1)
            tickets = c2.number_input("Support tickets", 0, 1000, 0)
            nps     = st.slider("NPS score (0 = very unhappy · 10 = very happy)", 0, 10, 7)
            d1, d2, d3 = st.columns(3)
            signup  = d1.date_input("Signup date")
            active  = d2.date_input("Last active date")
            expiry  = d3.date_input("Contract expiry")
            if st.form_submit_button("Add customer", use_container_width=True):
                success, message = add_customer(
                    DB_PATH, name=name, region=region, tier=tier, usage=usage,
                    devices=devices, tickets=tickets, nps=nps,
                    signup=signup, active=active, expiry=expiry,
                )
                (st.success if success else st.error)(message)

    with tab_edit:
        if not all_names:
            st.info("No customers yet.")
        else:
            target = st.selectbox("Choose customer to edit", all_names, key="edit_pick")
            row = get_customer(DB_PATH, target)
            if row:
                with st.form("edit_form"):
                    c1, c2 = st.columns(2)
                    region = c1.selectbox("Region", REGIONS,
                                          index=REGIONS.index(row["region"]) if row["region"] in REGIONS else 0)
                    tier   = c2.selectbox("Plan tier", TIERS,
                                          index=TIERS.index(row["plan_tier"]) if row["plan_tier"] in TIERS else 0)
                    usage  = c1.selectbox("Monthly usage", USAGE,
                                          index=USAGE.index(row["monthly_usage"]) if row["monthly_usage"] in USAGE else 0)
                    tickets = c2.number_input("Support tickets", 0, 1000, int(row["support_tickets"]))
                    nps     = st.slider("NPS score", 0, 10, int(row["nps_score"]))
                    if st.form_submit_button("Save changes", use_container_width=True):
                        success, message = update_customer(
                            DB_PATH, company_name=target, region=region, tier=tier,
                            usage=usage, tickets=tickets, nps=nps,
                        )
                        (st.success if success else st.error)(message)

    with tab_delete:
        if not all_names:
            st.info("No customers yet.")
        else:
            target = st.selectbox("Choose customer to delete", all_names, key="del_pick")
            confirm = st.checkbox(f"Yes, permanently delete **{target}**")
            if st.button("Delete customer", type="primary", disabled=not confirm):
                success, message = delete_customer(DB_PATH, target)
                st.success(message)
                st.rerun()


elif page == "📝 Customer Feedback":
    st.title("📝 Customer Feedback & Complaints")
    st.caption(
        "This is the channel where customer complaints ENTER the system. In a real company this form "
        "would live on your public website or helpdesk — each submission raises the customer's ticket "
        "count and updates their NPS, which drives the health score and churn prediction on the Portal."
    )

    all_names = list_customer_names(DB_PATH)

    if not all_names:
        st.info("No customers in the database yet.")
    else:
        with st.form("feedback_form", clear_on_submit=True):
            company = st.selectbox("Which company are you from?", all_names)
            message = st.text_area("Describe your issue or feedback", height=120,
                                   placeholder="e.g. The dashboard export feature keeps failing...")
            rating  = st.slider("How likely are you to recommend us? (NPS)", 0, 10, 5)
            if st.form_submit_button("Submit feedback", use_container_width=True):
                if not message.strip():
                    st.error("Please describe the issue.")
                else:
                    result_message = submit_feedback(
                        DB_PATH, company_name=company, message=message, rating=rating
                    )
                    st.success(result_message)

        st.divider()
        st.subheader("Recent submissions")
        recents = recent_complaints(DB_PATH, limit=10)
        if not recents:
            st.caption("No complaints submitted yet.")
        for r in recents:
            emoji = "😡" if (r["rating"] or 0) < 5 else "😐" if (r["rating"] or 0) < 8 else "😊"
            st.markdown(
                f"{emoji} **{r['company_name']}** · NPS {r['rating']}/10 · {r['created_at']}  \n"
                f"> {r['message']}"
            )