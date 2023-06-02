import sys
import os
from pyhunter import PyHunter


def obtener_informacion_redes_sociales(nombre: str):
    # Verificar el sistema operativo
    if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        # Llamada al sistema en Linux
        comando = "python src/sherlock/sherlock/sherlock.py -fo output " + nombre
    else:
        # Llamada al sistema en otros sistemas operativos
        comando = "python src\sherlock\sherlock\sherlock.py -fo output " + nombre

    # Ejecutar el comando y capturar la salida
    os.system(comando)


def obtener_informacion_theHarvester(domain: str):
    # Verificar el sistema operativo
    if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        # Llamada al sistema en Linux
        comando = (
            "python src/theHarvester/theHarvester.py -d "
            + domain
            + " -b all -n -c -f output/"
            + domain
            + ".json"
        )
    else:
        # Llamada al sistema en otros sistemas operativos
        comando = (
            "python src\theHarvester\theHarvester.py -d "
            + domain
            + " -b all -n -c -f output'"
            + domain
            + ".json"
        )

    # Ejecutar el comando y capturar la salida
    os.system(comando)


def obtener_informacion_email(apikey: str, mail: str):
    hunter = PyHunter(apikey)
    result = hunter.email_verifier(mail)

    if result["status"] == "valid":
        print("La dirección de correo electrónico es válida.")
        print(result)
        print("----------")
        print("Nombre encontrado:", result["first_name"])
        print("Apellido encontrado:", result["last_name"])
    else:
        print(
            "La dirección de correo electrónico no es válida o no se encontró información asociada."
        )


def obtener_informacion_dominio(domain: str, apikey: str):
    hunter = PyHunter(apikey)
    result = hunter.domain_search(domain)

    if result["domain"] != None:
        comprobar_none(result["domain"], "Dominio")
        comprobar_none(result["organization"], "Nombre de la organización: ")
        comprobar_none(result["organization"], "Descripcion: ")
        comprobar_none(result["twitter"], "Twitter: ")
        comprobar_none(result["facebook"], "Facebook: ")
        comprobar_none(result["linkedin"], "LinkedIn: ")
        comprobar_none(result["instagram"], "Instagram: ")
        comprobar_none(result["youtube"], "Youtube: ")
        comprobar_none(result["facebook"], "Facebook: ")

        aux = result["technologies"]
        print("Tecnologias empleadas:")
        for a in aux:
            print("\t- " + str(a))

        comprobar_none(result["country"], "Pais: ")
        comprobar_none(result["state"], "Estado: ")
        comprobar_none(result["city"], "Ciudad: ")

        aux = result["emails"]
        print("Emails encontrados:")
        for email in aux:
            comprobar_none(email["value"], "\t- Email: ")
            if email["first_name"] != None and email["last_name"] != None:
                comprobar_none(
                    email["first_name"] + " " + email["last_name"], "\t- Nombre: "
                )
            comprobar_none(email["position"], "\t\t- Posicion: ")
            comprobar_none(email["seniority"], "\t\t- Senior: ")
            comprobar_none(email["department"], "\t\t- Departamento: ")
            comprobar_none(email["linkedin"], "\t\t- LinkedIn: ")
            comprobar_none(email["phone_number"], "\t\t- Telefono: ")
            print("\n")
    else:
        print(
            "La dirección de correo electrónico no es válida o no se encontró información asociada."
        )


def comprobar_none(text: str, mensaje: str):
    if text != None:
        print(str(mensaje) + " " + str(text))
