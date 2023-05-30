from . import fuentes
import os


def verificar_carpeta_output():
    if not os.path.exists("output"):
        os.makedirs("output")


def realizar_consulta(nombre: str):
    # Verificar que exista la carpeta output
    verificar_carpeta_output()

    # Consultamos las redes sociales
    fuentes.obtener_informacion_redes_sociales(nombre)
