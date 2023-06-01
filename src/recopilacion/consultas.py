from . import fuentes
import os


def verificar_carpeta_output():
    if not os.path.exists("output"):
        os.makedirs("output")


def realizar_consulta_redes_sociales(nombre: str):
    # Verificar que exista la carpeta output
    verificar_carpeta_output()

    # Consultamos las redes sociales
    fuentes.obtener_informacion_redes_sociales(nombre)


def realizar_consulta_email(mail: str, apikey: str):
    fuentes.obtener_informacion_email(apikey, mail)


def realizar_consulta_dominio(domain, pyhunter_api_key):
    fuentes.obtener_informacion_dominio(domain, pyhunter_api_key)
