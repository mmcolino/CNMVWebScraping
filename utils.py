# -*- coding: utf-8 -*-********************
import zipfile
import csv
import time
import os

"""
    Clase que implementa funciones de utilidad
    - Descomprensión de ficheros
    - Espera hasta que finaliza la descarga de ficheros
"""
class Utils:
    # Utilities
    # Permite la descomprensión de un fichero, desde un directorio origen a un directorio destino
    def upzip_file(self, path_to_zip_file, directory_to_extract_to):
        zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
        zip_ref.extractall(directory_to_extract_to)
        zip_ref.close()
    
    # Espera el fichero suministrado como parámetro en file_path ha sido descargado por Firefox
    # Para evitar una espera infinita, en caso de que nunca llegue a existir el fichero se usa time_counter,
    # como mucho se esperaran time_to_wait*time_counter segundos, antes de descartar la existencia del fichero.   
    # Se retorna true, si se localiza el fichero tras la espera, y false en caso contrario
    def wait_until_file_is_download(self, file_path, time_to_wait, count_until_filepart_cre, count_until_filepart_del):
        # nombre del fichero temporal que indica que la descarga sigue activca
        file_part_path = file_path+'.part'
        print("wait_until_file_exist - Step 1: "+file_part_path)
        print(file_path)
        counter = 0
        # se realiza un bucle esperando hasta que el fichero .part exista
        while not os.path.exists(file_part_path):
            print("wait_until_file_part_exist - Step 2.1")
            print('En bucle: '+str(counter))
            time.sleep(time_to_wait)
            counter += 1
            if counter > count_until_filepart_cre:
                break
            
        # se realiza un bucle esperando hasta que el fichero .part desaparezca
        while os.path.exists(file_part_path):
            print("wait_until_file_part_not_exist - Step 2.2")
            print('En bucle: '+str(counter))
            time.sleep(time_to_wait)
            counter += 1
            if counter > count_until_filepart_del:
                break        
            
        # al salir del bucle para asegurarnos esperamos un poco más    
        if os.path.exists(file_path) and not os.path.exists(file_part_path):
            print("wait_until_file_exist - Step 4.1")
            return True
        else:
            print("wait_until_file_exist - Step 4.2")
            return False

    # Vuelca un array de dos dimensiones a fichero csv
    def write2DArrayToCsv(self, twoDimensionArray, file_csv_path, delimiter):
        with open(file_csv_path,"w+") as my_csv:
            csvWriter = csv.writer(my_csv,delimiter=delimiter)
            csvWriter.writerows(twoDimensionArray)
    