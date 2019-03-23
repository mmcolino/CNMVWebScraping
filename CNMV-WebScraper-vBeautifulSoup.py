# -*- coding: utf-8 -*-
"""
Librerías a instalar
pip install beautifulsoup4
pip install html5lib
"""

# Se realiza el import de las librerías requeridas
from requests import get
from bs4 import BeautifulSoup
from pprint import pprint

# Se define la url de la página de acceso a la descarga de informes xbrl, y se accede a ella
cnmv_xbrl_url = "http://www.cnmv.es/ipps"
response = get(cnmv_xbrl_url)
print(response.text[:1500])

# Se parsea el resultado obtenido
soup = BeautifulSoup(response.text, 'html5lib')

#CONFIGURAMOS LA BÚSQUEDA
#Verificamos si el elemento con ID="lkDescarga" ya está cargado, este elemento es el botón 
#que nos da acceso a la configuración de las descargas
btn = soup.find(attrs={'id':'lkDescarga'})

        