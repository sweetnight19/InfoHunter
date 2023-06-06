import sys
import os
from pyhunter import PyHunter
import requests


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


def obtener_informacion_email(apikey: str, breachdirectory_api_key: str, mail: str):
    hunter = PyHunter(apikey)
    result = hunter.email_verifier(mail)

    if result["status"] == "valid":
        print("La dirección de correo electrónico es válida.")
        # print(result)
        if "first_name" in result:
            print("Nombre encontrado:", result["first_name"])
        if "last_name" in result:
            print("Apellido encontrado:", result["last_name"])
    else:
        print(
            "La dirección de correo electrónico no es válida o no se encontró información asociada."
        )

    url = "https://breachdirectory.p.rapidapi.com/"

    querystring = {"func": "auto", "term": mail}

    headers = {
        "X-RapidAPI-Key": breachdirectory_api_key,
        "X-RapidAPI-Host": "breachdirectory.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()

        # print(data)

        # Verificar si la solicitud fue exitosa
        if data.get("success", True):
            # Obtener los resultados que cumplen con la condición "email_only false"
            results = [
                result
                for result in data.get("result", [])
                if not result.get("email_only", True)
            ]

            # Mostrar por pantalla los campos "line" separados por ":"
            for result in results:
                line = result.get("line", "")
                username, password = line.split(":")
                source = result.get("sources")[0]
                print(f"Source: {source}")
                print(f"Username: {username}")
                print(f"Password: {password}")
                print()
        else:
            print("La solicitud no fue exitosa.")
    else:
        print("Error en Breachdirectory API: " + response.status_code)


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
