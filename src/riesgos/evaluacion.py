import json


# En este ejemplo, se itera sobre cada red social en los datos y se evalúa el nivel de riesgo de privacidad específico para cada una.
# En el caso de Reddit, se verifican ciertos campos en los datos y se incrementa el nivel de riesgo de privacidad en función de la presencia de información sensible (por ejemplo, si el usuario es empleado, moderador o si el contenido es NSFW).
# Puedes agregar más condiciones y lógica de evaluación de riesgo para otras redes sociales según tus necesidades.
def evaluar_privacidad(datos):
    riesgo_privacidad = 0

    # Evaluar el nivel de riesgo de privacidad para cada red social en los datos
    for red_social, datos_red_social in datos.items():
        if red_social == "Reddit":
            # Evaluar el riesgo de privacidad en los datos de Reddit
            if "status" in datos_red_social and "ids" in datos_red_social["status"]:
                ids = datos_red_social["status"]["ids"]
                # Verificar si hay información sensible en los IDs de Reddit
                if ids.get("is_employee", "").lower() == "true":
                    riesgo_privacidad += 3
                if ids.get("is_mod", "").lower() == "true":
                    riesgo_privacidad += 2
                if ids.get("is_nsfw", "").lower() == "true":
                    riesgo_privacidad += 1

        # Agrega más condiciones para evaluar el riesgo de privacidad en otras redes sociales

    return riesgo_privacidad


# Se itera sobre cada red social en los datos y se evalúa el nivel de riesgo de reputación específico para cada una.
# En el caso de Reddit, se verifica si el campo "total_karma" en los datos está por debajo de cierto umbral (en este caso, 1000) y se incrementa el nivel de riesgo de reputación en consecuencia.
# Puedes agregar más condiciones y lógica de evaluación de riesgo para otras redes sociales según tus necesidades.
def evaluar_reputacion(datos):
    riesgo_reputacion = 0

    # Evaluar el nivel de riesgo de reputación para cada red social en los datos
    for red_social, datos_red_social in datos.items():
        if red_social == "Reddit":
            # Evaluar el riesgo de reputación en los datos de Reddit
            if "status" in datos_red_social:
                status = datos_red_social["status"]
                # Verificar si el usuario tiene baja reputación en Reddit
                if status.get("total_karma", 0) < 1000:
                    riesgo_reputacion += 2

        # Agrega más condiciones para evaluar el riesgo de reputación en otras redes sociales

    return riesgo_reputacion


# Se itera sobre cada red social en los datos y se evalúa el nivel de riesgo de seguridad específico para cada una.
# En el caso de Reddit, se verifica si el campo "http_status" en los datos indica un código de error HTTP mayor o igual a 400 y se incrementa el nivel de riesgo de seguridad en consecuencia.
# Puedes agregar más condiciones y lógica de evaluación de riesgo para otras redes sociales según tus necesidades.
def evaluar_seguridad(datos):
    riesgo_seguridad = 0

    # Evaluar el nivel de riesgo de seguridad para cada red social en los datos
    for red_social, datos_red_social in datos.items():
        if red_social == "Reddit":
            # Evaluar el riesgo de seguridad en los datos de Reddit
            if "http_status" in datos_red_social:
                http_status = datos_red_social["http_status"]
                # Verificar si la respuesta HTTP indica un error de seguridad
                if http_status >= 400:
                    riesgo_seguridad += 3

        # Agrega más condiciones para evaluar el riesgo de seguridad en otras redes sociales

    return riesgo_seguridad


# Se itera sobre cada red social en los datos y se evalúa el nivel de riesgo de configuración de privacidad específico para cada una.
# En el caso de Reddit, se verifica si el campo "status" en los datos contiene información sobre los identificadores de usuario ("ids") y se verifica si el perfil de usuario está configurado como privado.
# Si es así, se incrementa el nivel de riesgo de configuración de privacidad en consecuencia.
# Puedes agregar más condiciones y lógica de evaluación de riesgo para otras redes sociales según tus necesidades.
def evaluar_configuracion_privacidad(datos):
    riesgo_configuracion = 0

    # Evaluar el nivel de riesgo de configuración de privacidad para cada red social en los datos
    for red_social, datos_red_social in datos.items():
        if red_social == "Reddit":
            # Evaluar el riesgo de configuración de privacidad en los datos de Reddit
            if "status" in datos_red_social:
                status = datos_red_social["status"]
                if "ids" in status:
                    ids = status["ids"]
                    if "is_private" in ids:
                        is_private = ids["is_private"]
                        # Verificar si el perfil de usuario está configurado como privado
                        if is_private == "True":
                            riesgo_configuracion += 2

        # Agrega más condiciones para evaluar el riesgo de configuración de privacidad en otras redes sociales

    return riesgo_configuracion


# Se itera sobre cada red social en los datos y se evalúa el nivel de riesgo de cumplimiento legal específico para cada una.
# En el caso de Reddit, se verifica si el campo "status" en los datos contiene información sobre si el contenido asociado al perfil es considerado para adultos (NSFW).
# Si es así, se incrementa el nivel de riesgo de cumplimiento legal en consecuencia.
# Puedes agregar más condiciones y lógica de evaluación de riesgo para otras redes sociales según tus necesidades.
def evaluar_cumplimiento_legal(datos):
    riesgo_cumplimiento = 0

    # Evaluar el nivel de riesgo de cumplimiento legal para cada red social en los datos
    for red_social, datos_red_social in datos.items():
        if red_social == "Reddit":
            # Evaluar el riesgo de cumplimiento legal en los datos de Reddit
            if "status" in datos_red_social:
                status = datos_red_social["status"]
                if "is_nsfw" in status:
                    is_nsfw = status["is_nsfw"]
                    # Verificar si el contenido asociado al perfil es considerado para adultos (NSFW)
                    if is_nsfw == "True":
                        riesgo_cumplimiento += 3

        # Agrega más condiciones para evaluar el riesgo de cumplimiento legal en otras redes sociales

    return riesgo_cumplimiento


def identificar_riesgos_username(username: str):
    # Leer los datos de redes sociales del archivo JSON
    file_path = f"output/maigret_{username}.json"
    with open(file_path, "r") as file:
        datos_redes_sociales = json.load(file)

    # Definir un diccionario vacío para almacenar los riesgos
    riesgos = {}

    riesgos["privacidad"] = {
        "tipo": "privacidad",
        "descripcion": "Riesgo de divulgación no autorizada de información personal.",
        "impacto": "",
        "probabilidad": "",
        "valoracion": "",
    }

    riesgos["reputacion"] = {
        "tipo": "reputacion",
        "descripcion": "Riesgo de daño a la reputación de la persona o entidad.",
        "impacto": "",
        "probabilidad": "",
        "valoracion": "",
    }

    riesgos["seguridad"] = {
        "tipo": "seguridad",
        "descripcion": "Riesgo de acceso no autorizado a la cuenta o datos sensibles.",
        "impacto": "",
        "probabilidad": "",
        "valoracion": "",
    }

    riesgos["configuracion_privacidad"] = {
        "tipo": "configuracion_privacidad",
        "descripcion": "Riesgo de configuraciones inadecuadas que afecten la privacidad.",
        "impacto": "",
        "probabilidad": "",
        "valoracion": "",
    }

    riesgos["cumplimiento_legal"] = {
        "tipo": "cumplimiento_legal",
        "descripcion": "Riesgo de incumplimiento de regulaciones legales y normativas.",
        "impacto": "",
        "probabilidad": "",
        "valoracion": "",
    }

    for datos in datos_redes_sociales.items():
        # Evaluar la privacidad de la información
        riesgo_privacidad = evaluar_privacidad(datos)
        riesgos.append(riesgo_privacidad)

        # Evaluar la reputación y daño a la imagen
        riesgo_reputacion = evaluar_reputacion(datos)
        riesgos.append(riesgo_reputacion)

        # Evaluar las amenazas de seguridad
        riesgo_seguridad = evaluar_seguridad(datos)
        riesgos.append(riesgo_seguridad)

        # Evaluar la configuración de privacidad
        riesgo_configuracion = evaluar_configuracion_privacidad(datos)
        riesgos.append(riesgo_configuracion)

        # Evaluar el cumplimiento legal
        riesgo_cumplimiento = evaluar_cumplimiento_legal(datos)
        riesgos.append(riesgo_cumplimiento)

    # Aplicar la norma ISO 27001
    criterios_iso = {
        "privacidad": 0.8,
        "reputacion": 0.6,
        "seguridad": 0.9,
        "configuracion": 0.7,
        "cumplimiento": 0.5,
    }

    riesgos_iso = []

    print(riesgos)

    for riesgo in riesgos:
        riesgo_iso = riesgo.get("riesgo", 0) * criterios_iso.get(
            riesgo.get("tipo", ""), 0
        )
        riesgos_iso.append(riesgo_iso)

    # Mostrar los resultados de la evaluación ISO
    print(
        "Resultado de la evaluación de riesgos según la norma ISO 27001 para el usuario:",
        username,
    )
    for riesgo in riesgos_iso:
        print("- Riesgo:", riesgo)
