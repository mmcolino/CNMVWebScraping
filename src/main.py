# -*- coding: utf-8 -*-
from scraper_orchestrator import ScraperOrchestrator
import traceback
import argparse

# Configurar el scraping de datos
# - Conjunto de sectores para los que nos interesa realizar la descarga de datos
#   (Se ha decidido establecer este dato por configuraicón, en lugar de hacer scraping del mismo con el objetivo de 
#    disponer de la flexibilidad necesaria para poder configurar los sectores para los que interesa cargar datos)
#sectorDictionary = {'S1_13': 'OTROS'}
sectorDictionary = {'S1_1':'PETROLEO', 
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
                    }
# - Periodos financieros a contemplar (años)
periods = [2018]

# Configuración de la extracción de datos
# - Propiedades xbrl a ser extraidas

xbrlPropertiesMap = {# Balance consolidado
                      'I1040': 'Icur_PeriodoActualBalanceMiembro', # A) ACTIVO NO CORRIENTE
                      'I1085': 'Icur_PeriodoActualBalanceMiembro', # B) ACTIVO CORRIENTE
                      'I1100': 'Icur_PeriodoActualBalanceMiembro', # TOTAL ACTIVO (A + B)
                      'I1195': 'Icur_PeriodoActualBalanceMiembro', # A) PATRIMONIO NETO (A.1 + A.2 + A.3 )
                      'I1120': 'Icur_PeriodoActualBalanceMiembro', # B) PASIVO NO CORRIENTE
                      'I1130': 'Icur_PeriodoActualBalanceMiembro', # C) PASIVO CORRIENTE
                      'I1200': 'Icur_PeriodoActualBalanceMiembro', # TOTAL PASIVO Y PATRIMONIO NETO (A + B + C )
                      # Cuenta de Pérdidas y Ganancias Consolidada
                      'I1245': 'Dcur_AcumuladoActualMiembro_ImporteMiembro', # RESULTADO DE EXPLOTACIÓN
                      'I1256': 'Dcur_AcumuladoActualMiembro_ImporteMiembro', # RESULTADO FINANCIERO
                      'I1265': 'Dcur_AcumuladoActualMiembro_ImporteMiembro', # RESULTADO ANTES DE IMPUESTOS
                      'I1280': 'Dcur_AcumuladoActualMiembro_ImporteMiembro', # RESULTADO DEL EJERCICIO PROCEDENTE DE OPERACIONES CONTINUADAS
                      'I1285': 'Dcur_AcumuladoActualMiembro_ImporteMiembro', # Resultado del ejercicio procedente de operaciones interrumpidas neto de impuestos
                      'I1288': 'Dcur_AcumuladoActualMiembro_ImporteMiembro', # RESULTADO CONSOLIDADO DEL EJERCICIO
                      'I1290': 'Dcur_AcumuladoActualMiembro_ImporteMiembro', # BENEFICIO POR ACCIÓN básico
                      'I1295': 'Dcur_AcumuladoActualMiembro_ImporteMiembro', # BENEFICIO POR ACCIÓN diluido
                      # Estado de Ingresos y Gastos Reconocidos Consolidado
                      'I1305': 'Dcur_PeriodoActualMiembro', # RESULTADO CONSOLIDADO DEL EJERCICIO (de la cuenta de pérdidas y ganancias)
                      'I1310': 'Dcur_PeriodoActualMiembro', # OTRO RESULTADO GLOBAL – PARTIDAS QUE NO SE RECLASIFICAN AL RESULTADO DEL PERIODO
                      'I1350': 'Dcur_PeriodoActualMiembro', # OTRO RESULTADO GLOBAL – PARTIDAS QUE PUEDEN RECLASIFICARSE POSTERIORMENTE AL RESULTADO DEL PERIODO
                      'I1400': 'Dcur_PeriodoActualMiembro', # RESULTADO GLOBAL TOTAL DEL EJERCICIO (A + B + C)
                      # Plantilla
                      'I2295': 'Icur_IndividualMiembro_PeriodoActualMiembro', # Plantilla Media - Total
                      'I2296': 'Icur_IndividualMiembro_PeriodoActualMiembro', # Plantilla Media - Hombres
                      'I2297': 'Icur_IndividualMiembro_PeriodoActualMiembro'  # Plantilla Media - Mujeres
                      }

try:
    # Obtener argumentos command line
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", help="Enter execution mode: total / xbrlExtract")
    args = parser.parse_args()
    mode = args.mode
    
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

    # Evaluar el modo de ejecución        
    if mode == None or mode == "total":
        # Ejecutar scraping y extracción de datos
        scraperOrchestator.run(sectorDictionary,
                               periods, 
                               xbrlPropertiesMap)

    if mode != None and mode == "xbrlExtract":
        # Extracción de datos (aplicable cuandos se desean realizar extracciones posteriores de datos
        #  a partir de un conjunto de informes ipp xbbrl previamente descargados)
        scraperOrchestator.extracting(xbrlPropertiesMap)   
except Exception:
    traceback.print_exc()          



