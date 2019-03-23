# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""

print("Hello Anaconda")

""" Importar librerías requeridas """
""" Ejemplo - http://pythonpiura.org/posts/2016/01/25/web-scraping-con-selenium/ """ 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.options import Options
import sys
import os

print("Librerías importadas")

""" Definir función para carga de un sector empresarial """
def load_sector(cadena):
    options = Options()
    options.set_preference("browser.download.folderList",2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir","/data")
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/zip");
    driver = webdriver.Firefox(options=options, executable_path='C:/Users/Marimar/Anaconda3/Lib/site-packages/selenium/webdriver/geckodriver-v0.24.0-win64/geckodriver.exe')

    #driver = webdriver.Firefox(executable_path='C:/Users/Marimar/Anaconda3/Lib/site-packages/selenium/webdriver/geckodriver-v0.24.0-win64/geckodriver.exe')
    #Página a la que queremos acceder
    driver.get("http://www.cnmv.es/ipps")
    # valores configurados en elemento select con id = wDescargas_drpSectores //fixme: ver como obtener valores automáticamente
    diccionarioSectores = {'S1_1':'PETROLEO', 'S1_2': 'ENERGÍA Y AGUA', 'S1_3': 'MINERIA', 'S1_4': 'QUÍMICAS', 'S1_5': 'TEXTIL Y PAPELERAS', 'S1_6' : 'COMERCIO'}
    
    lista_datos = []
    try:
        #CONFIGURAMOS LA BÚSQUEDA
        #Verificamos si el elemento con ID="lkDescarga" ya está cargado, este elemento es el botón 
        #que nos da acceso a la configuración de las descargas
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "lkDescarga")))
        #Obtenemos el botón para configurar las descargas
        botonDescarga = driver.find_element_by_id("lkDescarga")
        #Damos click al botón
        botonDescarga.click()
         
        #Obtenemos el Radio button para seleccionar Sectores, con ID="wDescargas_rbTipoBusqueda_1"
        opcionSectores = driver.find_element_by_id("wDescargas_rbTipoBusqueda_1")
        #Damos click al readio button
        opcionSectores.click()
        
        #Obtenemos el Select de sectores con ID = "wDescargas_drpSectores"
        selectSectores = Select(driver.find_element_by_id("wDescargas_drpSectores"))
        
        #Seleccionamos la primera opción
        #selectSectores.select_by_visible_text('PETROLEO')
        selectSectores.select_by_value('S1_1')#//fixme: sustituir valor por el pasado como parámetro
        
        #EJECUTAMOS LA BÚSQUEDA
        #Obtenemos el botón para realizar la búsqueda
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "wDescargas_btnBuscar")))
        #Obtenemos el botón para realizar la búsqueda según el sector
        botonBuscar = driver.find_element_by_id("wDescargas_btnBuscar")
        #Damos click al botón
        botonBuscar.click()
        
        #TRATAMOS EL RESULTADO
        #-Se tratan los datos de la lista de informes semestrales
        #Ahora buscamos el resultado en la tabla con ID="wDescargas_Listado_gridInformes"
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "wDescargas_Listado_gridInformes")))
        
        tablaResultados = driver.find_element_by_id("wDescargas_Listado_gridInformes")
        rows = tablaResultados.find_elements(By.TAG_NAME, "tr") # get all of the rows in the table

        for row in rows:
            #//fixme: al recorrer las filas, obviar la fila usada para id="paginador"
            
            #Obtenemos las columnas de cada fila      
            cols = row.find_elements(By.TAG_NAME, "td")
            #Recorreoms las columnas
            for col in cols:
                #Imprimimos el contenido de la columna //fixme: tratar estos datos
                print(col.text) 

        #-Se descargan los ficheros xbrl correspondientes a los datos en la lista
        #http://allselenium.info/file-downloads-python-selenium-webdriver/
        
        #Verificamos si el elemento con ID="lkDescarga" ya está cargado, este elemento es el botón 
        #que nos da acceso a la configuración de las descargas
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "wDescargas_Listado_btnDescargar")))
        #Obtenemos el botón para configurar las descargas
        botonDescargaFicheros = driver.find_element_by_id("wDescargas_Listado_btnDescargar")
        #Damos click al botón
        botonDescargaFicheros.click()
        
        print(cadena)
        
    except:
        #Mostramos este mensaje en caso de que se presente algún problema
        print("Unexpected error:", sys.exc_info()[0])
    
    #/fixme: wait until end download
    #driver.close()
    return cadena

print("load_sector definida")

""" Cargar sector de ejemplo """
load_sector("Ejemplo")