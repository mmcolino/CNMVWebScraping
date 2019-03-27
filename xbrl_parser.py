# -*- coding: utf-8 -*-********************
from bs4 import BeautifulSoup


class XbrlParser:
    """
    Clase que implementa la funcionalidad de parseado de ficheros XBRL
    """   
    def __init__(self, xbrlPath): 
        """ Constructor de la clase, recibe como parámetro la ruta del fichero xbrl a parsear.
        
        El constructor se encarga de realizar la lectura y carga del fichero xbrl, dejando el
        objeto listo para recibir solicitudes de consulta sobre los elementos presentes en el
        xbrl.
        
        Parameters
        ----------
        xbrlPath: str, mandatory
            Ruta fichero XBRL sobre el que se desea realizar el pareo.
        
        """
        try:
            # leer el fichero xbrl, usando encoding 'utf-8'
            self.xbrl_string = open(xbrlPath, encoding='utf-8').read()
            # Inializar el contenedor BeautifulSoup
            self.soup = BeautifulSoup(self.xbrl_string, "lxml-xml")
        except Exception as e:
            raise Exception('Error inicializando XbrlParser.')
            

    def get(self,tag_name, contextRef):
        """Recupera el/los elemento/s cuyo nombre de tag y contexto coincidan con los suministrados
           como parámetro.
        Parameters
        ----------
        tag_name: str, mandatory
            Nombre de tag del elemento/s que se desea recuperar
        contextRef: str, mandatory
            Nombre de contexto al que ha de pertenecer el/los elementos a recuperar
        """
        # recupera el conjunto completo de elementos
        tag_list = self.soup.find_all()
        for tag in tag_list:
            if(tag.name == tag_name and tag['contextRef'] == contextRef):
                print(tag.text)