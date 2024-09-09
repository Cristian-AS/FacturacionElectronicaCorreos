import os, sys
from O365 import Account, FileSystemTokenBackend
from datetime import datetime
import Connection.get_data as get_data
from Messages.ObtenerInfoCorreo import get_info_message
from BOTS.ErrorCorreo import error_correo
from BOTS.CrearLogs import crear_log_error


original_stdout = sys.stdout

# Obtener la fecha y hora actual
now = datetime.now()

# Formatear la fecha y la hora como una cadena
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

# Definir la ruta del archivo de console log
log_path = crear_log_error()

with open(os.path.join(log_path, f'LOGS - Facturacion Correos -{timestamp}.txt'), 'a') as f:
    sys.stdout = f # Cambiar la salida estándar al archivo que acabamos de abrir

    # Obtener las variables de entorno
    data = get_data.get_datos_id('1')

    # Extraer las variables del objeto data
    client_id = data['client_id']
    client_secret = data['secret_id']
    tenant_id_ = data['tenant_id']

    # Definir ruta relativa de trabajo de la Automatización
    path_root = os.path.dirname(os.path.abspath(__file__))

    # Definir credenciales de acceso a la cuenta de correo
    credentials = (client_id, client_secret)

    # Construir la ruta del archivo de token relativa a la raíz del proyecto
    token_path = os.path.join(path_root, 'o365_token.txt')
    token_backend = FileSystemTokenBackend(token_path=token_path)
    account = Account(credentials, tenant_id=tenant_id_, token_backend=token_backend)

    # Iniciar sesión en la cuenta de correo
    if not account.is_authenticated:  # No almacenamos el token o el token ha expirado
        if account.authenticate(scopes=['basic', 'message_all']):
            print('Autenticado correctamente y token almacenado.')
        else:
            print('Error de autenticación')
    else:
        print('Autenticación exitosa utilizando el token almacenado.')

    # obtener los mensajes de la bandeja
    if account.is_authenticated:
        # Obtener mensajes de la bandeja de entrada no leídos
        message = account.mailbox().get_folder(folder_name='Contabilidad Facturacion').get_messages(query='isRead eq false', download_attachments=True)
        
    # Listar mensajes
    messages = list(message)

    # Si hay mensajes en la bandeja de entrada
    if len(messages) > 0:
        for message in messages:
            # Obtener asunto del mensaje
            subject = message.subject
            # Obtener cuerpo del mensaje
            body = message.get_body_text()
            # Obtener remitente del mensaje
            sender = message.sender.address
            
            # Llamar a la función para extraer la información del mensaje
            try:
                get_info_message(path_root, message, sender)
            except ValueError as e:
                print(error_correo(str(e), sender))
            
            # Marcar mensaje como leído
            message.mark_as_read()
    else:
        print("No hay mensajes en la bandeja de entrada")
    
    sys.stdout = original_stdout # Restaurar la salida estándar original