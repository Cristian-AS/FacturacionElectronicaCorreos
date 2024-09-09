import os
import shutil
from dotenv import load_dotenv
from BOTS.CrearLogs import CrearCarpetaAdjuntos

load_dotenv()

# Obtener la ruta de las variables de entorno
RutaFacturacion = os.getenv('RutaFacturacion')

def limpiar_carpeta(carpeta):
    """ Elimina todos los archivos en la carpeta especificada. """
    for archivo in os.listdir(carpeta):
        archivo_path = os.path.join(carpeta, archivo)
        try:
            if os.path.isfile(archivo_path):
                os.remove(archivo_path)
            elif os.path.isdir(archivo_path):
                shutil.rmtree(archivo_path)
        except Exception as e:
            print(f"Error al eliminar {archivo_path}: {e}")

def get_info_message(path_root, message, sender):
    
    CreacionCarpetas = CrearCarpetaAdjuntos()
    
    download_path = os.path.join(path_root, 'adjuntos')
    
    FacturacionElectronica = os.path.join(RutaFacturacion, 'Contabilidad FacturacionE')
    Colaboracion = os.path.join(RutaFacturacion, 'Contabilidad Colaboracion')
    Provisiones = os.path.join(RutaFacturacion, 'Contabilidad Provisiones')

    # Limpiar la carpeta de adjuntos
    limpiar_carpeta(download_path)
    
    attachments = message.attachments
        
    # Verificar si el mensaje tiene algún adjunto
    if attachments:
        # Iterar a través de cada adjunto y guardarlo en la ruta especificada
        for attachment in attachments:
            attachment.save(download_path)
    
    # Definir un diccionario para las rutas de destino y sus claves de contador
    destino_rutas = {
        'COLABORACION': Colaboracion,
        'PROVISIONES': Provisiones,
        'FACTURACION ELECTRONICA': FacturacionElectronica
    }
    
    # Ruta del archivo de contadores
    contador_path = os.path.join(path_root, 'contadores.txt')

    # Leer el último número de los contadores, o inicializar a 1 si no existe
    if os.path.exists(contador_path):
        with open(contador_path, 'r') as f:
            contadores = {line.split(':')[0]: int(line.split(':')[1].strip()) for line in f}
    else:
        contadores = {clave: 1 for clave in destino_rutas.keys()}

    # Mover y renombrar los archivos a las carpetas correspondientes con numeración
    for file in os.listdir(download_path):
        movido = False
        for clave, destino in destino_rutas.items():
            if clave in file:
                print(clave)
                print(file)
                # Construir el nuevo nombre del archivo con el número consecutivo
                base_name, ext = os.path.splitext(file)
                nuevo_nombre = f"{base_name} {contadores[clave]}{ext}"
                
                # Definir las rutas completas para el archivo original y el nuevo destino
                old_file_path = os.path.join(download_path, file)
                new_file_path = os.path.join(destino, nuevo_nombre)
                
                # Verificar si el archivo ya existe en el destino y ajustar el nombre si es necesario
                while os.path.exists(new_file_path):
                    contadores[clave] += 1
                    nuevo_nombre = f"{base_name} {contadores[clave]}{ext}"
                    new_file_path = os.path.join(destino, nuevo_nombre)
                
                # Mover el archivo a la nueva carpeta
                shutil.move(old_file_path, new_file_path)
                
                # Incrementar el contador para la clave correspondiente
                contadores[clave] += 1
                
                print(f"Archivo movido: {file} a {nuevo_nombre} en {destino}")
                movido = True
                break
        if not movido:
            print(f"No se encontró una carpeta de destino para el archivo: {file}")
    
    # Guardar los contadores actualizados en el archivo de texto
    with open(contador_path, 'w') as f:
        for clave, numero in contadores.items():
            f.write(f"{clave}:{numero}\n")