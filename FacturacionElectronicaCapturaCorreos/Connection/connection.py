import pyodbc, os
from dotenv import load_dotenv

def connection():
    
    # Cargar las variables de entorno desde el archivo .env
    load_dotenv()
    
    # Obtener las credenciales de las variables de entorno
    server = os.getenv('SERVER')
    database = os.getenv('DATABASE')
    
    # Construir cadena de conexión
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    
    try:
        conn = pyodbc.connect(connection_string)
        print("Conexión exitosa a la base de datos.")
        return conn
    except pyodbc.Error as ex:
        print("Error al conectar a la base de datos:", ex)
        return None