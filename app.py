from pathlib import Path
import os

import streamlit as st
from dotenv import find_dotenv, load_dotenv

from osint import domain_analyzer, email_analyzer, report_generator, username_analyzer


load_dotenv(find_dotenv())
ROOT_DIR = Path(__file__).resolve().parent
REPORTS_DIR = ROOT_DIR / "reports"

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
      [data-testid="stMetric"] {background: #f5f7fb; border: 1px solid #e6eaf2;
        padding: 1rem 1.1rem; border-radius: .8rem;}
      h1 {letter-spacing: -.03em;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🕵️ InfoHunter")
st.caption("Análisis OSINT local para dominios, emails y nombres de usuario.")
tab_analysis, tab_config, tab_reports = st.tabs(
    ["🔎 Análisis", "🔐 Configuración", "📄 Informes"]
)

ANALYZERS = {
    "Dominio": domain_analyzer.analyze,
    "Email": email_analyzer.analyze,
    "Usuario": username_analyzer.analyze,
}


def _create_pdf(kind: str, target: str, result: dict) -> str:
    if kind == "Usuario":
        return report_generator.generate_osint_pdf_username(
            target,
            result.get("sherlock_profiles", []),
            result.get("maigret_profiles", []),
            output_dir=str(REPORTS_DIR),
        )
    if kind == "Email":
        return report_generator.generate_osint_pdf_email(
            target,
            result.get("hibp", {}),
            result.get("breachdirectory", {}),
            result.get("holehe", []),
            result.get("intelx", {}),
            output_dir=str(REPORTS_DIR),
        )
    return report_generator.generate_osint_pdf_domain(
        target,
        result.get("whois", {}),
        result.get("dns", {}),
        result.get("subdomains_sublist3r", []),
        result.get("subdomains_crtsh", []),
        result.get("hunter", {}),
        result.get("theharvester", {}),
        result.get("wayback", []),
        result.get("shodan", {}),
        result.get("virustotal", {}),
        output_dir=str(REPORTS_DIR),
    )


with tab_analysis:
    st.subheader("Nuevo análisis")
    with st.form("analysis_form"):
        left, right = st.columns([1, 2])
        with left:
            kind = st.selectbox("Tipo de búsqueda", list(ANALYZERS), key="analysis_kind")
        with right:
            target = st.text_input(
                "Dominio, email o usuario",
                placeholder="example.com, persona@example.com o username",
                key="analysis_target",
            )
        submitted = st.form_submit_button("🔍 Analizar", type="primary")

    if submitted:
        normalized_target = target.strip()
        if not normalized_target:
            st.warning("Introduce un valor para analizar.")
            st.session_state.pop("analysis_result", None)
            st.session_state.pop("generated_pdf", None)
        else:
            try:
                with st.spinner("Consultando las fuentes configuradas…"):
                    result = ANALYZERS[kind](normalized_target)
                st.session_state["analysis_result"] = {
                    "kind": kind,
                    "target": normalized_target,
                    "result": result,
                }
                st.session_state.pop("generated_pdf", None)
            except Exception as error:
                st.session_state.pop("analysis_result", None)
                st.session_state.pop("generated_pdf", None)
                st.error(
                    f"El análisis falló ({type(error).__name__}). "
                    "Revisa la configuración de fuentes y la salida del terminal."
                )

    saved = st.session_state.get("analysis_result")
    normalized_target = target.strip()
    matches_current_input = (
        saved is not None
        and saved.get("kind") == kind
        and saved.get("target") == normalized_target
    )

    if matches_current_input:
        st.markdown("### Resultado")
        st.json(saved["result"], expanded=False)
        if st.button("Crear informe PDF local", key="create_pdf"):
            try:
                pdf_path = _create_pdf(kind, normalized_target, saved["result"])
                st.session_state["generated_pdf"] = {
                    "analysis_key": (kind, normalized_target),
                    "path": pdf_path,
                }
                st.success("Informe generado.")
            except Exception as error:
                st.error(f"No se pudo generar el informe ({type(error).__name__}).")

        generated_pdf = st.session_state.get("generated_pdf")
        if (
            generated_pdf
            and generated_pdf.get("analysis_key") == (kind, normalized_target)
            and Path(generated_pdf["path"]).is_file()
        ):
            pdf_path = Path(generated_pdf["path"])
            st.download_button(
                "Descargar informe PDF",
                data=pdf_path.read_bytes(),
                file_name=pdf_path.name,
                mime="application/pdf",
                key="download_current_pdf",
            )
    elif saved:
        st.info(
            f"El resultado anterior corresponde a {saved['kind']}: "
            f"{saved['target']}. Pulsa «Analizar» para ejecutar la búsqueda actual."
        )
    else:
        st.info("Los resultados aparecerán aquí después de ejecutar un análisis.")


with tab_config:
    st.subheader("Configuración de fuentes")
    st.write(
        "Las claves se leen desde el entorno o desde un archivo .env local. "
        "Esta pantalla solo muestra si cada clave está presente; no revela ni edita secretos."
    )
    api_keys = {
        "HIBP_API_KEY": "Have I Been Pwned",
        "BREACHDIRECTORY_API_KEY": "BreachDirectory",
        "INTELX_KEY": "Intelligence X",
        "SHODAN_API_KEY": "Shodan",
        "VT_API_KEY": "VirusTotal",
        "HUNTER_API_KEY": "Hunter.io",
    }
    for key, service in api_keys.items():
        configured = bool(os.getenv(key))
        st.write(
            f"{'✅' if configured else '○'} **{service}** — "
            f"{'configurada' if configured else 'no configurada'}"
        )
    st.caption(
        "Las fuentes que no tengan clave devolverán su propio aviso; las demás "
        "seguirán ejecutándose. Reinicia la app después de cambiar el archivo .env."
    )


with tab_reports:
    st.subheader("Informes locales")
    st.caption("Los PDFs se guardan en la carpeta reports del proyecto.")
    if not REPORTS_DIR.exists():
        st.info("Todavía no hay informes generados.")
    else:
        pdfs = sorted(
            (
                path for path in REPORTS_DIR.glob("*.pdf")
                if path.is_file() and not path.is_symlink()
            ),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
        if not pdfs:
            st.info("Todavía no hay informes PDF.")
        for pdf_path in pdfs:
            with st.container(border=True):
                col_name, col_download, col_delete = st.columns([4, 1, 1])
                col_name.write(pdf_path.name)
                col_download.download_button(
                    "Descargar",
                    data=pdf_path.read_bytes(),
                    file_name=pdf_path.name,
                    mime="application/pdf",
                    key=f"download_{pdf_path.name}",
                    use_container_width=True,
                )
                if col_delete.button(
                    "Eliminar",
                    key=f"delete_{pdf_path.name}",
                    use_container_width=True,
                ):
                    try:
                        resolved_path = pdf_path.resolve(strict=True)
                        if resolved_path.parent != REPORTS_DIR.resolve() or pdf_path.is_symlink():
                            raise ValueError("Ruta del informe no válida.")
                        resolved_path.unlink()
                        st.rerun()
                    except (OSError, ValueError) as error:
                        st.error(f"No se pudo eliminar el informe ({type(error).__name__}).")

st.divider()
st.caption("InfoHunter · Usa estas herramientas solo con autorización y respeta la privacidad.")
