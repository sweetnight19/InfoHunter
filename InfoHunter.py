import pyfiglet
import argparse
import json
from src.recopilacion import consultas
from src.recopilacion.extraccion import procesar_resultados
from src.recopilacion.fuentes import obtener_informacion_redes_sociales


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

    # 1. Realizar la recopilación de información
    if username:
        recopilar_informacion_redes_sociales(username)
    if mail:
        pyhunter_api_key = keys_manager.get_key("pyhunter")
        breachdirectory_api_key = keys_manager.get_key("breachdirectory")
        if pyhunter_api_key:  # Utilizar la clave de API
            # print(f"Clave de PyHunter: {pyhunter_api_key}")
            recopilar_informacion_mail(mail, pyhunter_api_key, breachdirectory_api_key)
        else:
            print(
                "La clave de PyHunter no se encuentra en el archivo de claves de API."
            )
    if domain:
        pyhunter_api_key = keys_manager.get_key("pyhunter")
        if pyhunter_api_key:  # Utilizar la clave de API
            recopilar_informacion_dominio(domain, pyhunter_api_key)
        else:
            print(
                "La clave de PyHunter no se encuentra en el archivo de claves de API."
            )

    # 2. Analizar la información obtenida
    # analizar_informacion()

    # 3. Identificar riesgos de seguridad o privacidad
    # identificar_riesgos()

    # 4. Establecer medidas para proteger la privacidad y seguridad
    # establecer_medidas()

    # 5. Evaluar la eficacia de las medidas implementadas
    # evaluar_eficacia()

    print("¡Proceso de OSINT finalizado!")


if __name__ == "__main__":
    main()
