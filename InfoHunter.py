import pyfiglet
import argparse
import json
import os
from src.recopilacion import consultas
from src.riesgos import evaluacion


class ApiKeysManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.api_keys = {}

    def load_keys(self):
        try:
            with open(self.file_path) as file:
                self.api_keys = json.load(file)
        except FileNotFoundError:
            print(
                f"El archivo {self.file_path} no existe. Asegúrate de crearlo y agregar las claves de API."
            )

    def get_key(self, api_name):
        return self.api_keys.get(api_name)

    def add_key(self, api_name, api_key):
        self.api_keys[api_name] = api_key

    def save_keys(self):
        with open(self.file_path, "w") as file:
            json.dump(self.api_keys, file, indent=4)


def analizar_informacion_username(username: str):
    # Ruta de los archivos JSON generados por Sherlock y Maigret
    sherlock_json_file = f"output/{username}.json"
    maigret_json_file = f"output/report_{username}_simple.json"

    # Verificar si los archivos existen
    if not (os.path.exists(sherlock_json_file) and os.path.exists(maigret_json_file)):
        print("Los archivos JSON no existen.")
        return

    print("Leyendo el archivo JSON de Sherlock...")
    # Leer el archivo JSON generado por Sherlock
    with open(sherlock_json_file, "r") as file:
        sherlock_data = json.load(file)

    print("Leyendo el archivo JSON de Maigret...")
    # Leer el archivo JSON generado por Maigret
    with open(maigret_json_file, "r") as file:
        maigret_data = json.load(file)

    # Crear una lista para almacenar los servicios del Maigret que no están en Sherlock
    servicios_faltantes = []

    print("Verificando los servicios faltantes...")
    # Verificar si las URL de Sherlock están en Maigret
    for sherlock_url in sherlock_data:
        url_encontrada = False

        # Buscar la URL de Sherlock en Maigret
        for servicio, datos in maigret_data.items():
            if "url_user" in datos and datos["url_user"] == sherlock_url:
                url_encontrada = True
                break

        # Si la URL de Sherlock no está en Maigret, agregarla a la lista de servicios faltantes
        if not url_encontrada:
            servicios_faltantes.append(sherlock_url)

    # Agregar los servicios faltantes a maigret_data
    for servicio_faltante in servicios_faltantes:
        maigret_data[servicio_faltante] = {
            "url_user": servicio_faltante,
            # Puedes añadir más campos según la estructura de los datos de Maigret
        }

    # Guardar los datos actualizados en un nuevo archivo JSON
    analyzed_output_file = f"output/analyzed_{username}.json"
    with open(analyzed_output_file, "w") as file:
        json.dump(maigret_data, file, indent=4)

    print(
        "Análisis completo. Los servicios faltantes se han añadido a /output/analyzed_"
        + username
    )


def print_banner():
    ascii_banner = pyfiglet.figlet_format("InfoHunter")

    print(ascii_banner)
    print("Bienvenido a InfoHunter - Herramienta de OSINT")


def recopilar_informacion_mail(
    mail: str, pyhunter_api_key: str, breachdirectory_api_key: str
):
    # Realizar una consulta
    consultas.realizar_consulta_email(mail, pyhunter_api_key, breachdirectory_api_key)


def recopilar_informacion_dominio(domain: str, pyhunter_api_key: str):
    # Realizar una consulta
    consultas.realizar_consulta_dominio(domain, pyhunter_api_key)


def recopilar_informacion_redes_sociales(username: str):
    # Realizar una consulta
    consultas.realizar_consulta_redes_sociales(username)

    # Procesar los resultados
    # datos_procesados = procesar_resultados(resultados)

    # Obtener información adicional de redes sociales
    # informacion_social = obtener_informacion_redes_sociales('nombre de usuario')


def identificar_riesgos_redes_sociales(username: str):
    evaluacion.identificar_riesgos_username(username)


def main():
    # Crear el parser de argumentos
    parser = argparse.ArgumentParser(description="Herramienta de OSINT")

    parser.add_argument("-u", "--username", type=str, help="Nombre de usuario")
    parser.add_argument("-m", "--email", type=str, help="Email a buscar")
    parser.add_argument("-d", "--domain", type=str, help="Dominio a buscar")

    # Obtener los argumentos pasados desde la línea de comandos
    args = parser.parse_args()

    # Acceder a los valores de los argumentos
    username = args.username
    mail = args.email
    domain = args.domain

    # Uso de la clase ApiKeysManager
    keys_manager = ApiKeysManager("api_keys.json")
    keys_manager.load_keys()

    # Mostrar el banner
    print_banner()

    if username:
        print("1. Realizar la recopilación de información")
        recopilar_informacion_redes_sociales(username)

        print("2. Analizar la información obtenida")
        analizar_informacion_username(username)

        print("3. Identificar riesgos de seguridad o privacidad")
        identificar_riesgos_redes_sociales(username)
    if mail:
        print("1. Realizar la recopilación de información")
        pyhunter_api_key = keys_manager.get_key("pyhunter")
        breachdirectory_api_key = keys_manager.get_key("breachdirectory")
        if pyhunter_api_key:  # Utilizar la clave de API
            recopilar_informacion_mail(mail, pyhunter_api_key, breachdirectory_api_key)
        else:
            print(
                "La clave de PyHunter no se encuentra en el archivo de claves de API."
            )
    if domain:
        print("1. Realizar la recopilación de información")
        pyhunter_api_key = keys_manager.get_key("pyhunter")
        if pyhunter_api_key:  # Utilizar la clave de API
            recopilar_informacion_dominio(domain, pyhunter_api_key)
        else:
            print(
                "La clave de PyHunter no se encuentra en el archivo de claves de API."
            )

    # 3. Identificar riesgos de seguridad o privacidad
    # identificar_riesgos()

    # 4. Establecer medidas para proteger la privacidad y seguridad
    # establecer_medidas()

    # 5. Evaluar la eficacia de las medidas implementadas
    # evaluar_eficacia()

    print("¡Proceso de OSINT finalizado!")


if __name__ == "__main__":
    main()
