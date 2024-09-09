from Connection.get_data import get_datos_id

def env_email():
    
    data = get_datos_id('1')
    
    # Extraer las variables del objeto data para el envío de correos
    smtp_server = data['server_smtp']
    smtp_port = data['port_smtp']
    smtp_username = data['user_smtp']
    smtp_password = data['pass_smtp']
    
    return smtp_server, smtp_port, smtp_username, smtp_password