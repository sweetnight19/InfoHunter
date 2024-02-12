from . import fuentes
import os
import json
from fpdf import FPDF
from src.evaluacion import mejoras


def verificar_carpeta_output():
    if not os.path.exists("output"):
        os.makedirs("output")


def realizar_consulta_redes_sociales(nombre: str):
    # Verificar que exista la carpeta output
    verificar_carpeta_output()

    # Consultamos las redes sociales
    fuentes.obtener_informacion_redes_sociales(nombre)


def realizar_consulta_email(
    mail: str, apikey: str, breachdirectory_api_key: str, similar_web_api_key: str
):
    fuentes.obtener_informacion_email(
        apikey, breachdirectory_api_key, similar_web_api_key, mail
    )


def realizar_consulta_dominio(domain, pyhunter_api_key, similar_web_api_key):
    datos_pyhunter = fuentes.obtener_informacion_dominio(
        domain, pyhunter_api_key, similar_web_api_key
    )
    # mejoras.generar_report_domain(datos_pyhunter)
    fuentes.obtener_informacion_theHarvester(domain)
    mejoras.generar_report_domain(datos_pyhunter, domain)
    # generate_pdf_from_json(domain)


class PDF(FPDF):
    def header(self):
        # Encabezado
        self.set_font("Arial", "B", 12)
        self.cell(40, 10, "InfoHunter", 0, 0, "L")
        self.cell(0, 10, f"Dominio: {self.domain}", 0, 0, "R")
        self.ln(20)

    def set_domain(self, domain):
        self.domain = domain

    def chapter_title(self, title):
        # Título del capítulo
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, title, ln=True)

    def chapter_body(self, data):
        # Definir el estilo de fuente y tamaño
        self.set_font("Arial", size=10)

        # Verificar si los datos son una cadena o una lista
        if isinstance(data, str):
            # Dividir por salto de línea si es una cadena
            elements = data.split("\n")
        elif isinstance(data, list):
            # Utilizar la lista tal cual si es una lista
            elements = data
        else:
            # No hacer nada si el tipo de dato no es válido
            return

        # Agregar un guion ("-") antes de cada elemento
        elements_formatted = ["- " + element for element in elements]

        # Imprimir los elementos en el documento
        for element in elements_formatted:
            self.multi_cell(0, 6, element)
            self.ln(4)

    def chapter_break(self):
        # Salto de página entre capítulos
        self.add_page()

    def footer(self):
        # Número de página
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")


def generate_pdf_from_json(domain):
    # Ruta del archivo JSON
    json_file = f"output/{domain}.json"

    # Verificar si el archivo existe
    if not os.path.exists(json_file):
        print(f"El archivo JSON '{json_file}' no existe.")
        return

    # Cargar el archivo JSON
    with open(json_file) as file:
        data = json.load(file)

    # Obtener los datos del archivo JSON
    asns = "\n".join(data.get("asns", []))
    emails = "\n".join(data.get("emails", []))
    hosts = "\n".join(data.get("hosts", []))
    interesting_urls = "\n".join(data.get("interesting_urls", []))
    ips = "\n".join(data.get("ips", []))

    # Crear el documento PDF
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_domain(domain)

    # Capítulo: ASNs
    pdf.add_page()
    pdf.chapter_title(f"ASNs")
    pdf.chapter_body(asns)

    # Capítulo: Emails
    pdf.chapter_break()
    pdf.chapter_title(f"Emails")
    pdf.chapter_body(emails)

    # Capítulo: Hosts
    pdf.chapter_break()
    pdf.chapter_title(f"Hosts")
    pdf.chapter_body(hosts)

    # Capítulo: URLs interesantes
    pdf.chapter_break()
    pdf.chapter_title(f"URLs interesantes")
    pdf.chapter_body(interesting_urls)

    # Capítulo: IPs
    pdf.chapter_break()
    pdf.chapter_title(f"IPs")
    pdf.chapter_body(ips)

    # Guardar el documento PDF
    pdf.output(f"output/{domain}.pdf")

    print(f"Se ha generado el PDF 'output/{domain}.pdf'.")
