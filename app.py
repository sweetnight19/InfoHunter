import streamlit as st
import os
from osint import domain_analyzer, email_analyzer, username_analyzer, report_generator
from dotenv import load_dotenv, find_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv(find_dotenv())

# --- Configuración de la página ---
st.set_page_config(
    page_title="InfoHunter OSINT Dashboard",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Logo y cabecera ---
st.markdown(
    """
    <div style='display: flex; align-items: center;'>
        <img src='https://img.icons8.com/ios-filled/100/ffffff/hacker.png' width='60' style='margin-right: 20px;'>
        <div>
            <h1 style='margin-bottom: 0;'>InfoHunter <span style='font-size:0.7em;'>OSINT Dashboard</span></h1>
            <p style='margin-top: 0; color: #888;'>Herramienta de análisis OSINT para dominios, emails y usuarios</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
tab1, tab2, tab3 = st.tabs(["Análisis OSINT", "Editar .env", "Reportes generados"])

with tab1:
    st.markdown("## Análisis OSINT")
    col1, col2 = st.columns([2, 3])
    with col1:
        st.markdown("### Selecciona el tipo de análisis")
        option = st.selectbox(
            "¿Qué quieres analizar?",
            ["Dominio", "Email", "Usuario"],
            index=0,
            key="selectbox_tipo_analisis_tab1",
        )
        input_value = st.text_input(
            f"Introduce el {option.lower()} a analizar:",
            key="input_valor_analisis_tab1",
        )
        analizar = st.button(
            "🔍 Buscar", use_container_width=True, key="btn_buscar_tab1"
        )
    with col2:
        st.markdown("### Resultado del análisis")
        if "result" not in st.session_state:
            st.session_state["result"] = None
        if analizar and input_value:
            with st.spinner("Analizando, por favor espera..."):
                try:
                    if option == "Dominio":
                        result = domain_analyzer.analyze(input_value)
                    elif option == "Email":
                        result = email_analyzer.analyze(input_value)
                    elif option == "Usuario":
                        result = username_analyzer.analyze(input_value)
                    st.session_state["result"] = result
                    st.success("¡Análisis completado!")
                except Exception as e:
                    st.session_state["result"] = None
                    st.error(f"Error durante el análisis: {e}")
        if st.session_state["result"]:
            # Mostrar el resultado de forma bonita
            if option == "Dominio":
                report_generator.show_results_domain(
                    st.session_state["result"], input_value
                )
            elif option == "Email":
                report_generator.show_results_email(
                    st.session_state["result"], input_value
                )
            elif option == "Usuario":
                report_generator.show_results_username(
                    st.session_state["result"], input_value
                )
            else:
                if isinstance(st.session_state["result"], dict):
                    for k, v in st.session_state["result"].items():
                        st.metric(label=k, value=str(v))
                else:
                    st.write(st.session_state["result"])
        elif analizar and not input_value:
            st.warning("Por favor, introduce un valor para analizar.")

with tab2:
    st.markdown("## Editor de archivo .env 📝")
    env_path = os.path.join(os.getcwd(), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            env_content = f.read()
    else:
        env_content = ""
    with st.form(key="env_editor_form"):
        new_env_content = st.text_area("Contenido de .env", env_content, height=300)
        save_env = st.form_submit_button("Guardar cambios")
        if save_env:
            try:
                with open(env_path, "w", encoding="utf-8") as f:
                    f.write(new_env_content)
                st.success("Archivo .env guardado correctamente.")
            except Exception as e:
                st.error(f"Error al guardar .env: {e}")
            except Exception as e:
                st.error(f"Error al guardar .env: {e}")

with tab3:
    st.markdown("## Reportes generados 🗂️")
    reports_dir = "reports"
    update_reports = st.button(
        "🔄 Actualizar lista de reportes", key="update_reports_btn"
    )
    if update_reports:
        st.rerun()
    if os.path.exists(reports_dir):
        pdfs = [f for f in os.listdir(reports_dir) if f.endswith(".pdf")]
        if pdfs:
            for pdf in pdfs:
                col_dl, col_del = st.columns([6, 1])
                with col_dl:
                    st.download_button(
                        label=f"Descargar {pdf}",
                        data=open(os.path.join(reports_dir, pdf), "rb").read(),
                        file_name=pdf,
                        mime="application/pdf",
                        key=f"tab_dl_{pdf}",
                    )
                with col_del:
                    delete = st.button(
                        "❌", key=f"tab_del_{pdf}", help=f"Eliminar {pdf}"
                    )
                    if delete:
                        try:
                            os.remove(os.path.join(reports_dir, pdf))
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error al eliminar {pdf}: {e}")
        else:
            st.info("No hay reportes PDF generados.")
    else:
        st.info("No existe la carpeta de reportes.")

# --- Footer ---
st.markdown(
    """
<hr style='margin-top:40px;margin-bottom:10px;'>
<div style='text-align:center;color:#888;'>
    &copy; 2025 InfoHunter | Proyecto OSINT educativo
</div>
""",
    unsafe_allow_html=True,
)
