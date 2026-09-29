import streamlit as st
from dotenv import find_dotenv, load_dotenv

from dashboard import (
    render_analysis_tab,
    render_configuration_tab,
    render_reports_tab,
)


load_dotenv(find_dotenv())

st.set_page_config(
    page_title="InfoHunter OSINT Dashboard",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      .block-container {max-width: 1450px; padding-top: 2rem; padding-bottom: 3rem;}
      [data-testid="stMetric"] {
        background: var(--secondary-background-color);
        border: 1px solid var(--border-color);
        padding: .9rem 1rem;
        border-radius: .8rem;
      }
      h1 {letter-spacing: -.03em;}
      @media (max-width: 640px) {
        .block-container {padding: 1rem .8rem 2rem;}
        [data-testid="stMetric"] {padding: .7rem;}
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🕵️ InfoHunter")
st.caption("Análisis OSINT local para dominios, emails y nombres de usuario.")
st.info(
    "Esta interfaz no incluye autenticación: mantenla en localhost y no la expongas "
    "a Internet o a redes compartidas."
)

tab_analysis, tab_config, tab_reports = st.tabs(
    ["🔎 Análisis", "🔐 Configuración", "📄 Informes"]
)
with tab_analysis:
    render_analysis_tab()
with tab_config:
    render_configuration_tab()
with tab_reports:
    render_reports_tab()

st.divider()
st.caption("InfoHunter · Usa estas herramientas solo con autorización y respeta la privacidad.")
