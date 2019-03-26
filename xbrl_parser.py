# -*- coding: utf-8 -*-********************
from bs4 import BeautifulSoup

"""
    Clase que implementa funciones de utilidad
    - Descomprensión de ficheros
    - Espera hasta que finaliza la descarga de ficheros
"""
class XbrlParser:
    """ Constructor de la clase, recibe como parámetro la ruta del fichero xbrl a parsear """
    def __init__(self, xbrlPath):  
        self.xbrl_string = open(xbrlPath, encoding='utf-8').read()
        self.soup = BeautifulSoup(self.xbrl_string, "lxml-xml")
        #print(soup.prettify())
        
    def get(self,tag_name, contextRef):
        tag_list = self.soup.find_all()
        for tag in tag_list:
            if(tag.name == tag_name and tag['contextRef'] == contextRef):
                print(tag.text)