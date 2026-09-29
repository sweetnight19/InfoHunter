"""Human-readable status labels for analyzer outputs."""


def source_status(value):
    if isinstance(value, dict):
        error = value.get("error")
        if error:
            message = str(error).lower()
            if "not set" in message or "not configured" in message:
                return "Falta configuración"
            if "not installed" in message or "not on path" in message:
                return "Herramienta no instalada"
            return "Error"
        if "found" in value:
            return "Completado · con hallazgos" if value["found"] else "Completado · sin hallazgos"
        if value:
            return "Completado"
        return "Sin resultados"
    if isinstance(value, (list, tuple, set)):
        errors = [str(item).lower().startswith("error running") for item in value]
        if any(errors) and any(not item for item in errors):
            return "Parcial"
        if any(errors):
            return "Error"
        return "Completado · con hallazgos" if value else "Completado · sin hallazgos"
    if value is None or value == "":
        return "Sin resultados"
    return "Completado"
