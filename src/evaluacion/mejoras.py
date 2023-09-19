from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
import os, requests

def generar_report_mail(informe_data):
    # Ruta donde se guardará el archivo PDF
    output_path = 'output'
    pdf_filename = os.path.join(output_path, 'Informe_Infohunter.pdf')

    # Crear un archivo PDF
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # Definir colores personalizados
    colores = {
        'titulo': colors.darkblue,
        'subtitulo': colors.darkcyan,
        'parrafo': colors.black,
    }

    # Estilo de párrafo para los títulos
    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle(name='TituloStyle', fontSize=24, textColor=colores['titulo'])
    subtitulo_style = ParagraphStyle(name='SubtituloStyle', fontSize=16, textColor=colores['subtitulo'])

    # Estilo personalizado para los párrafos
    parrafo_style = ParagraphStyle(name='ParrafoStyle', fontSize=12, leading=14, textColor=colores['parrafo'])

    # Crear el contenido del informe
    contenido = []

    # Crear un estilo de párrafo personalizado para el título centrado
    titulo_centrado_style = ParagraphStyle(name='TituloCentradoStyle', fontSize=24, textColor=colores['titulo'], alignment=1)

    # Título centrado
    contenido.append(Paragraph('<font size="24" color="DarkBlue">Informe de Evaluación OSINT</font>', titulo_centrado_style))
    contenido.append(Spacer(1, 40))  # Aumentar el espacio vertical

    # Detalles de la evaluación con recuadros y más espacio vertical
    for item in informe_data:
        contenido.append(Paragraph('<b>Email:</b> {}'.format(item['Email']), parrafo_style))
        contenido.append(Paragraph('<b>Source:</b> {}'.format(item['Breaches']), parrafo_style))
        contenido.append(Paragraph('<b>Password:</b> {}'.format(item['Password']), parrafo_style))
        contenido.append(Paragraph('<b>Nivel de Criticidad:</b> {}'.format(item['Nivel de Criticidad']), parrafo_style))
    
        # Identar las recomendaciones
        recomendaciones = item['Recomendaciones']  # Obtener la lista de recomendaciones
        contenido.append(Paragraph('<b>Recomendaciones:</b>', parrafo_style))
        #contenido.append(Spacer(1, 5))  # Aumentar el espacio vertical
        for recomendacion_info in recomendaciones:
            recomendacion = recomendacion_info["recomendacion"]
            
            # Formatear la recomendación con el impacto
            recomendacion_formateada = f'&nbsp;&nbsp;&nbsp;&nbsp;- {recomendacion}'
            
            # Agregar la recomendación al contenido del informe
            contenido.append(Paragraph(recomendacion_formateada, parrafo_style))
            contenido.append(Paragraph(f'&nbsp;&nbsp;&nbsp;&nbsp;Nivel de Impacto: {recomendacion_info["impacto"]}', parrafo_style))

            contenido.append(Spacer(1, 5))  # Aumentar el espacio vertical
        contenido.append(Spacer(1, 10))  # Aumentar el espacio vertical

    # Construir el PDF
    doc.build(contenido, onFirstPage=add_header, onLaterPages=add_header)

def generar_report_username(datos_importantes):
    # Ruta donde se guardará el archivo PDF
    output_path = 'output'
    pdf_filename = os.path.join(output_path, 'Informe_OSINT.pdf')

    # Crear un archivo PDF
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # Definir colores personalizados
    colores = {
        'titulo': colors.darkblue,
        'subtitulo': colors.darkcyan,
        'parrafo': colors.black,
    }

    # Estilo de párrafo para los títulos
    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle(name='TituloStyle', fontSize=24, textColor=colores['titulo'])
    subtitulo_style = ParagraphStyle(name='SubtituloStyle', fontSize=16, textColor=colores['subtitulo'])

    # Estilo personalizado para los párrafos
    parrafo_style = ParagraphStyle(name='ParrafoStyle', fontSize=12, leading=14, textColor=colores['parrafo'])

    # Estilo personalizado para el texto en negrita
    negrita_style = ParagraphStyle(name='NegritaStyle', fontSize=12, leading=14, textColor=colores['parrafo'], fontName='Helvetica-Bold')

    # Crear el contenido del informe
    contenido = []

    # Crear un estilo de párrafo personalizado para el título centrado
    titulo_centrado_style = ParagraphStyle(name='TituloCentradoStyle', fontSize=24, textColor=colores['titulo'], alignment=1)

    # Título centrado
    contenido.append(Paragraph('<font size="24" color="DarkBlue">Informe de Evaluación OSINT</font>', titulo_centrado_style))
    contenido.append(Spacer(1, 40))  # Aumentar el espacio vertical

    # Recorrer los datos importantes y agregarlos al informe
    for red_social, detalles in datos_importantes.items():
        # Título de la red social
        contenido.append(Paragraph(f'{red_social}', subtitulo_style))
        contenido.append(Spacer(1, 10))  # Aumentar el espacio vertical

        # Estado y URL del usuario
        contenido.append(Paragraph(f'<b>Username:</b> {detalles["status"]["username"]}', parrafo_style))
        contenido.append(Paragraph(f'<b>URL del Usuario:</b> {detalles["url_user"]}', parrafo_style))

        # Nivel Crítico
        contenido.append(Paragraph(f'<b>Nivel Crítico:</b> {detalles["nivel_critico"]}', parrafo_style))

        # IDs (si está disponible)
        ids = detalles["status"].get("ids")
        if ids:
            contenido.append(Paragraph('<b>IDs:</b>', parrafo_style))
            for key, value in ids.items():
                contenido.append(Paragraph(f'&nbsp;&nbsp;&nbsp;&nbsp;{key}: {value}', parrafo_style))

        try:
            # Imagen (si está disponible)
            imagen_url = detalles["status"]["ids"].get("image")
            response = requests.get(imagen_url)
            if response.status_code == 200:
                # Convertir la respuesta en un objeto de imagen de BytesIO
                imagen_bytesio = BytesIO(response.content)
                
                # Cargar la imagen desde BytesIO
                imagen = Image(imagen_bytesio, width=100, height=100)
    
                # Agregar la imagen al contenido del informe
                contenido.append(imagen)
            #if imagen_url:
            #    imagen = Image(imagen_url, width=100, height=100)
            #    contenido.append(imagen)
        except:
            pass
    
        # Recomendaciones
        #contenido.append(Spacer(1, 5))  # Aumentar el espacio vertical
        contenido.append(Paragraph('<b>Recomendaciones:</b>', parrafo_style))
        contenido.append(Spacer(1, 5))  # Aumentar el espacio vertical
        for recomendacion_info in detalles['recomendaciones']:
            recomendacion = recomendacion_info["recomendacion"]
            impacto = recomendacion_info["impacto"]
            # Identar la recomendación
            recomendacion_formateada = '&nbsp;&nbsp;&nbsp;&nbsp;- {}'.format(recomendacion)
            contenido.append(Paragraph(f' {recomendacion_formateada}', parrafo_style))
            contenido.append(Paragraph(f'&nbsp;&nbsp;&nbsp;&nbsp;Nivel de Impacto: {impacto}', parrafo_style))
            contenido.append(Spacer(1, 5))  # Aumentar el espacio vertical


        contenido.append(Spacer(1, 20))  # Aumentar el espacio vertical

    # Construir el PDF
    #doc.build(contenido)
    doc.build(contenido, onFirstPage=add_header, onLaterPages=add_header)

    
    # Función para crear el footer
def add_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    page_num_text = f'Página {doc.page}'
    page_width = letter[0]
    canvas.drawString(page_width - inch, 0.75 * inch, page_num_text)
    canvas.restoreState()
    
    
def add_header(canvas, doc):
    text = "InfoHUnter"
    canvas.setFont("Helvetica", 9)
    text_width = canvas.stringWidth(text, "Helvetica", 9)
    canvas.drawString(letter[0] - inch - text_width, letter[1] - 0.75 * inch, text)

