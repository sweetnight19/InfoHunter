import sys
import os
from pyhunter import PyHunter
import requests
import json
from src.riesgos import evaluacion
from src.evaluacion import mejoras


def convert_txt_to_json(nombre: str, txt_file_path: str):
    json_data = []
    with open(txt_file_path, "r") as file:
        lines = file.readlines()
        for line in lines[:-1]:
            website_url = line.strip()
            json_obj = website_url
            json_data.append(json_obj)

    print(json.dumps(json_data, indent=4))

    output_file_path = f"./output/{nombre}.json"
    with open(output_file_path, "w") as file:
        json.dump(json_data, file, indent=4)

    print(
        f"Se ha convertido el archivo '{txt_file_path}' a '{output_file_path}' en formato JSON."
    )


def sherlock(nombre: str):
    # Verificar el sistema operativo
    if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        # Llamada al sistema en Linux
        # comando = "python src/sherlock/sherlock/sherlock.py -fo output " + nombre
        comando = "python src/sherlock/sherlock/sherlock.py -fo output " + nombre

    else:
        # Llamada al sistema en otros sistemas operativos
        comando = "python src\\sherlock\\sherlock\\sherlock.py -fo output " + nombre

    # Ejecutar el comando y capturar la salida
    os.system(comando)


def maigret(nombre: str):
    # Verificar el sistema operativo
    if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        # Llamada al sistema en Linux
        comando = (
            "python src/maigret/maigret.py --timeout 10 -n 1000 -fo output -J simple "
            + nombre
        )

    else:
        # Llamada al sistema en otros sistemas operativos
        comando = (
            "python src\\maigret\\maigret.py --timeout 10 -n 1000 -fo output -J simple "
            + nombre
        )

    # Ejecutar el comando y capturar la salida
    os.system(comando)


def obtener_informacion_redes_sociales(nombre: str):
    sherlock(nombre)
    txt_file_path = "./output/" + nombre + ".txt"
    convert_txt_to_json(nombre, txt_file_path)
    maigret(nombre)


def obtener_informacion_theHarvester(domain: str):
    # Verificar el sistema operativo
    if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        # Llamada al sistema en Linux
        comando = (
            "python src/theHarvester/theHarvester.py -d "
            + domain
            + " -s -v -n -b all -f output/"
            + domain
            + ".json"
        )
    else:
        # Llamada al sistema en otros sistemas operativos
        comando = (
            "python src\\theHarvester\\theHarvester.py -d "
            + domain
            + " -s -v -n -b all -f output\\"
            + domain
            + ".json"
        )

    # Ejecutar el comando y capturar la salida
    os.system(comando)


def obtener_informacion_email(
    apikey: str, breachdirectory_api_key: str, similar_web_api_key: str, mail: str
):
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

    print("2. Buscando filtracion de datos...")
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

            # print(results)
            # 3. Identificar riesgos de seguridad o privacidad
            print("3. Identificando riesgos")
            print("4. Realizando evaluación")
            evaluacion_resultante = evaluacion.generar_evaluacion_y_recomendaciones(
                results, similar_web_api_key
            )

            print("5. Generando informe en PDF")
            mejoras.generar_report_mail(evaluacion_resultante)

        else:
            print("La solicitud no fue exitosa.")
    else:
        print("Error en Breachdirectory API: " + str(response.status_code))


def obtener_informacion_dominio(domain: str, apikey: str, similar_web_api_key: str):
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

        result["alexa_rank"] = evaluacion.getAlexaRank(domain, similar_web_api_key)
        return result
    else:
        print(
            "La dirección de correo electrónico no es válida o no se encontró información asociada."
        )


def comprobar_none(text: str, mensaje: str):
    if text != None:
        print(str(mensaje) + " " + str(text))
