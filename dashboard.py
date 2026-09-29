"""Streamlit dashboard sections for InfoHunter."""

from datetime import datetime
from pathlib import Path
import time

import streamlit as st

from osint.config import Settings
from osint.results import SourceResult
from osint import domain_analyzer, email_analyzer, report_generator, username_analyzer
from osint.input_validation import validate_target
from osint.result_status import source_status
from osint.tool_status import harvester_key_file_status, optional_tool_status


ROOT_DIR = Path(__file__).resolve().parent
REPORTS_DIR = ROOT_DIR / "reports"

ANALYZERS = {
    "Dominio": domain_analyzer.analyze,
    "Email": email_analyzer.analyze,
    "Usuario": username_analyzer.analyze,
}
SOURCE_OPTIONS = {
    "Dominio": [
        "whois", "dns", "subdomains_sublist3r", "subdomains_crtsh",
        "hunter", "theharvester", "wayback", "shodan", "virustotal",
    ],
    "Email": ["hibp", "breachdirectory", "holehe", "intelx"],
    "Usuario": ["sherlock_profiles", "maigret_profiles"],
}
METADATA_KEYS = {"email", "username", "domain"}


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


def _render_source_details(source: str, value) -> None:
    status = source_status(value)
    if isinstance(value, SourceResult):
        value = value.to_legacy()
    has_problem = status in {"Error", "Parcial", "Falta configuración", "Herramienta no instalada"}
    with st.expander(f"{'⚠️ ' if has_problem else ''}{source} · {status}", expanded=has_problem):
        if isinstance(value, (list, tuple)) and all(isinstance(item, str) for item in value):
            if value:
                st.dataframe(
                    {"Resultado": list(value)},
                    hide_index=True,
                    use_container_width=True,
                    column_config={
                        "Resultado": st.column_config.LinkColumn(
                            "Resultado", display_text="Abrir"
                        )
                    } if all(item.startswith(("https://", "http://")) for item in value) else None,
                )
            else:
                st.caption("La fuente terminó sin resultados.")
        elif isinstance(value, dict):
            st.json(value, expanded=False)
        else:
            st.write(value)


def render_analysis_tab() -> None:
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
        selected_sources = st.multiselect(
            "Fuentes",
            options=SOURCE_OPTIONS[kind],
            default=SOURCE_OPTIONS[kind],
            key=f"analysis_sources_{kind}",
            help="Solo se consultarán las fuentes seleccionadas.",
        )
        submitted = st.form_submit_button("🔍 Analizar", type="primary")

    if submitted:
        try:
            normalized_target = validate_target(kind, target)
        except ValueError as error:
            st.warning(str(error))
            st.session_state.pop("analysis_result", None)
            st.session_state.pop("generated_pdf", None)
        else:
            if not selected_sources:
                st.warning("Selecciona al menos una fuente.")
                st.session_state.pop("analysis_result", None)
                st.session_state.pop("generated_pdf", None)
            else:
                try:
                    started_at = datetime.now().astimezone()
                    started_clock = time.perf_counter()
                    with st.status("Consultando las fuentes seleccionadas…", expanded=True) as progress:
                        def on_source_done(source, value):
                            state = source_status(value)
                            icon = "✅" if state.startswith("Completado") else "⚠️"
                            progress.write(f"{icon} **{source}** — {state}")

                        result = ANALYZERS[kind](
                            normalized_target,
                            selected_sources=selected_sources,
                            progress_callback=on_source_done,
                            structured=True,
                        )
                        progress.update(label="Análisis finalizado", state="complete")
                    st.session_state["analysis_result"] = {
                        "kind": kind,
                        "target": normalized_target,
                        "selected_sources": list(selected_sources),
                        "result": result,
                        "started_at": started_at.isoformat(timespec="seconds"),
                        "duration_seconds": round(time.perf_counter() - started_clock, 1),
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
    try:
        normalized_target = validate_target(kind, target)
    except ValueError:
        normalized_target = target.strip()
    matches_current_input = (
        saved is not None
        and saved.get("kind") == kind
        and saved.get("target") == normalized_target
        and set(saved.get("selected_sources", SOURCE_OPTIONS[kind])) == set(selected_sources)
    )

    if matches_current_input:
        st.markdown("### Resultado")
        result = saved["result"]
        source_values = {
            source: value for source, value in result.items()
            if source not in METADATA_KEYS
        }
        statuses = {source: source_status(value) for source, value in source_values.items()}
        problem_count = sum(
            status in {"Error", "Parcial", "Falta configuración", "Herramienta no instalada"}
            for status in statuses.values()
        )
        found_count = sum(status == "Completado · con hallazgos" for status in statuses.values())

        duration_col, sources_col, findings_col = st.columns(3)
        duration_col.metric("Duración", f'{saved.get("duration_seconds", 0):.1f} s')
        sources_col.metric("Fuentes consultadas", len(source_values))
        findings_col.metric("Fuentes con hallazgos", found_count)
        if saved.get("started_at"):
            st.caption(f'Inicio: {saved["started_at"]}')
        if problem_count:
            st.warning(
                f"{problem_count} fuente(s) requieren atención. "
                "Sus detalles aparecen abiertos debajo."
            )

        st.dataframe(
            [{"Fuente": source, "Estado": statuses[source]} for source in source_values],
            hide_index=True,
            use_container_width=True,
            column_config={
                "Fuente": st.column_config.TextColumn("Fuente", width="medium"),
                "Estado": st.column_config.TextColumn("Estado", width="large"),
            },
        )
        for source, value in source_values.items():
            _render_source_details(source, value)

        if st.button("Crear informe PDF local", key="create_pdf"):
            try:
                legacy_result = {\n                    source: value.to_legacy() if isinstance(value, SourceResult) else value\n                    for source, value in result.items()\n                }\n                pdf_path = _create_pdf(kind, normalized_target, legacy_result)
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
            f"El resultado anterior corresponde a {saved['kind']} y a {saved['target']}, "
            "o a otra selección de fuentes. Pulsa «Analizar» para actualizarlo."
        )
    else:
        st.info("Los resultados aparecerán aquí después de ejecutar un análisis.")


def render_configuration_tab() -> None:
    st.subheader("Configuración de fuentes")
    st.write(
        "Las claves se leen desde el entorno o desde un archivo .env local. "
        "Esta pantalla solo muestra si cada clave está presente; no revela ni edita secretos."
    )
    st.dataframe(
        Settings.from_environment().api_key_status(),
        hide_index=True,
        use_container_width=True,
    )
    st.caption(
        "Las fuentes que no tengan clave devolverán su propio aviso; las demás "
        "seguirán ejecutándose. Reinicia la app después de cambiar el archivo .env."
    )

    st.markdown("#### Herramientas opcionales")
    tool_rows = [
        {"Herramienta": name, "Estado": "Disponible en PATH" if installed else "No encontrada en PATH"}
        for name, installed in optional_tool_status().items()
    ]
    st.dataframe(tool_rows, hide_index=True, use_container_width=True)

    key_status = harvester_key_file_status()
    key_labels = {
        "valid": ("Correcto", "YAML válido"),
        "missing": ("No encontrado", "archivo api-keys.yaml no encontrado"),
        "invalid_yaml": ("Revisar", "YAML con sintaxis inválida"),
        "invalid_structure": ("Revisar", "estructura YAML inesperada"),
        "unreadable": ("Revisar", "archivo no legible"),
    }
    label, description = key_labels.get(key_status, ("Revisar", "estado desconocido"))
    st.write(f"**theHarvester API keys — {label}:** {description}")
    st.caption(
        "Se comprueba localmente la estructura YAML, sin mostrar valores de claves. "
        "theHarvester obtiene sus claves de api-keys.yaml, no del .env de InfoHunter."
    )


def render_reports_tab() -> None:
    st.subheader("Informes locales")
    st.caption("Los PDFs se guardan en la carpeta reports del proyecto.")
    if not REPORTS_DIR.exists():
        st.info("Todavía no hay informes generados.")
        return

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
        return

    st.warning(
        "Revisa los informes antiguos: versiones previas podían incluir datos de "
        "credenciales en claro."
    )
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
