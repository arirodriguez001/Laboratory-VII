import os
import subprocess

# Obtener el directorio local actual
directory = os.getcwd()

# Ruta al ejecutable de ANGEL
angel_executable = r'C:\phits\bin\angel_win.exe'  # Cambia por la ruta real al ejecutable de ANGEL

def enviar_archivos_a_angel(directory, angel_executable):
    # Recorremos todos los archivos en el directorio
    for filename in os.listdir(directory):
        # Filtrar archivos con extensión .out, excluyendo batch.out y phits.out
        if filename.endswith('.out') and filename not in ['batch.out', 'phits.out']:
            filepath = os.path.join(directory, filename)

            # Mostrar mensaje informativo al iniciar el procesamiento
            print(f"ANGEL calculation for {filename} is started")

            # Crear un archivo temporal para los argumentos
            temporary_filename = 'angel_temporary.ang'
            with open(temporary_filename, 'w') as temp_file:
                # Escribir el nombre del archivo .out en el archivo temporal
                temp_file.write(f"{filepath}\n")

            try:
                # Eliminar archivo de error si existe
                if os.path.exists('error.ang'):
                    os.remove('error.ang')

                # Ejecutar el comando y enviar el archivo a ANGEL
                command = [angel_executable, '<', temporary_filename]  # Usar '<' para redirigir entrada

                # Ejecutar el comando en la consola (pasa el archivo temporal a ANGEL)
                result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                # Mostrar el resultado del procesamiento
                print(f"Processed {filename} successfully. Output:\n{result.stdout.decode('utf-8')}")
            except subprocess.CalledProcessError as e:
                print(f"Error processing {filename}. Error:\n{e.stderr.decode('utf-8')}")
            finally:
                # Limpiar cualquier archivo temporal si es necesario
                if os.path.exists(temporary_filename):
                    os.remove(temporary_filename)

if __name__ == "__main__":
    enviar_archivos_a_angel(directory, angel_executable)
