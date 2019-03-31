# -*- coding: utf-8 -*-
from scraper_orchestrator import ScraperOrchestrator
import traceback

# Configurar el scraping de datos
# - Conjunto de sectores para los que nos interesa realizar la descarga de datos
#   (Se ha decidido establecer este dato por configuraicón, en lugar de hacer scraping del mismo con el objetivo de 
#    disponer de la flexibilidad necesaria para poder configurar los sectores para los que interesa cargar datos)
sectorDictionary = {'S1_2': 'ENERGÍA Y AGUA'}
"""sectorDictionary = {'S1_1':'PETROLEO', 
                    'S1_2': 'ENERGÍA Y AGUA', 
                    'S1_3': 'MINERIA', 
                    'S1_4': 'QUÍMICAS', 
                    'S1_5': 'TEXTIL Y PAPELERAS', 
                    'S1_6': 'COMERCIO',
                    'S1_7': 'METAL MECÁNICA',
                    'S1_8': 'ALIMENTACIÓN',
                    'S1_9': 'CONSTRUCCIÓN',
                    'S1_10': 'INMOBILIARIAS',
                    'S1_11': 'TRANSPORTES Y COMUNICACIONES',
                    'S1_12': 'OTRAS INDUSTRIAS MANUFACTURERAS',
                    'S1_13': 'OTROS',
                    'S2_1': 'BANCOS',
                    'S2_2': 'CAJAS Y COOPERATIVAS DE CREDITO',
                    'S2_3': 'SEGUROS Y OTRAS INTERMEDIACIONES FINANCIERAS',
                    'S3_1': 'ESTADO',
                    'S3_2': 'OTROS ORGANISMOS PUBLICOS'
                    }"""
# - Periodos financieros a contemplar (años)
periods = [2018]

# Configuración de la extracción de datos
# - Propiedades xbrl a ser extraidas
xbrlPropertiesList = ['I2295', # Plantilla Media - Total
                      'I2296', # Plantilla Media - Hombres
                      'I2297'] # Plantilla Media - Mujeres
# - Contexto aplicable
xbrlContext = 'Icur_IndividualMiembro_PeriodoActualMiembro'

try:
    # Inicializar el orquestador de scraping de datos
    wsPreferences = {'selenium_firefox_path' : 'C:/Program Files/Mozilla Firefox/Firefox.exe',
                     'selenium_firefox_driver' : 'C:/Users/Marimar/Anaconda3/Lib/site-packages/selenium/webdriver/geckodriver-v0.24.0-win64/geckodriver.exe',
                     'xbrl_ipp_url': 'http://www.cnmv.es/ipps',
                     'xbrl_download_dir' : 'F:\CNMV-IPPWebScraping\data\download',
                     'xbrl_extract_dir' : 'F:\CNMV-IPPWebScraping\data\ipp-xbrl',
                     'xbrl_download_time_to_wait' : 5,
                     'xbrl_download_count_until_filepart_cre' : 15,
                     'xbrl_download_count_until_filepart_del' : 15 }
    # - Directorio contenedor de los datos que van a ser extraidos y formateados en formato csv
    csv_data_dir = 'F:\CNMV-IPPWebScraping\data\csv'
    
    scraperOrchestator = ScraperOrchestrator(wsPreferences, csv_data_dir)
    
    # Ejecutar scraping y extracción de datos
    scraperOrchestator.run(sectorDictionary,
                           periods, 
                           xbrlPropertiesList, 
                           xbrlContext)

    # Extracción de datos (aplicable cuandos se desean realizar extracciones posteriores de datos
    #  a partir de un conjunto de informes ipp xbbrl previamente descargados)
    # scraperOrchestator.extracting(xbrlPropertiesList, xbrlContext)   
except Exception:
    traceback.print_exc()          



