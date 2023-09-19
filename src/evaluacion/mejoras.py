from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
import os, requests, json

def generar_report_mail(informe_data):
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

def generar_report_domain(data,domain):
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
    titulo_seccion_style = ParagraphStyle(name='TituloSeccionStyle', fontSize=16, textColor=colors.darkblue, alignment=0)

    # Estilo personalizado para los párrafos
    parrafo_style = ParagraphStyle(name='ParrafoStyle', fontSize=12, leading=14, textColor=colores['parrafo'])

    # Crear el contenido del informe
    contenido = []

    # Crear un estilo de párrafo personalizado para el título centrado
    titulo_centrado_style = ParagraphStyle(name='TituloCentradoStyle', fontSize=24, textColor=colores['titulo'], alignment=1)

    # Título centrado
    contenido.append(Paragraph('<font size="24" color="DarkBlue">Informe de Evaluación OSINT</font>', titulo_centrado_style))
    contenido.append(Spacer(1, 40))  # Aumentar el espacio vertical

    # Agregar información de PyHunter
    contenido.append(Paragraph('<b>Dominio:</b> {}'.format(data['domain']), parrafo_style))
    contenido.append(Paragraph('<b>Nombre de la Organización:</b> {}'.format(data['organization']), parrafo_style))
    contenido.append(Paragraph('<b>Descripción:</b> {}'.format(data['description']), parrafo_style))
    contenido.append(Paragraph('<b>Industria:</b> {}'.format(data['industry']), parrafo_style))
    contenido.append(Paragraph('<b>País:</b> {}'.format(data['country']), parrafo_style))
    contenido.append(Paragraph('<b>Ciudad:</b> {}'.format(data['city']), parrafo_style))
    contenido.append(Paragraph('<b>Código Postal:</b> {}'.format(data['postal_code']), parrafo_style))
    contenido.append(Paragraph('<b>Dirección:</b> {}'.format(data['street']), parrafo_style))

    contenido.append(Spacer(1, 20))  # Aumentar el espacio vertical

    # Agregar información de contacto
    contenido.append(Paragraph('<b>Información de Contacto:</b>', subtitulo_style))
    contenido.append(Spacer(1, 10))  # Aumentar el espacio vertical
    for email_info in data['emails']:
        contenido.append(Paragraph('<b>Nombre:</b> {} {}'.format(email_info['first_name'], email_info['last_name']), parrafo_style))
        contenido.append(Paragraph('<b>Email:</b> {}'.format(email_info['value']), parrafo_style))
        contenido.append(Paragraph('<b>Confianza:</b> {}%'.format(email_info['confidence']), parrafo_style))
        contenido.append(Paragraph('<b>Origen:</b> {}'.format(email_info['sources'][0]['domain']), parrafo_style))
        # Agregar información de redes sociales si está disponible
        if email_info.get('linkedin'):
            contenido.append(Paragraph('<b>LinkedIn:</b> <a href="{}">{}</a>'.format(email_info['linkedin'], email_info['linkedin']), parrafo_style))
        if email_info.get('twitter'):
            contenido.append(Paragraph('<b>Twitter:</b> <a href="{}">{}</a>'.format(email_info['twitter'], email_info['twitter']), parrafo_style))
        # Agregar información de teléfono si está disponible
        if email_info.get('phone_number'):
            contenido.append(Paragraph('<b>Teléfono:</b> {}'.format(email_info['phone_number']), parrafo_style))
        contenido.append(Spacer(1, 10))  # Aumentar el espacio vertical

    # Agregar enlaces a redes sociales de la organización
    contenido.append(Paragraph('<b>Enlaces a Redes Sociales de la Organización:</b>', subtitulo_style))
    contenido.append(Spacer(1, 10))  # Aumentar el espacio vertical
    if data['twitter']:
        contenido.append(Paragraph('<b>Twitter:</b> <a href="{}">{}</a>'.format(data['twitter'], data['twitter']), parrafo_style))
    if data['facebook']:
        contenido.append(Paragraph('<b>Facebook:</b> {}'.format(data['facebook']), parrafo_style))
    if data['linkedin']:
        contenido.append(Paragraph('<b>LinkedIn:</b> <a href="{}">{}</a>'.format(data['linkedin'], data['linkedin']), parrafo_style))
    if data['instagram']:
        contenido.append(Paragraph('<b>Instagram:</b> {}'.format(data['instagram']), parrafo_style))
    if data['youtube']:
        contenido.append(Paragraph('<b>YouTube:</b> {}'.format(data['youtube']), parrafo_style))

    # Agregar un salto de página para separar las páginas
    contenido.append(PageBreak())

    contenido.append(Spacer(1, 40))  # Aumentar el espacio vertical
    # Recomendaciones generales
    contenido.append(Paragraph('Recomendaciones Generales:', subtitulo_style))
    contenido.append(Spacer(1, 10))  # Aumentar el espacio vertical

    recomendaciones_generales = [
        {"recomendacion": "Verificación de Datos: Siempre verifica la precisión de la información antes de utilizarla para tomar decisiones importantes. Los datos pueden volverse obsoletos o inexactos con el tiempo.", "impacto": "Medio"},
        {"recomendacion": "Uso Responsable: Utiliza la información de manera ética y legal. No la utilices para fines maliciosos, como el phishing o la suplantación de identidad.", "impacto": "Alto"},
        {"recomendacion": "Seguridad de Datos: Si manejas datos personales, asegúrate de seguir las mejores prácticas de seguridad de datos para proteger la información de posibles brechas de seguridad.", "impacto": "Alto"},
    ]
    
    for recomendacion_info in recomendaciones_generales:
        recomendacion = recomendacion_info["recomendacion"]
        impacto = recomendacion_info["impacto"]
        contenido.append(Paragraph(f'{recomendacion} (Impacto: {impacto})', parrafo_style))
        contenido.append(Spacer(1, 10))  # Aumentar el espacio vertical

    contenido.append(Spacer(1, 40))  # Aumentar el espacio vertical
    # Recomendaciones específicas
    contenido.append(Paragraph('Recomendaciones Específicas:', subtitulo_style))
    contenido.append(Spacer(1, 10))  # Aumentar el espacio vertical

        
    recomendaciones_especificas = [
        {"recomendacion": "Redes Sociales: Revisa la configuración de privacidad en tus cuentas de redes sociales y ajusta la visibilidad de tus perfiles y publicaciones según tu preferencia.", "impacto": "Medio"},
        {"recomendacion": "Contraseñas Seguras: Utiliza contraseñas seguras y cámbialas regularmente. Habilita la autenticación de dos factores (2FA) cuando esté disponible para mejorar la seguridad de tus cuentas.", "impacto": "Alto"},
        {"recomendacion": "Compartir Datos Personales: Evita compartir información personal o sensible en tus publicaciones en línea. Protege tu privacidad.", "impacto": "Medio"},
        {"recomendacion": "Aplicaciones de Terceros: Ten cuidado al autorizar aplicaciones de terceros en tus cuentas de redes sociales. Verifica su reputación antes de conceder acceso.", "impacto": "Medio"},
        {"recomendacion": "Actividad de Cuenta: Revisa periódicamente la actividad en tus cuentas y ajusta la configuración de notificaciones para un mayor control.", "impacto": "Bajo"},
        {"recomendacion": "Mensajes Sospechosos: Sé escéptico ante los mensajes sospechosos que recibas y no hagas clic en enlaces no verificados.", "impacto": "Alto"},
    ]

    for recomendacion_info in recomendaciones_especificas:
        recomendacion = recomendacion_info["recomendacion"]
        impacto = recomendacion_info["impacto"]
        contenido.append(Paragraph(f'{recomendacion} (Impacto: {impacto})', parrafo_style))
        contenido.append(Spacer(1, 10))  # Aumentar el espacio vertical
        
    # Cargar la información de TheHarvester
    theharvester_data = cargar_theharvester_json(domain)
    
    # Verificar si se cargó exitosamente
    if theharvester_data:
        
        # Agregar un salto de página para separar las secciones
        contenido.append(PageBreak())
        
        # Agregar contenido del JSON de TheHarvester
        contenido.append(Paragraph("Información de TheHarvester:", styles['Heading2']))
        
        # Agregar información de ASNs
        contenido.append(Paragraph("ASNs:", titulo_seccion_style))
        contenido.append(Spacer(1, 10))  # Aumentar el espacio vertical
        contenido.append(Paragraph(', '.join(theharvester_data['asns']), parrafo_style))
        contenido.append(Spacer(1, 20))  # Aumentar el espacio vertical
        
        # Agregar información de Emails
        contenido.append(Paragraph("Emails:", titulo_seccion_style))
        contenido.append(Spacer(1, 10))  # Aumentar el espacio vertical
        contenido.append(Paragraph(', '.join(theharvester_data['emails']), parrafo_style))
        contenido.append(Spacer(1, 20))  # Aumentar el espacio vertical
        
        # Agregar información de Hosts
        contenido.append(Paragraph("Hosts:", titulo_seccion_style))
        contenido.append(Spacer(1, 10))  # Aumentar el espacio vertical
        contenido.append(Paragraph(', '.join(theharvester_data['hosts']), parrafo_style))
        contenido.append(Spacer(1, 20))  # Aumentar el espacio vertical

        
        # Agregar información de URLs interesantes
        contenido.append(Paragraph("URLs Interesantes:", titulo_seccion_style))
        contenido.append(Spacer(1, 10))  # Aumentar el espacio vertical
        contenido.append(Paragraph(', '.join(theharvester_data['interesting_urls']), parrafo_style))
        contenido.append(Spacer(1, 20))  # Aumentar el espacio vertical

        
        # Agregar información de IPs
        contenido.append(Paragraph("IPs:", titulo_seccion_style))
        contenido.append(Spacer(1, 10))  # Aumentar el espacio vertical
        contenido.append(Paragraph(', '.join(theharvester_data['ips']), parrafo_style))
        contenido.append(Spacer(1, 20))  # Aumentar el espacio vertical

        
        # Agregar información de Shodan
        contenido.append(Paragraph("Shodan:", titulo_seccion_style))
        contenido.append(Spacer(1, 10))  # Aumentar el espacio vertical
        contenido.append(Paragraph(', '.join(theharvester_data['shodan']), parrafo_style))
        contenido.append(Spacer(1, 40))  # Aumentar el espacio vertical

    else:
        contenido.append(Paragraph("No se encontró información de TheHarvester para el dominio proporcionado.", parrafo_style))

    recomendaciones_theharvester = [
        {"recomendacion": "ASNs: Investiga y verifica la seguridad de los ASNs asociados a tu dominio.", "impacto": "Alto"},
        {"recomendacion": "Emails: Asegúrate de que los correos electrónicos asociados a tu dominio sean seguros y estén protegidos contra phishing.", "impacto": "Alto"},
        {"recomendacion": "Hosts: Realiza un análisis de seguridad en los hosts utilizados por tu dominio para detectar posibles vulnerabilidades.", "impacto": "Medio"},
        {"recomendacion": "URLs Interesantes: Verifica la seguridad de las URLs que has identificado como interesantes para tu dominio.", "impacto": "Medio"},
        {"recomendacion": "IPs: Asegúrate de que las IPs asociadas a tu dominio estén bien configuradas y protegidas contra ataques.", "impacto": "Alto"},
        {"recomendacion": "Shodan: Monitorea regularmente Shodan para asegurarte de que no haya información sensible expuesta públicamente.", "impacto": "Bajo"},
    ]

    # Recomendaciones específicas
    contenido.append(Paragraph('Recomendaciones Específicas:', subtitulo_style))
    contenido.append(Spacer(1, 10))  # Aumentar el espacio vertical

   
    for recomendacion_info in recomendaciones_theharvester:
        recomendacion = recomendacion_info["recomendacion"]
        impacto = recomendacion_info["impacto"]
        contenido.append(Paragraph(f'{recomendacion} (Impacto: {impacto})', parrafo_style))
        contenido.append(Spacer(1, 10))  # Aumentar el espacio vertical

    # Construir el PDF
    doc.build(contenido, onFirstPage=add_header, onLaterPages=add_header)
def addfooter(canvas, doc):
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

def cargar_theharvester_json(domain):
    # Construir la ruta del archivo JSON
    ruta_json = f'output/{domain}.json'

    # Verificar si el archivo JSON existe
    if os.path.exists(ruta_json):
        # Cargar el archivo JSON de TheHarvester
        with open(ruta_json, 'r') as json_file:
            theharvester_data = json.load(json_file)
        return theharvester_data
    else:
        print("No existe el fichero"+ruta_json)
        return None