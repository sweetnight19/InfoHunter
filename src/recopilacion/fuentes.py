import sys
import os

def obtener_informacion_redes_sociales(nombre: str):
    # Verificar el sistema operativo
    if sys.platform.startswith('linux'):
        # Llamada al sistema en Linux
        comando = "python src/sherlock/sherlock/sherlock.py -fo output "+nombre
    else:
        # Llamada al sistema en otros sistemas operativos
        comando = "python src\sherlock\sherlock\sherlock.py -fo output "+nombre
    
    # Ejecutar el comando y capturar la salida
    os.system(comando)