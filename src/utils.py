# -*- coding: utf-8 -*-********************
import zipfile
import traceback
import time
import csv
import sys
import os

"""
    Clase que implementa funciones de utilidad
    - Descomprensión de ficheros
    - Espera hasta que finaliza la descarga de ficheros
    - Escritura y lectura de ficheros csv
    - Borrado de ficheros
"""
class Utils:
    # Utilities
    # Permite la descomprensión de un fichero, desde un directorio origen a un directorio destino
    def upzip_file(self, path_to_zip_file, directory_to_extract_to):
        """ Descomprime un fichero zip
        Parameters
        ----------
        path_to_zip_file: str, mandatory
            Path del fichero a ser descomprimido
        directory_to_extract_to: str, mandatory
            Directorio donde ha de realizarse la descompresión            
        """
        try:
            zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
            zip_ref.extractall(directory_to_extract_to)
            zip_ref.close()            
        except Exception:
            traceback.print_exc()
            raise Exception('Error en Utils.upzip_file')             
    
    def wait_until_file_is_download(self, file_path, time_to_wait, count_until_filepart_cre, count_until_filepart_del):
        """ Espera el fichero suministrado como parámetro en file_path ha sido descargado por Firefox
        Para evitar una espera infinita, en caso de que nunca llegue a existir el fichero se usa time_counter,
        como mucho se esperaran time_to_wait*time_counter segundos, antes de descartar la existencia del fichero.   
        Se retorna true, si se localiza el fichero tras la espera, y false en caso contrario
        
        Parameters
        ----------
        file_path: str, mandatory
            Path del fichero a ser descargado
        time_to_wait: int, mandatory
            Tiempo a esperar entre verificaciones de la existencia de el fichero <download_file>.part
        count_until_filepart_cre: int, mandatory
            Número de veces a esperar por la aparicicón del fichero <download_file>.part
        count_until_filepart_del: int, mandatory
            Número de veces a esperar por la desaparición del fichero <download_file>.part        
        """
        try:
            # nombre del fichero temporal que indica que la descarga sigue activca
            file_part_path = file_path+'.part'
            counter = 0
            # se realiza un bucle esperando hasta que el fichero .part exista
            print("  * Waiting for file: "+file_part_path)
            while not os.path.exists(file_part_path):
                sys.stdout.write('.')
                time.sleep(time_to_wait)
                counter += 1
                if counter > count_until_filepart_cre:
                    break
            sys.stdout.write('\n')
            
            # se realiza un bucle esperando hasta que el fichero .part desaparezca
            print("  * Waiting for deleting file: "+file_part_path) 
            while os.path.exists(file_part_path):
                sys.stdout.write('.')
                time.sleep(time_to_wait)
                counter += 1
                if counter > count_until_filepart_del:
                    break        
            sys.stdout.write('\n')
            
            # se verifica si el fichero ha sido descargado satisfactoriamente   
            if os.path.exists(file_path) and not os.path.exists(file_part_path):
                print("  * "+file_path+" Downloaded")
                return True
            else:
                print("  * "+file_path+" NOT Downloaded!!!!!!!!!")
                return False            
        except Exception:
            traceback.print_exc()
            raise Exception('Error en Utils.wait_until_file_is_download') 

    def deleteIfExist(self, file_path):
        """ Elimina el fichero suministrado como parámetro, en caso de existir
        Parameters
        ----------
        file_path: str, mandatory
            Path del fichero a eliminar      
        """
        try:
            exists = os.path.isfile(file_path)
            if exists:
                os.remove(file_path)           
        except Exception:
            traceback.print_exc()
            raise Exception('Error en Utils.deleteIfExist')             

    def write2DArrayToCsv(self, twoDimensionArray, file_csv_path, delimiter):
        """ Vuelca un array de dos dimensiones a fichero csv
        Parameters
        ----------
        twoDimensionArray: array, mandatory
            Array de dos dimensiones con los registros que representan a cada informe ipp
        file_csv_path: str, mandatory
            Path del fichero csv a escribir
        delimiter: array, mandatory
            Delimitador a usar entre los campos de cada fila            
        """
        try:
            f = open(file_csv_path, 'a')
            for item in twoDimensionArray:
                f.write(delimiter.join([str(x) for x in item]) + '\n')
            f.close()            
        except Exception:
            traceback.print_exc()
            raise Exception('Error en Utils.write2DArrayToCsv')            
            
    def loadCsvTo2DArray(self, path_to_csv, delimiter = ","):
        """ Carga un array de dos dimensiones con el contenido del fichero csv
        cuyo path se suminitra como parámetro.
        Parameters
        ----------
        path_to_csv: str, mandatory
            Path fichero csv a ser cargado
        delimiter: str, optional ("," by default)
            Valor del delimitador entre campos
        """
        try:
            with open(path_to_csv ) as csv_file:
                data_iter = csv.reader(csv_file,
                                       delimiter = delimiter,
                                       quotechar = '"')
                data = [data for data in data_iter]                
                return data
        except Exception:
            traceback.print_exc()
            raise Exception('Error en Utils.losCsvTo2DArray')         