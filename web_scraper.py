# -*- coding: utf-8 -*-

# Importar librerías requeridas
# https://docs.python.org
# Ejemplo - http://pythonpiura.org/posts/2016/01/25/web-scraping-con-selenium/
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

from utils import Utils
import traceback
import os

# Inicializar elementos requeridos
utils = Utils()

class WebScraper():
    """
    Clase que implementa la funcionalidad de scraping para los informes IPP publicados en la CNMV
    http://cnmv.es/ipps/
    """     
    def __init__(self, wsPreferences):  
        """ Constructor de la clase, recibe como parámetro las preferencias configurables 
        Parameters
        ----------
        wsPreferences: dictionary, mandatory
            Objeto de tipo dictionary que define las preferencias a ser confiuradas de acuerdo 
            a las características del scraping que va a ser realizado, y del entorno de ejecución.
            Las claves que se corresponden con cada propiedad a configurar se listan a continuación,
            divididas por tipo de configuración:
                * Configuración web driver
                    - selenium_firefox_path
                        Configurarion para el driver firefox, indica la ruta al ejecutable de Firefox
                    - selenium_firefox_driver (Configuración web driver)
                        Configurarion para el driver firefox, indica la ruta al driver de Selenium para Firefox
                * Configuración persistencia descarga de ficheros IPP xbrl
                    - xbrl_ipp_url
                        Url donde se encuentran los informes ipp xbrl publicados por la CNVM
                    - xbrl_download_dir
                        Configuración ubicación donde se ha de realizar la descarga de los ficheros zip que contienen 
                        los ficheros XBRL para una página de resultados.
                    - xbrl_extract_dir
                        Configuración directorio donde se descombrimirán y ubicarán los ficheros xbrl resultantes de 
                        la descompresión del zip previo.
                * Configuración tiempos de espera por descarga de ficheros xbrl.
                    Se requerirá configurar una serie de parámetros para parametrizar el comportamiento de la función de 
                    espera hasta que una determinada descarga de fichero ha sido realizada.
                    Como máximo se esperará: 
                        xbrl_download_time_to_wait * xbrl_download_count_until_filepart_cre * xbrl_download_count_until_filepart_del
                    - xbrl_download_time_to_wait
                        Tiempo a esperar entre verificaciones de la existencia de el fichero <download_file>.part
                    - xbrl_download_count_until_filepart_cre
                        Número de veces a esperar por la aparicicón del fichero <download_file>.part
                    - xbrl_download_count_until_filepart_del
                        Número de veces a esperar por la desaparición del fichero <download_file>.part
                
        """
        try:
            # Configuración web driver
            self.selenium_firefox_path = wsPreferences['selenium_firefox_path']
            self.selenium_firefox_driver = wsPreferences['selenium_firefox_driver']
            # Configuración del origen de datos
            self.xbrl_ipp_url = wsPreferences['xbrl_ipp_url']
            # Configuración persistencia descarga de ficheros IPP xbrl
            self.xbrl_download_dir = wsPreferences['xbrl_download_dir']
            self.xbrl_extract_dir = wsPreferences['xbrl_extract_dir']
            # Configuración tiempos de espera por descarga de ficheros xbrl
            self.xbrl_download_time_to_wait = wsPreferences['xbrl_download_time_to_wait']
            self.xbrl_download_count_until_filepart_cre = wsPreferences['xbrl_download_count_until_filepart_cre']
            self.xbrl_download_count_until_filepart_del = wsPreferences['xbrl_download_count_until_filepart_del']
        except Exception:
            traceback.print_exc()          
            raise Exception('Error WebScrapper.__init__.')  

    def load_sector_data(self, sectorDictionary, sectorId, period):
        """ Realiza la carga de los informes IPP xbrl para el sector identificado y el periodo identificado
        Parameters
        ----------
        sectorDictionary: dictionary, mandatory
            Mapa con la clave de cada sector y nombre asociado al mismo
        sectorId: str, mandatory
            Identificador de sector para el que se desean cargar los datos
        period: int, mandatory
            Año que identifica el periodo para el que se desean cargar los datos
        
        Returns
        -------
        data: array 2 dimensiones, con los datos de los informes recuperados
        False: 
            si no se ha logrado descargar y descomprimir los ficheros xbrl se retorna
            False indicando que la extracción de los datos del sector y periodo no ha
            podido ser realizada satisfactoriametne
        """
        # Inicializar objeto contenedor de los datos a ser retornados
        result = None
        try:
            # Inicializaliza el webdriver de Selenium que va a ser usado para realizar el scraping
            self.__init_webdriver()
            
            # Realizar la petición de la página a la que queremos acceder
            self.__load_page(self.xbrl_ipp_url)
            
            # Realiza la búsqueda y recuperacón de los datos para el sector y el periodo específicados
            self.__retrieve_data(sectorId, period)

            # Procesa el resultado obtenido tras la búsqueda y recuperación de datos
            result = self.__process_result(sectorId, sectorDictionary);
        except Exception:
            traceback.print_exc()
            result = False
        finally:
            # Se finaliza el driver inicializado
            self.driver.close()
            return result
        
    def __decompress_ipp_xbrl_data(self):
        """ Realiza la decompresión de los ficheros .zip con los informes IPP xbrl descargados,
            dejando el resultado en el directorio de extración de xbrl's 'xbrl_extract_dir'
        """
        try:
            # definir ruta a fichero zip de informes IPP xbrl a ser extraídos
            path_to_zip_file = self.xbrl_download_dir + '\Informes.zip'
            # esperar hasta que se haya finalizado la descarga
            fileIsDownloaded = utils.wait_until_file_is_download(path_to_zip_file, 
                                                                 self.xbrl_download_time_to_wait, 
                                                                 self.xbrl_download_count_until_filepart_cre, 
                                                                 self.xbrl_download_count_until_filepart_del);
            # si el fichero zip de informes xbrl ha sido descargado
            if fileIsDownloaded == True:
                # descomprimir fichero zip
                utils.upzip_file(path_to_zip_file, self.xbrl_extract_dir)
                # eliminar fichero zip ya procesado
                os.remove(path_to_zip_file)
                print("  * Unziped file")
                return True
            else:
                print('"  * Warning, file Not Found: '+path_to_zip_file);
                return False
        except Exception:
            traceback.print_exc()          
            raise Exception('Error WebScrapper.__decompress_ipp_xbrl_data.')           

    def __process_result(self, sectorId, sectorDictionary):
        """ Procesa el resultado obtenido tras la búsqueda y recuperación de datos
        Parameters
        ----------
        sectorId: str, mandatory
            Identificador de sector para el que se desean cargar los datos
        sectorDictionary: dictionary, mandatory
            Mapa con la clave de cada sector y nombre asociado al mismo
        """
        try:
            # --- Tratamos el resultado
            # Realizamos la descarga de ficheros XBRL corresondientes a los informes IPP
            downloadXbrlButtom = self.__get_elment_byid("wDescargas_Listado_btnDescargar", 5, modeError='noRaise')
            if(downloadXbrlButtom != False):
                downloadXbrlButtom.click() 
                # Realizar la extracción de los informes IPP
                if(self.__decompress_ipp_xbrl_data() == True):
                    # Recuperamos la tabla de datos y extraemos los datos existentes
                    result_data = self.__get_elment_byid("wDescargas_Listado_gridInformes", 5) 
                    data = self.__process_result_table_data(result_data, sectorId, sectorDictionary)
                    result = data
                else:
                    # si no se ha logrado descargar y descomprimir los ficheros xbrl se retorna
                    # False indicando que la extracción de los datos del sector y periodo no ha
                    # podido ser realizada satisfactoriametne
                    result = False
            else:
                result = False
            
            print('  * Result processed')
            return result
        except Exception:
            traceback.print_exc()            
            raise Exception('Error en WebScraper.__load_page.')

    def __process_result_table_data(self, result_data, sectorId, sectorDictionary):
        """ Procesa la tabla de resultados de una búsqueda
        Parameters
        ----------
        result_data: <table_element>, mandatory
            Elemento tabla con los resultados de la búsqueda   
        sectorId: str, mandatory
            Identificador de sector para el que se desean cargar los datos            
        sectorDictionary: dictionary, mandatory
            Mapeo sector, nombre de sector
        """
        try:
            #---- Procesar datos de la tabla de resultados
            
            # Se inicializa el contenedor de datos resultantes.
            # Este contenedor sera un array de 2 dimensiones, donde:
            # - cada fila se corresponde con una fila de la tabla
            # - cada columnna, con un campo de la fila de la tabla
            data = []

            # recupera las filas de la tabla
            rows = result_data.find_elements(By.TAG_NAME, "tr")
            # recorremos las distintas filas obteniendo los datos correspondietnes
            for row in rows:
                # Al recorrer las filas, si llegamos a una fila de paginación, 
                # significa que se ha finalizado de procesar la tabla de datos actual
                if(row.get_attribute("class") == 'paginador'):
                    break

                # Se inicializa los datos de la fila
                rowdata = []
                # Se añade el campo sector, incluyendo el nombre del sector cargado
                rowdata.append(sectorDictionary[sectorId])

                # Obtenemos las columnas de la fila de la tabla    
                cols = row.find_elements(By.TAG_NAME, "td")
                # Recorreoms las columnas
                colnum = 0
                xbrlPath = None
                for col in cols: 
                    # la columna con posición 4 se corresponde con el nombre del fichero xbrl, lo usamos
                    # para componer el path al mismo
                    colnum = colnum+1
                    if(colnum == 4):
                        xbrlPath = self.xbrl_extract_dir + '/' + col.text +'.xbrl'

                    # sabemos que no hay más de 6 campos de utilidad, ignoramos posibles columnas adicionales
                    if(colnum == 6):
                        continue
                    # añadimos el valor de la columna a los datos de la fila en procesamiento
                    rowdata.append(col.text)
                        
                # añadimos el valor del xbrlPath a los datos de la fila en procesamiento
                if(xbrlPath != None):
                    rowdata.append(xbrlPath)
                # Si en la fila de datos se han añadido más columnas además del sector
                # se añade la fila al contenedor de datos resultante
                if(len(rowdata) > 1):
                    data.append(rowdata)
            return data      
        except Exception:
            traceback.print_exc()            
            raise Exception('Error WebScrapper.__process_result_data.')          

    def __retrieve_data(self, sectorId, period):
        """ Realiza la búsqueda y recuperacón de los datos para el sector y el periodo específicados
        Parameters
        ----------
        sectorId: str, mandatory
            Identificador de sector para el que se desean cargar los datos
        period: int, mandatory
            Año que identifica el periodo para el que se desean cargar los datos
        """
        try:
            # --- Configurar la Búsqueda de informes
            # Click en opción Descarga de informes IPP
            downloadOption = self.__get_elment_byid("lkDescarga", 5)
            downloadOption.click()
            
            # Click en opción de búsqueda por Sector
            searchOption = self.__get_elment_byid("wDescargas_rbTipoBusqueda_1", 5)
            searchOption.click()
            
            # Seleccionar Sector suministrado como parámetro
            sectorSelector = Select(self.__get_elment_byid("wDescargas_drpSectores", 5))
            sectorSelector.select_by_value(sectorId)
            
            # Seleccionamos el periodo suministrado como parámetro
            sectorSelector = Select(self.__get_elment_byid("wDescargas_drpEjercicios", 5))
            sectorSelector.select_by_value(str(period))
  
            # --- Ejecutamos la búsqueda
            searchButtom = self.__get_elment_byid("wDescargas_btnBuscar", 5)
            searchButtom.click()
            
            print('  * Searched data')
        except Exception:
            traceback.print_exc()            
            raise Exception('Error en WebScraper.__load_page.')

    def __get_elment_byid(self, elementId, timeToWait, modeError = 'raise'):
        """ Recupera un elemento de la página por id 
        Parameters
        ----------
        elementId: str, mandatory
            Identifiador del elemento a recuperar
        timeToWait: int, mandatory
            Tiempo que ha de esperarse por la presencia del elemento en la página
        modeError: str, mandatory
            Determina si en caso de producirse una excepción ha de ser elevada o no
        """
        try:
            # Si procede, se espera el tiempo establecido por la presencia del elemento
            if(timeToWait):
                WebDriverWait(self.driver, timeToWait).until(EC.presence_of_element_located((By.ID, elementId)))
            #Obtenemos el elemento solicitado
            element = self.driver.find_element_by_id(elementId)
            return element
        except Exception:
            traceback.print_exc()
            if(modeError == 'raise'):
                raise Exception('Error WebScrapper.__get_elment_byid.')
            return False
        
    def __load_page(self, url):
        """ Carga la página, cuya url se suministra como parámetro
        Parameters
        ----------
        url: str, mandatory
            Url página a ser solicitada
        """
        try:
            self.driver.get(url)
            print('  * Pagina soliciada: http://www.cnmv.es/ipps')
        except Exception as e:
            print(e)            
            raise Exception('Error en WebScraper.__load_page.')
            
    def __init_webdriver(self):
        """ Inicializaliza el webdriver de Selenium que va a ser usado para realizar el scraping.
        """
        try:
            # Inicializar driver para Firefox
            # - Configuración parámetro profile
            profile = webdriver.FirefoxProfile()
            # - Indicar que no se ha de usar el directorio por defecto de Downloads
            profile.set_preference("browser.download.folderList",2)
            # - Deshabilitar showing download progress
            profile.set_preference("browser.download.manager.showWhenStarting", False)
            # - Establecer el directorio para los Downloads
            profile.set_preference("browser.download.dir", self.xbrl_download_dir)
            # - Especificar a Firefox que descarge automátiamente las ficheros de mime-types especificados
            profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/zip");
            # -Configuración parámetro binary
            binary = FirefoxBinary(self.selenium_firefox_path)

            # Instanciar driver par Firefox
            self.driver = webdriver.Firefox(firefox_profile=profile, firefox_binary=binary, executable_path=self.selenium_firefox_driver)
            print('  * Web driver inicializado')
        except Exception:
            traceback.print_exc()            
            raise Exception('Error en WebScraper.__init_webdriver.')      
