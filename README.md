# CNMVWebScraping

## Descripción

El contenido de este respositorio se corresponde con el resultado de la elaboración de la Práctica 1 de la asignatura Tipología y ciclo de vida de los datos, enmarcada dentro del máster en Data Science de la Universitat Oberta de Catalunya.

En la ejecución de esta práctica se han aplicado técnicas de web scraping haciendo uso del lenguaje de programación Python, con el objetivo de extraer información relativa a estados financieros estandarizados de caracter público.

El ámbito de la información objeto del alcance de esta práctica, son los estados financieros disponibles en la web de la Comision Nacional del Mercado de Valores [CNMV](http://www.cnmv.es/ipps/), centrándonos en el uso de la versión de datos suministrada en formato estandarizado [XBRL](https://xbrl.es/wp/).

## Miembros del equipo

Esta práctica ha sido elaborada de forma individual por **María del Mar Colino García**.

## Ficheros

El presente repositorio define la siguiente estructura de directorios y ficheros:

- **src**: Contenedor código fuente de la aplicación
    * *main.py*: Punto de entrada a la aplicación, en este fichero se realiza la configuración del proceso de scraping y se inicial el proceso.
    * *scraper_orchestrator.py*: Clase que implementa la orquestación de las tareas de Web Scraping, extracción de los datos y generación de datasets.
    * *web_scraper.py*: Clase que implementa la funcionalidad de scraping para los informes IPP publicados en la CNMV
    * *xbrl_parser.py*: Clase que implementa la funcionalidad de parseado de ficheros XBRL
    * *utils.py*: Clase que implementa funciones de utilidad

- **data**: Contenedor datos extraidos. Define la siguiente estructura de directorios:
    * *download*: Ubicación donde serán descargados los ficheros zip con paquetes de informes xbrl.
    * *ipp-xbrl*: Ubicación donde se persistirán los ficheros xbrl.
    * *csv*: Ubicación donde se persistirán los datasets generados:
        - *indexIPPXbrlReports.csv*: Dataset con los datos generales y de indexación de los ficheros xbrl descargados.
                                     De cara a hacer uso de estos datos, se ha de considerar que la el base path del repositorio donde se encuentran los ficheros xbrl será denotado como <repositoryPath> en este fichero, por lo tanto a la hora de hacer uso de esta información, deberá reemplazarse dicho valor por el path base que haya sido configurado en la extracción.
                                     De esta forma se facilita la flexibilidad en la persistencia y posterior uso del repositorio de ficheros xbrl.
        - *statementsIPPXbrlReports.csv*: Dataset con los datos extraidos de los xbrl.

- **doc**: Contenedor documento con el enunciado de la práctica y respuestas a las cuestiones planteadas.

## Consideraciones generales

A la hora de abordar el diseño de la aplicación de scraping objetivo de la presente práctica, se ha enfocado considerando las siguientes áreas de interés:

- Se desear mantener la información en bruto de los ficheros xbrl asociados a cada informe IPP, así como sus datos generales, ya que esta información en si misma puede resultar de interés para un gran conjunto de usuarios de los datos.

  Disponer de la información en bruto permitirá poder realizar extracciones y procesados posteriores adaptadoas a las necesidades específicas de cada usuario del dataset.

- Se desea disponer de la capacidad de llevar a cabo la descarga de datos asociados a los sectores empresariales y periodos financieros deseados por cada potencial usuario de la aplicación.

- Se desea disponer de la capacidad para extraer las propiedades de los xbrl, asociadas al contexto o contextos que pueda requerir cada potencial usuario de la aplicación.

Por lo tanto:

- Se dispondrá de un almacen de ficheros xbrl

- Se contará con la flexibilidad para configurar el conjunto de datos a ser descargados desde la fuente de datos:
    * Sector / sectores financieros
    * Periodo / periodos financieros

- Se contará con la flexibilidad para configurar la extracción de datos de los xbrl:
    * Propiedad / propiedades.     
    * Contexto asociado a cada propiedad.

## Consideraciones de instalación y ejecución

Se hace uso de las siguientes librerías, por lo que en caso de no estar previamente instaladas, se requerirá proceder a su instalación:
```
pip install selenium
pip install lxml
pip install beautifulsoup4
```

Como puede observarse, se hace uso de selenium dado que la página principal de descarga suministrada por la [CNMV](http://www.cnmv.es/ipps/) tiene un alto grado de carga dinámica, esta librería por lo tanto, simplificará mucho la solución. 

Además, previo a su ejecución, se deberá revisar y ajustar la configuración de la aplicación de scraping:

- **Configuración web driver**
    - *selenium\_firefox\_path*: Configurarion para el driver firefox, indica la ruta al ejecutable de Firefox
    * *selenium\_firefox\_driver*: Configurarion para el driver firefox, indica la ruta al driver de Selenium para Firefox
    * *selenium_user_agent_comment*: Configuracón de comentario a incluir al final del user agent establecedio por el cliente web Firefox.
       El objetivo de este parámetro es meramente informativo, tratamos de añadir algún dato que permita identificar a nuestro web scraping, para facilitar las tareas de control del site para el cual se está realizando el web scraping.
       (*Nota*: Si estuieramos usando directamente algúna librería de phyton como *urllib2*, esta librería incluiría un User agent por defencto como "Python-urllib/3.0", existen *sites* donde bloquean a los robots que usan UserAgent por defecto, en estos casos es de especial relevancia incluir un valor específico en este parámetro.)
                         
- **Configuración persistencia descarga de ficheros IPP xbrl**
    * *xbrl\_ipp\_url*: Url donde se encuentran los informes ipp xbrl publicados por la CNVM
    * *xbrl\_download\_dir*: Configuración ubicación donde se ha de realizar la descarga de los ficheros zip que contienen los ficheros XBRL para una página de resultados.
    * *xbrl\_extract\_dir*: Configuración directorio donde se descombrimirán y ubicarán los ficheros xbrl resultantes de la descompresión del zip previo.

- **Configuración tiempos de espera por descarga de ficheros xbrl**     
    Se requerirá configurar una serie de parámetros para parametrizar el comportamiento de la función de espera hasta que una determinada descarga de fichero ha sido realizada.

    * *xbrl\_download\_time\_to\_wait*: Tiempo a esperar entre verificaciones de la existencia de el fichero <download_file>.part
    * *xbrl\_download\_count\_until\_filepart\_cre*: Número de veces a esperar por la aparicicón del fichero <download_file>.part
    * *xbrl\_download\_count\_until\_filepart\_del*: Número de veces a esperar por la desaparición del fichero <download_file>.part
    
    Como máximo se esperará:     
    *xbrl\_download\_time\_to\_wait \* xbrl\_download\_count\_until\_filepart\_cre \* xbrl\_download\_count\_until\_filepart\_del*

- **Configuración ámbito scraping**:
    * *sectorDictionary*: configuración de sectores empresariales para los que descargar datos
    * *periods*: configuración de periodos para los que descargar datos

- **Configuración de la extracción de datos** (ver info para configuración en [IPP Taxonomy](https://www.xbrl.es/informacion/ipp.html))
    * *xbrlPropertiesMap*: mapa de propiedades xbrl, donde la key será el nombre del elemento xbrl, y el value el contexto aplicable a dicho elemento
    
Estas propiedades pueden ser encontradas dentro de fichero *src/main.py*

Una vez configurado el scraping podrá llevarse a cabo la ejecución mediante la ejecución del comando:
```
python main.py --mode total
```
Para una ejecución completa del web scraping y extracción de propiedades xbrl.

Y de la siguiente forma:
```
python main.py --mode xbrlExtract
```
Para llevar a cabo únicamente la ejecución del proceso de extracción de propiedades xbrl.

Adicionalmente, podrá usarse el parámetro **evalrobot** con valor *True* o *False* para indicar si se desea comprobar que el web scraping requerido está permimtido según el fichero *robots.txt* del site, si se establece valor *True* y se encuentra que el scraping para *http://www.cnmv.es/ipps* no está permitido, se parará la ejecución del programa.
```
python main.py --mode total --evalrobot True
```

Esto será útil cuando se haya realizado previamente una descarga y lo único que se desee es extraer nuevas propiedades xbrl sobre los datos ya descargados.

## Referencias

1. Lawson, R.; Jarmul, Katherine (2017). _Python Web Scraping_. Packt Publishing Ltd.
2. Subirats Maté, Laia: Calvo González, Mireia (2019). _Web Scraping_. UOC.
3. [CNMV](http://www.cnmv.es/ipps/)
4. [IPP Taxonomy](https://www.xbrl.es/informacion/ipp.html)
4. [XBRL](https://xbrl.es/wp/)
5. [Selenium](https://selenium-python.readthedocs.io/api.html)
6. [Phyton](https://www.python.org/)