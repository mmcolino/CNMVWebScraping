# -*- coding: utf-8 -*-
from web_scraper import WebScraper
from xbrl_parser import XbrlParser
from utils import Utils
import traceback

class ScraperOrchestrator():
    """
    Clase que implementa la orquestación de las tareas de:
        - Web Scraping
        - Extracción de los datos y generación de datasets
    """ 
    def __init__(self, wsPreferences, csv_data_dir):
        """ Constructor de la clase, recibe como parámetro las preferencias configurables 
        Parameters
        ----------
        wsPreferences: dictionary, mandatory
            Objeto de tipo dictionary que define las preferencias a ser confiuradas de acuerdo 
            a las características del scraping que va a ser realizado, y del entorno de ejecución.
            (Más detalles en la documentación de la clase WebScraper)
        csv_data_dir: str, mandatory
            Directorio donde se volcarán los datasets resultantes, en formato csv
        """        
        try:
            # Establecer ubicación salida de datos csv
            self.csv_data_dir = csv_data_dir
            # Inicializar el Web Scraper
            self.webScraper = WebScraper(wsPreferences)
            # Inicializar clase de utilidades
            self.utils = Utils() 
        except Exception:
            traceback.print_exc()          
            raise Exception('Error ScraperOrchestrator.__init__.') 
        
    def run(self, sectorDictionary, periods, xbrlPropertiesList, xbrlContext):
        """ Metodo que lleva a cabo la ejecución del proceso de scraping y posterior extracción y 
        construcción de los data sets.
        Para ello llevará a cabo los siguientes pasos:
            1. Para cada sector y periodo especificados: 
               1.1. Realizará el Web scraping de los datos relativos a sectores empresariales y periodos especificados
                    como parámetro.
                    - Se recuperará un array de 2 dimensiones con los datos de indexación asociados a los informes IPP 
                      correspondientes a las empresas del sector que han presentado dicha información en el periodo especificados.
                      Para cada informe presentado se recuperarán los campos: 'Sector', 'Entidad', 'Ejercicio', 'Periodo', 
                     'NombreXBRL', 'Tamaño(KB)', 'Path'
                    - Se descargarán los ficheros xbrl asociados a los informes IPP
                1.2. Se volcala la información de indexación de informes IPP a un dataset en formato CSV.
            2. Para cada informe IPP presente en el fichero de indexación del dataset generado en el paso 1.2 se realizará
               el parseo XBRL extrayendo las propiedades configuradas, y se generará un dataset con un registro para cada informe
               IPP procesado con la siguiente información:
                   'Sector', 'Entidad', 'Ejercicio', 'Periodo', 'NombreXBRL', '<prop1>', ..., '<propn>'
        Parameters
        ----------
        wsPreferences: dictionary, mandatory
            Objeto de tipo dictionary que define las preferencias a ser confiuradas de acuerdo 
            a las características del scraping que va a ser realizado, y del entorno de ejecución.
            (Más detalles en la documentación de la clase WebScraper)
        periods: [int, ..], mandatory
            Lista de años que identifican los periodos financieros aplicables
        xbrlPropertiesList: list, mandatory
            Lista de propiedades a ser extraidas de los ficheros xbrl
        xbrlContext: str, mandatory
            Identificador del contexto aplicable a las propiedades a ser extraidas
        """         
        try:
            # Carga de datos por sector y periodo
            self.__scraping(sectorDictionary, periods)
            # Extracción xbrl properties
            self.extracting(xbrlPropertiesList, xbrlContext)
        except Exception:
            traceback.print_exc()          
            raise Exception('Error ScraperOrchestrator.__init__.') 

    def __scraping(self, sectorDictionary, periods):
        """ Ejecuta el scraping por sector y periodo
        wsPreferences: dictionary, mandatory
            Objeto de tipo dictionary que define las preferencias a ser confiuradas de acuerdo 
            a las características del scraping que va a ser realizado, y del entorno de ejecución.
            (Más detalles en la documentación de la clase WebScraper)
        periods: [int, ..], mandatory
            Lista de años que identifican los periodos financieros aplicables        
        """
        try:
            # Inicializa juego de datos de indexación de informes IPP de 
            # - Borra el fichero en caso de que existiera 
            pathIndexReports = self.__get_indexIppReportsPath();
            self.utils.deleteIfExist(pathIndexReports)
            # - Añade una línea de cabecera
            self.utils.write2DArrayToCsv(twoDimensionArray=[self.__get_indexIppReportsHeader()], 
                                         file_csv_path=pathIndexReports, delimiter=';') 
            # Carga de datos por sector y periodo
            for key, value in sectorDictionary.items():
                for period in periods:
                    print('> Loading sector: '+sectorDictionary[key]+' period: '+str(period))
                    data2Darray = self.webScraper.load_sector_data(sectorDictionary=sectorDictionary, sectorId=key, period=period)
                    if data2Darray == False:
                        print('---- Not found data, sector: '+sectorDictionary[key]+' period: '+str(period)) 
                    else:
                        print('---- Loaded sector: '+sectorDictionary[key]+' period: '+str(period))
                        self.utils.write2DArrayToCsv(twoDimensionArray=data2Darray, file_csv_path=pathIndexReports, delimiter=';')             
        except Exception:
            traceback.print_exc()          
            raise Exception('Error ScraperOrchestrator.__scraping.')             
       
        
    def extracting(self, xbrlPropertiesList, xbrlContext):
        """ Ejecuta la extracción y posterior creación del dataset con las propiedades requeridas de los 
            ficheros xbrl.
        Parameters
        ----------
        xbrlPropertiesList: list, mandatory
            Lista de propiedades a ser extraidas de los ficheros xbrl
        xbrlContext: str, mandatory
            Identificador del contexto aplicable a las propiedades a ser extraidas
        """ 
        try:
            pathIndexReports = self.__get_indexIppReportsPath();
            indexReportArray = self.utils.loadCsvTo2DArray(pathIndexReports, delimiter=";");
            ouputArray = []
            line_count = 0
            for row in indexReportArray:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    pathXbrlFile = row[6]
                    print(f'\tExtracting xbrl file: {row[6]}.')
                    outputrow = row
                    xbrlParser = XbrlParser(pathXbrlFile)
                    for prop in xbrlPropertiesList:
                        valuePropertie = xbrlParser.get(prop, xbrlContext)
                        outputrow.append(valuePropertie)
                    ouputArray.append(outputrow)   
                    line_count += 1

            # - Añade una línea de cabecera
            pathProperiesIPPXbrl = self.__get_propertiesIPPXbrlPath()
            self.utils.deleteIfExist(pathProperiesIPPXbrl)
            header = self.__get_indexIppReportsHeader() + xbrlPropertiesList
            self.utils.write2DArrayToCsv(twoDimensionArray=[header], 
                                        file_csv_path=pathProperiesIPPXbrl, delimiter=';')                     
            self.utils.write2DArrayToCsv(twoDimensionArray=ouputArray, file_csv_path=pathProperiesIPPXbrl, delimiter=';') 
            print(f'Processed {line_count} lines.')            
        except Exception:
            traceback.print_exc()          
            raise Exception('Error ScraperOrchestrator.__scraping.')             

    def __get_indexIppReportsHeader(self):
        """ Retorna la lista de campos que forman parte del fichero de indexación de ficheros IPP xbrl"""
        return ['Sector', 'Entidad', 'Ejercicio', 'Periodo', 'NombreXBRL', 'Tamaño(KB)', 'Path']
            
    def __get_indexIppReportsPath(self):
        """ Retorna el path del fichero de indexación de informes IPPs xbrl descargados"""
        csvfileName = 'indexIPPXbrlReports.csv'
        pathIndexReports = self.csv_data_dir+'/'+csvfileName   
        return pathIndexReports
    
    def __get_propertiesIPPXbrlPath(self):
        """ Retorna el path del fichero de salida con el dataset de propiedades xbrl extraidos"""
        csvfileName = 'propertiesIPPXbrl.csv'
        pathIndexReports = self.csv_data_dir+'/'+csvfileName   
        return pathIndexReports    