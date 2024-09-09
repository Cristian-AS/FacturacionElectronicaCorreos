import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from BOTS.Credential import env_email

def error_correo(mensaje, sender):
    # Llamar funcion para cargar variables de entorno
    smtp_server, smtp_port, smtp_username, smtp_password = env_email()

    # Dirección de correo electrónico del remitente y destinatario
    from_email = 'correo.automatizacion@gruporeditos.com'
    #to_email = ['aprendiz.serviciosti@gruporeditos.com']
    to_email = ['aprendiz.funcional@gruporeditos.com']

    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ', '.join(to_email)
    msg['Subject'] = f'Error al procesar la Solictud de la Automatización Facturacion Electronica'

    # Contenido del correo (puede incluir HTML)
    body = f"""
    <html>
    <body>
        <p><strong>Cordial saludo</strong>,<br>
        <br>
        Ocurrió un error en la Solicitud del destinatario: {sender}<br>
        <br>
        Detalles del error: <br><br>{mensaje}<br>
        <br>
        Por favor no responder ni enviar correos de respuesta a la cuenta correo.automatizacion@gruporeditos.com.
        </p>
    </body>
    </html>
    """
    msg.attach(MIMEText(body, 'html'))

    # Iniciar sesión en el servidor SMTP y enviar correo
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Correo enviado correctamente")
    except Exception as e:
        print("Error al enviar el correo:", str(e))