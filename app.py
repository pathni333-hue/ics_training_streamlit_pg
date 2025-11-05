import streamlit as st
from db_pg import init_db, login_user, register_user, save_progress, get_user_progress
from report import generate_report_pdf
import modules.segmentation as segmentation
import modules.asset_lab as asset_lab
import modules.risk_workshop as risk_workshop
import modules.threat_mapping as threat_mapping
import modules.incident_response as incident_response
import modules.hygiene_dashboard as hygiene_dashboard

import tempfile, os

st.set_page_config(page_title="OT/ICS Training Platform (PGSQL)", layout="wide")
init_db()

# --- LOGIN / REGISTER ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

if st.session_state['user'] is None:
    tab1, tab2 = st.tabs(["🔐 Login", "🆕 Register"])
    with tab1:
        st.subheader("Login")
        user = st.text_input("Username", key="login_user")
        pw = st.text_input("Password", type="password", key="login_pw")
        if st.button("Login"):
            if login_user(user, pw):
                st.session_state['user'] = user
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")
    with tab2:
        st.subheader("Register")
        user = st.text_input("New username", key="reg_user")
        pw = st.text_input("New password", type="password", key="reg_pw")
        if st.button("Register"):
            if register_user(user, pw):
                st.success("Registered! Please login.")
            else:
                st.warning("Username already exists.")
    st.stop()

# --- MAIN APP ---
st.sidebar.markdown(f"👋 **User:** {st.session_state['user']}")
if st.sidebar.button("Log out"):
    st.session_state['user'] = None
    st.experimental_rerun()

MODULES = {
    "1 - Network Segmentation Trainer": segmentation,
    "2 - Asset Discovery & Classification Lab": asset_lab,
    "3 - OT Risk Scoring Workshop": risk_workshop,
    "4 - Threat-to-Mitigation Mapping Challenge": threat_mapping,
    "5 - OT Incident Response Simulation": incident_response,
    "6 - OT Cyber Hygiene Assessment Dashboard": hygiene_dashboard
}

choice = st.sidebar.radio("Choose module", list(MODULES.keys()))
module = MODULES[choice]

st.title("OT / ICS Interactive Training Platform (PostgreSQL Edition)")

# run selected module
score, details = module.app()

if score is not None:
    save_progress(st.session_state['user'], choice, score, details)

st.sidebar.markdown("---")
if st.sidebar.button("📊 View My Progress"):
    df = get_user_progress(st.session_state['user'])
    st.sidebar.dataframe(df)

if st.sidebar.button("📄 Download My Report (PDF)"):
    df = get_user_progress(st.session_state['user'])
    path = generate_report_pdf(st.session_state['user'], df)
    with open(path, "rb") as f:
        st.sidebar.download_button("Download PDF", f, file_name="training_report.pdf")
