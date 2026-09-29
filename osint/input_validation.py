"""Input validation shared by the CLI and Streamlit dashboard."""
import ipaddress
import re

_LABEL = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")
_LOCAL = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+$")


def _domain(value):
    try:
        address = ipaddress.ip_address(value)
        return str(address)
    except ValueError:
        pass
    try:
        host = value.rstrip(".").encode("idna").decode("ascii").lower()
    except UnicodeError as error:
        raise ValueError("El dominio no es válido.") from error
    if len(host) > 253 or "." not in host or any(
        not _LABEL.fullmatch(label) for label in host.split(".")
    ):
        raise ValueError("Introduce un dominio válido, sin esquema ni ruta.")
    return host


def validate_target(kind, value):
    """Return a normalized target or raise ValueError with a user-facing message."""
    target = str(value or "").strip()
    if not target:
        raise ValueError("Introduce un valor para analizar.")
    if kind == "Usuario":
        if len(target) > 100 or any(char.isspace() or not char.isprintable() for char in target):
            raise ValueError("El usuario debe tener hasta 100 caracteres imprimibles, sin espacios.")
        return target
    if kind == "Email":
        if len(target) > 254 or target.count("@") != 1:
            raise ValueError("Introduce una dirección de email válida.")
        local, host = target.rsplit("@", 1)
        if (not local or len(local) > 64 or not _LOCAL.fullmatch(local)
                or local.startswith(".") or local.endswith(".") or ".." in local):
            raise ValueError("Introduce una dirección de email válida.")
        return f"{local}@{_domain(host)}"
    if kind == "Dominio":
        return _domain(target)
    raise ValueError("Tipo de búsqueda no válido.")
