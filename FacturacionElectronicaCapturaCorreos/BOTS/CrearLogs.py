import os

path_root = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(path_root)

def crear_log_error():
    # Definir la ruta de la carpeta de log
    log_path = os.path.join(parent_dir, 'Console_log')

    # Crear la carpeta de log si no existe
    if not os.path.exists(log_path):
        os.mkdir(log_path)
        print(f"Se ha creado la carpeta de log en {log_path}")

    return log_path

def CrearCarpetaAdjuntos():
    # Definir la ruta de la carpeta de log
    log_path = os.path.join(parent_dir, 'adjuntos')

    # Crear la carpeta de log si no existe
    if not os.path.exists(log_path):
        os.mkdir(log_path)
        print(f"Se ha creado la carpeta de log en {log_path}")

    return log_path