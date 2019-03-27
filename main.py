# -*- coding: utf-8 -*-
print("Web Scraping: Spain CNMV-IPP (Información Pública Periódica)")

from web_scraper import WebScraper
from xbrl_parser import XbrlParser
from utils import Utils

import sys
import os

   
# Inicializar la clase que implementa las operaciones de web scraper
wsPreferences = {'selenium_firefox_path' : 'C:/Program Files/Mozilla Firefox/Firefox.exe',
                 'selenium_firefox_driver' : 'C:/Users/Marimar/Anaconda3/Lib/site-packages/selenium/webdriver/geckodriver-v0.24.0-win64/geckodriver.exe',
                 'xbrl_ipp_url': 'http://www.cnmv.es/ipps',
                 'xbrl_download_dir' : 'F:\CNMV-IPPWebScraping\data\download',
                 'xbrl_extract_dir' : 'F:/CNMV-IPPWebScraping/data/ipp-xbrl',
                 'xbrl_download_time_to_wait' : 5,
                 'xbrl_download_count_until_filepart_cre' : 15,
                 'xbrl_download_count_until_filepart_del' : 10 }
webScraper = WebScraper(wsPreferences)
# Inicializar clase de utilidades
utils = Utils()

# Configuración de los datos a ser descargados
sectorDictionary = {'S1_2': 'ENERGÍA Y AGUA'}
#sectorDictionary = {'S1_1':'PETROLEO', 'S1_2': 'ENERGÍA Y AGUA', 'S1_3': 'MINERIA', 'S1_4': 'QUÍMICAS', 'S1_5': 'TEXTIL Y PAPELERAS', 'S1_6' : 'COMERCIO'}
periods = [2018]

csv_data_dir = 'F:\CNMV-IPPWebScraping\data\csv'

# Carga de datos por sector y periodo
for key, value in sectorDictionary.items():
    for period in periods:
        print('> Loading sector: '+sectorDictionary[key]+' period: '+str(period))
        result = webScraper.load_sector_data(sectorDictionary=sectorDictionary, sectorId=key, period=period)
        if result == False:
            print('---- Not found data, sector: '+sectorDictionary[key]+' period: '+str(period)) 
        else:
            print('---- Loaded sector: '+sectorDictionary[key]+' period: '+str(period))
            csvfileName = str(period)+'_'+sectorDictionary[key]+'.csv'
            csvFilePath = csv_data_dir+'/'+csvfileName
            utils.write2DArrayToCsv(twoDimensionArray=result, file_csv_path=csvFilePath, delimiter=';')
                       

xbrlParser = XbrlParser('F:/CNMV-IPPWebScraping/data/ipp-xbrl/2018088106.xbrl')
# Plantilla Media
# - Individual, periodo actual - total
plantillaMediaTotal = xbrlParser.get('I2295', 'Icur_IndividualMiembro_PeriodoActualMiembro')
# - Individual, periodo actual - hombres
plantillaMediaHombres = xbrlParser.get('I2296', 'Icur_IndividualMiembro_PeriodoActualMiembro')
# - Individual, periodo actual - mujeres
plantillaMediaMujeres = xbrlParser.get('I2297', 'Icur_IndividualMiembro_PeriodoActualMiembro')
