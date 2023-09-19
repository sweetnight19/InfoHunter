import json
import random


def generar_evaluacion_y_recomendaciones(data):
    evaluacion = []
    
    # Clasificar automáticamente como "Crítico"
    nivel_critico = 'Crítico'

    # Definir recomendaciones basadas en la evaluación
    recomendaciones_data_leak = [
        {"recomendacion": "Cambie inmediatamente la contraseña de la cuenta afectada.", "impacto": "Alto"},
        {"recomendacion": "Habilite la autenticación de dos factores (2FA) para mejorar la seguridad de su cuenta.", "impacto": "Medio"},
        {"recomendacion": "Revise todas sus cuentas en busca de contraseñas reutilizadas y cámbielas.", "impacto": "Alto"},
        {"recomendacion": "Monitoree sus cuentas bancarias y financieras en busca de actividad no autorizada.", "impacto": "Alto"},
        {"recomendacion": "Sea escéptico ante los correos electrónicos o mensajes sospechosos y evite hacer clic en enlaces no verificados.", "impacto": "Medio"},
        {"recomendacion": "Informe a las autoridades pertinentes y a las plataformas en caso de fraude o robo de identidad.", "impacto": "Alto"},
        {"recomendacion": "Utilice una solución de gestión de contraseñas para crear y almacenar contraseñas seguras.", "impacto": "Medio"},
        {"recomendacion": "Mantenga sus sistemas y software actualizados para protegerse contra vulnerabilidades conocidas.", "impacto": "Alto"},
        {"recomendacion": "Revise la configuración de privacidad de sus cuentas en línea y limpie la información personal innecesaria.", "impacto": "Medio"},
        {"recomendacion": "Eduque a sus contactos sobre las amenazas en línea y promueva prácticas seguras.", "impacto": "Bajo"},
    ]

    for entry in data:
        email = entry['line'].split(':')[0]
        breaches = entry['sources']
        last_breach = entry['last_breach']
        password = entry['line'].split(':')[1]

        evaluacion.append({
            'Email': email,
            'Breaches': breaches,
            'Password': password,
            'Last Breach': last_breach,
            'Nivel de Criticidad': nivel_critico,
            'Recomendaciones': random.sample(recomendaciones_data_leak, 2)
        })
    #Debug
    #print(evaluacion)
    
    return evaluacion

def identificar_riesgos_username(username: str):
    # Leer los datos de redes sociales del archivo JSON
    file_path = f"output/report_{username}_simple.json"
    with open(file_path, "r") as file:
        datos_redes_sociales = json.load(file)
        
    # Crear una variable para almacenar los datos importantes
    datos_importantes = {}

    # Definir el nivel crítico común para todas las redes sociales
    nivel_critico_comun = "Medio"

    # Lista de recomendaciones para nivel crítico medio
    recomendaciones_medio = [
        {"recomendacion": "Revise cuidadosamente su configuración de privacidad y ajuste la visibilidad de su perfil y publicaciones según sea necesario.", "impacto": "Bajo"},
        {"recomendacion": "Sea cauteloso al aceptar solicitudes de amistad o seguir a personas desconocidas.", "impacto": "Medio"},
        {"recomendacion": "Regularmente revise su actividad y ajuste la configuración de notificaciones para mantener un mayor control sobre su cuenta.", "impacto": "Alto"},
        {"recomendacion": "Evite compartir datos personales o sensibles en sus publicaciones.", "impacto": "Medio"},
        {"recomendacion": "Use autenticación de dos factores (2FA) si está disponible para mejorar la seguridad de su cuenta.", "impacto": "Alto"},
        {"recomendacion": "Mantenga sus contraseñas seguras y cambie regularmente las contraseñas de sus cuentas.", "impacto": "Alto"},
        {"recomendacion": "Desactive las ubicaciones geográficas en sus publicaciones para proteger su privacidad.", "impacto": "Medio"},
        {"recomendacion": "No comparta información confidencial, como números de teléfono o direcciones, en su perfil público.", "impacto": "Medio"},
        {"recomendacion": "Sea escéptico ante las ofertas o enlaces sospechosos que reciba a través de mensajes directos.", "impacto": "Medio"},
        {"recomendacion": "Revise periódicamente las aplicaciones y servicios vinculados a su cuenta y elimine los que ya no usa o confía.", "impacto": "Bajo"},
        {"recomendacion": "Informe de inmediato cualquier actividad o cuenta sospechosa a la plataforma de redes sociales.", "impacto": "Alto"},
        {"recomendacion": "No revele su ubicación en tiempo real a través de las redes sociales, especialmente si está fuera de casa.", "impacto": "Medio"},
        {"recomendacion": "Tenga cuidado con las aplicaciones de terceros y asegúrese de que tengan buenas calificaciones y reseñas antes de autorizarlas.", "impacto": "Medio"},
    ]

    # Extraer los datos importantes y almacenarlos en la variable
    for red_social, detalles in datos_redes_sociales.items():
        datos_importantes[red_social] = {
            "status": detalles["status"],
            "url_user": detalles["url_user"],
            "nivel_critico": nivel_critico_comun,
            "recomendaciones":random.sample(recomendaciones_medio, 2)
        }

    # Asignar el nivel crítico común a todas las redes sociales
    #datos_importantes[red_social]["status"]["nivel_critico"] = nivel_critico_comun

    # Seleccionar un conjunto aleatorio de 3 recomendaciones de nivel crítico medio
    #recomendaciones_seleccionadas = random.sample(recomendaciones_medio, 3)

    # Agregar las recomendaciones al diccionario de datos importantes
    #datos_importantes[red_social]["recomendaciones"] = recomendaciones_seleccionadas

    # Imprimir los datos importantes con las recomendaciones y niveles de impacto
    """
    for red_social, detalles in datos_importantes.items():
        print(f"Red Social: {red_social}")
        print(f"Estado: {detalles['status']['estado']}")
        print(f"Nivel Crítico: {detalles['status']['nivel_critico']}")
        print(f"URL del Usuario: {detalles['url_user']}")
        print("Recomendaciones:")
        for idx, recomendacion_info in enumerate(detalles['recomendaciones'], start=1):
            recomendacion = recomendacion_info["recomendacion"]
            impacto = recomendacion_info["impacto"]
            print(f"{idx}. Recomendación: {recomendacion}")
            print(f"   Nivel de Impacto: {impacto}")
        print("\n")
    """
    
    #Debug    
    print(datos_importantes)
    
    return datos_importantes
        