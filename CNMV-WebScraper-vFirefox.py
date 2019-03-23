# -*- coding: utf-8 -*-
print("Web Scraping: Spain CNMV-IPP (Información Pública Periódica)")

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

import sys
import os

import csv

# Inicializar elementos requeridos
utils = Utils()

# Configuración
selenium_firefox_path = 'C:\Program Files\Mozilla Firefox\Firefox.exe'
selenium_firefox_driver = 'C:/Users/Marimar/Anaconda3/Lib/site-packages/selenium/webdriver/geckodriver-v0.24.0-win64/geckodriver.exe'

# - Configuración de la descarga de ficheros IPP xbrl
#   * Configuración ubicación donde se ha de realizar la descarga de los ficheros zip que contienen los ficheros
#     XBRL para una página de resultados.
xbrl_download_dir = 'F:\CNMV-IPPWebScraping\data\download'
#   * Configuración directorio donde se descombrimirán y ubicarán los ficheros xbrl resultantes de la descompresión
#     del zip previo.
xbrl_extract_dir = 'F:\CNMV-IPPWebScraping\data\ipp-xbrl'
#   * Se requerirá configurar una serie de parámetros para parametrizar el comportamiento de la función de espera
#     hasta que una determinada descarga de fichero ha sido realizada.
#     Como máximo se esperará: xbrl_download_time_to_wait * xbrl_download_count_until_filepart_cre * xbrl_download_count_until_filepart_del
#     > tiempo a esperar entre verificaciones de la existencia de el fichero <download_file>.part
xbrl_download_time_to_wait = 5
#     > número de veces a esperar por la aparicicón del fichero <download_file>.part
xbrl_download_count_until_filepart_cre = 15 
#    > número de veces a esperar por la desaparición del fichero <download_file>.part
xbrl_download_count_until_filepart_del = 10 

csv_data_dir = 'F:\CNMV-IPPWebScraping\data\csv'

# Configuración de los datos a ser descargados
sectorDictionary = {'S1_1':'PETROLEO', 'S1_2': 'ENERGÍA Y AGUA'}
#sectorDictionary = {'S1_1':'PETROLEO', 'S1_2': 'ENERGÍA Y AGUA', 'S1_3': 'MINERIA', 'S1_4': 'QUÍMICAS', 'S1_5': 'TEXTIL Y PAPELERAS', 'S1_6' : 'COMERCIO'}
periods = [2018]


""" Definir función para carga de un sector empresarial """
def load_sector(sectorDictionary, sectorId, period):
    data = []
    # //fixme: establecer useragent, ... time between request, etc
    
    # 1. Inicializar driver para Firefox
    # 1.1. Configuración parámetro profile
    #    https://stackoverflow.com/questions/25251583/downloading-file-to-specified-location-with-selenium-and-python
    #    https://stackoverflow.com/questions/41644381/python-set-firefox-preferences-for-selenium-download-location
    profile = webdriver.FirefoxProfile()
    # 1.1.1. tells it not to use default Downloads directory
    profile.set_preference("browser.download.folderList",2)
    # 1.1.2. turns of showing download progress
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    # 1.1.3. sets the directory for downloads
    profile.set_preference("browser.download.dir", xbrl_download_dir)
    # 1.1.4. tells Firefox to automatically download the files of the selected mime-types
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/zip");
    
    # 1.2. Configuración parámetro binary
    binary = FirefoxBinary(selenium_firefox_path)
    
    # 1.3. instanciar driver par Firefox
    driver = webdriver.Firefox(firefox_profile=profile, firefox_binary=binary, executable_path=selenium_firefox_driver)

    #Página a la que queremos acceder
    driver.get("http://www.cnmv.es/ipps")
   
    try:
        print("Step 1")
        #CONFIGURAMOS LA BÚSQUEDA
        #Verificamos si el elemento con ID="lkDescarga" ya está cargado, este elemento es el botón 
        #que nos da acceso a la configuración de las descargas
        # https://selenium-python.readthedocs.io/waits.html
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "lkDescarga")))
        #Obtenemos el botón para configurar las descargas
        botonDescarga = driver.find_element_by_id("lkDescarga")
        #Damos click al botón
        botonDescarga.click()
         
        print("Step 2")
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "wDescargas_rbTipoBusqueda_1")))
        #Obtenemos el Radio button para seleccionar Sectores, con ID="wDescargas_rbTipoBusqueda_1"
        opcionSectores = driver.find_element_by_id("wDescargas_rbTipoBusqueda_1")
        #Damos click al readio button
        opcionSectores.click()
        
        print("Step 3")
        #Obtenemos el Select de sectores con ID = "wDescargas_drpSectores"
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "wDescargas_drpSectores"))) 
        selectSectores = Select(driver.find_element_by_id("wDescargas_drpSectores"))
        #Seleccionamos el sector pasado como parámetro
        selectSectores.select_by_value(sectorId)
        
        print("Step 4")
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "wDescargas_drpEjercicios")))        
        #Obtenemos el Select de sectores con ID = "wDescargas_drpSectores"
        selectSectores = Select(driver.find_element_by_id("wDescargas_drpEjercicios"))
        #Seleccionamos el año
        selectSectores.select_by_value(str(period))#//fixme: sustituir valor por el pasado como parámetro        
        
        print("Step 5")         
        #EJECUTAMOS LA BÚSQUEDA
        #Obtenemos el botón para realizar la búsqueda
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "wDescargas_btnBuscar")))
        #Obtenemos el botón para realizar la búsqueda según el sector
        botonBuscar = driver.find_element_by_id("wDescargas_btnBuscar")
        #Damos click al botón
        botonBuscar.click()
        
        print("Step 6")
        #TRATAMOS EL RESULTADO
        try:
            #-Se tratan los datos de la lista de informes semestrales
            #Ahora buscamos el resultado en la tabla con ID="wDescargas_Listado_gridInformes"
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "wDescargas_Listado_gridInformes")))
            
            tablaResultados = driver.find_element_by_id("wDescargas_Listado_gridInformes")
            rows = tablaResultados.find_elements(By.TAG_NAME, "tr") # get all of the rows in the table
    
            for row in rows:
                rowdata = []
                #//fixme: al recorrer las filas, obviar la fila usada para id="paginador"
                
                #Obtenemos las columnas de cada fila      
                cols = row.find_elements(By.TAG_NAME, "td")
                #Recorreoms las columnas
                for col in cols:
                    rowdata.append(col.text)
                    #Imprimimos el contenido de la columna //fixme: tratar estos datos
                    print(col.text) 
                data.append(rowdata)
                
            #-Se descargan los ficheros xbrl correspondientes a los datos en la lista
            #http://allselenium.info/file-downloads-python-selenium-webdriver/
            
            print("Step 6")
            #Verificamos si el elemento con ID="lkDescarga" ya está cargado, este elemento es el botón 
            #que nos da acceso a la configuración de las descargas
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "wDescargas_Listado_btnDescargar")))
            #Obtenemos el botón para configurar las descargas
            botonDescargaFicheros = driver.find_element_by_id("wDescargas_Listado_btnDescargar")
            #Damos click al botón
            botonDescargaFicheros.click()
            
            print("Step 7")
            # Realizar la extracción de los informes IPP
            extract_ipp_xbrl_data()
            return data
        except Exception as e:
            print(str(e))
            driver.close()
            return False
    except:
        #Mostramos este mensaje en caso de que se presente algún problema
        print("Unexpected error:", sys.exc_info()[0])
        driver.close()
        return False
    
    #Wait until end download


# Realiza la extracción de los informes IPP xbrl descargados
def extract_ipp_xbrl_data():
    print("extract_ipp_xbrl_data - Step 1")
    # definir ruta a fichero zip de informes IPP xbrl a ser extraídos
    path_to_zip_file = xbrl_download_dir + '\Informes.zip'
    # esperar hasta que se haya finalizado la descarga
    fileIsDownloaded = utils.wait_until_file_is_download(path_to_zip_file, xbrl_download_time_to_wait, xbrl_download_count_until_filepart_cre, xbrl_download_count_until_filepart_del);
    print("extract_ipp_xbrl_data - Step 2")
    # si el fichero zip de informes xbrl ha sido descargado
    if fileIsDownloaded == True:
        # descomprimir fichero zip
        utils.upzip_file(path_to_zip_file, xbrl_extract_dir)
        # eliminar fichero zip ya procesado
        os.remove(path_to_zip_file)
    else:
        print('Warning, file Not Found: '+path_to_zip_file);

        
print("load_sector definida")


# Carga de datos por sector y periodo
for key, value in sectorDictionary.items():
    for period in periods:
        print('> Loading sector: '+sectorDictionary[key]+' period: '+str(period))
        result = load_sector(sectorDictionary=sectorDictionary, sectorId=key, period=period)
        if result == False:
            print('---- Not found data, sector: '+sectorDictionary[key]+' period: '+str(period)) 
        else:
            print('---- Loaded sector: '+sectorDictionary[key]+' period: '+str(period))
            csvfileName = str(period)+'_'+sectorDictionary[key]+'.csv'
            csvFilePath = csv_data_dir+'/'+fileName
            utils.write2DArrayToCsv(twoDimensionArray=result, file_csv_path=csvFilePath, delimiter=',')
                       



