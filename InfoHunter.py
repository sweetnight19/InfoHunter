import pyfiglet
import argparse
from src.recopilacion.consultas import realizar_consulta
from src.recopilacion.extraccion import procesar_resultados
from src.recopilacion.fuentes import obtener_informacion_redes_sociales


def print_banner():
    ascii_banner = pyfiglet.figlet_format("InfoHunter")

    print(ascii_banner)
    print("Bienvenido a InfoHunter - Herramienta de OSINT")


def recopilar_informacion(nombre: str):
    # Solicitar al usuario el nombre para buscar información
    # nombre = input("Ingresa el nombre para buscar información: ")

    # Realizar una consulta
    realizar_consulta(nombre)

    # Procesar los resultados
    # datos_procesados = procesar_resultados(resultados)

    # Obtener información adicional de redes sociales
    # informacion_social = obtener_informacion_redes_sociales('nombre de usuario')


def main():
    # Crear el parser de argumentos
    parser = argparse.ArgumentParser(description="Herramienta de OSINT")

    # Agregar el argumento '-u' para el nombre de usuario
    parser.add_argument("-u", "--username", type=str, help="Nombre de usuario")

    # Obtener los argumentos pasados desde la línea de comandos
    args = parser.parse_args()

    # Acceder al valor del argumento '-u' (username)
    username = args.username

    # Mostrar el banner
    print_banner()

    # 1. Realizar la recopilación de información
    recopilar_informacion(username)

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
