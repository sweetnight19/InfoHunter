import sys
import os
from pyhunter import PyHunter


def obtener_informacion_redes_sociales(nombre: str):
    # Verificar el sistema operativo
    if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        # Llamada al sistema en Linux
        comando = "python3 src/sherlock/sherlock/sherlock.py -fo output " + nombre
    else:
        # Llamada al sistema en otros sistemas operativos
        comando = "python src\sherlock\sherlock\sherlock.py -fo output " + nombre

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

    # print("test: " + str(result) + "----------\n")

    if result["domain"] != "None":
        print("Dominio: " + str(result["domain"]))
        print("Nombre de la organización: " + str(result["organization"]))
        print("Descripcion: " + str(result["description"]))
        if not result["twitter"] == "None":
            print("Twitter: " + str(result["twitter"]))
        if not result["facebook"] == "None":
            print("facebook: " + str(result["facebook"]))
        if not result["linkedin"] == "None":
            print("linkedin: " + str(result["linkedin"]))
        if not result["instagram"] == "None":
            print("instagram: " + str(result["instagram"]))
        if not result["youtube"] == "None":
            print("youtube: " + str(result["youtube"]))

        aux = result["technologies"]
        print("Tecnologias empleadas:")
        for a in aux:
            print("\t- " + str(a))

        print("Pais: " + str(result["country"]))
        print("Estado: " + str(result["state"]))
        print("Ciudad: " + str(result["city"]))

        aux = result["emails"]
        print("Emails encontrados:")
        for email in aux:
            print("\t- Email: " + str(email["value"]))
            print(
                "\t- Nombre: "
                + str(email["first_name"])
                + " "
                + str(email["last_name"])
            )
            if not email["position"] == "None":
                print("\t\t- Posicion: " + str(email["position"]))
            if not email["seniority"] == "None":
                print("\t\t- Senior: " + str(email["seniority"]))
            if not email["department"] == "None":
                print("\t\t- Departamento: " + str(email["department"]))
            if not email["linkedin"] == "None":
                print("\t\t- LinkedIn: " + str(email["linkedin"]))
            if not email["phone_number"] == "None":
                print("\t\t- Telefono: " + str(email["phone_number"]))
            print("\n")
    else:
        print(
            "La dirección de correo electrónico no es válida o no se encontró información asociada."
        )

    # print(result)
