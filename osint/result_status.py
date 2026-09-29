"""Presentation helpers for legacy payloads and normalized source results."""

from osint.results import SourceResult, SourceState


_STATE_LABELS = {
    SourceState.SUCCESS: "Completado · con hallazgos",
    SourceState.EMPTY: "Completado · sin hallazgos",
    SourceState.PARTIAL: "Parcial",
    SourceState.ERROR: "Error",
    SourceState.NOT_CONFIGURED: "Falta configuración",
    SourceState.UNAVAILABLE: "Herramienta no instalada",
}


def source_status(value):
    if isinstance(value, SourceResult):
        if value.state == SourceState.SUCCESS and not value.has_findings:
            return "Completado · sin hallazgos"
        return _STATE_LABELS[value.state]

    if isinstance(value, dict):
        error = value.get("error")
        if error:
            message = str(error).casefold()
            if "not set" in message or "not configured" in message:
                return "Falta configuración"
            if "not installed" in message or "not on path" in message:
                return "Herramienta no instalada"
            return "Error"
        if "found" in value:
            return "Completado · con hallazgos" if value["found"] else "Completado · sin hallazgos"
        return "Completado" if value else "Sin resultados"

    if isinstance(value, (list, tuple, set)):
        errors = [str(item).casefold().startswith("error running") for item in value]
        if any(errors) and any(not item for item in errors):
            return "Parcial"
        if any(errors):
            return "Error"
        return "Completado · con hallazgos" if value else "Completado · sin hallazgos"
    if value is None or value == "":
        return "Sin resultados"
    return "Completado"
