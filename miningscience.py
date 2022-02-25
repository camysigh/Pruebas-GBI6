from Bio import Entrez
from Bio.Seq import Seq
from Bio import Medline
import re
import pandas as pd

parametro = input ("Ingrese un parámetro de restricción. Ejem [title/Abstract]:")

def download_pubmed(keyword):
    
    """Esta función está destinada a la minería de datos, y sirve para realizar una búsqueda de
    diferentes papers de un tema en específico.
    \nEn esta se debe ingresar como dato de entrada las palabras claves para realizar la búsqueda,
    entre comillas. 
    \nAdemás el parámetro de búsqueda del tema de interés, será ingresado manualmente, como se 
    muestra en el ejemplo del input.
    \nSe empleó el paquete de Biopython Entrez y Medline para poder buscar y obtener la data.
    \nLa información a retornar será toda la data extraída y la cantidad de artículos 
    encontrados."""
    
    Entrez.email = "camila.freire@est.ikiam.edu.ec"
####### db = la base de datos que desea buscar,
####### term = Declarar los filtros de busqueda, en las declaraciones de búsqueda no deben contener comillas.
    handle1 = Entrez.esearch(db="pubmed", term=keyword+parametro)
    record1 = Entrez.read(handle1)
### El número predeterminado de registros que devuelve Entrez.esearch es 20. Esto es
### para evitar sobrecargar los servidores de NCBI. Para obtener la lista completa de registros,
### cambie el parámetro retmax:
    count=record1["Count"]
## Entrez.esearch - para buscar la información requirida
    handle = Entrez.esearch(db="pubmed", term=keyword+parametro,  retmax=count, usehistory ="y")
    record = Entrez.read(handle) # Para que se lea handle y que se guarde en la nueva variable record

# Guardar la IdList en una nueva variables, se saca la Id List de record
    ids=record["IdList"]
    #print ("Total: ", record["Count"])

# Parámetros de entorno web (&WebEnv) y clave de consulta (&query_key) que especifican la ubicación 
# en el servidor de historial de Entrez de la lista de UID cargados
    
    webenv = record["WebEnv"] 
    query_key = record["QueryKey"]

#### retype = Tipo de recuperación. Hay dos valores permitidos para ESearch: 
            #'uilist' (predeterminado), que muestra la salida XML estándar, y 'count', 
            # que muestra solo la etiqueta <Count>.
#### remode =
#### retstart = Índice secuencial del primer UID del conjunto recuperado que se mostrará en la salida XML 
            #(predeterminado=0, correspondiente al primer registro de todo el conjunto). 
            # Este parámetro se puede usar junto con retmax para descargar un subconjunto arbitrario de 
            # UID recuperados de una búsqueda.
#### retmax = Muestra la cantidad de archivos a buscar
    handle_efetch = Entrez.efetch(db="pubmed", rettype="medline", retmode = "text", retstart=0, retmax=1300, webenv=webenv, query_key=query_key) # efetch permite descargar la data
    info = handle_efetch.read()
    #print(info)
    info2 = re.sub(r'\n\s{6}', ' ', info)
    
    return(info2)

########################################## Otra función

def mining_pubs(data_descargada, tipo):
    
    """Previo a utilizar la función se debe cargar el el archivo miningscience como módulo msc.
    \nLa siguiente función depende de la función download_pubmed, ya que primero se le debe 
    asignar a una variable de cualquier nombre, los valores retornados por la función 
    download_pubmed. EJM Papers=msc.download_pubmed('Ecuador proteomics'). 
    \nPor otra parte, en esta función sólo se puede obtener tres tipos de datas: 
    Año de la publicación, escribiendo DP, número de autores por artículos, mediante 
    el ingreso de AU y el número de países, escribiendo AD.
    \nComo dato de entrada, se debe ingresar el nombre de la variable a la que se le ha asignado
    los valores de la función download_pubmed. EJM: Papers. Así como, el código mencionado de 
    cualquiera de estos tipos de data entre comillas.(Estos son separados por coma)
    \nEJEMPLO: msc.download_pubmed(Papers, 'DP'). 
    \nComo retorno se obtiene un data frame de la información requerida."""
### Para obtener los años y los PMIDs    
    if tipo=='DP':
        DPs = [] # crear lista vacia
        for line in data_descargada.splitlines():
            if line.startswith("DP  -"):# Para reconocer unicamente las lineas que inician con DP -
                DPs.append(line[:])# guardar las lineas reconocidas anteriormente en una lista vacia
            #print(DPs)
        form_text = "".join([str(_) for _ in DPs]) # cambiar de formato str a lista
        DP_year = re.findall(r'\d{4}', form_text) # buscar los codigos PMIDs
        #print (DP_year)
        #print(len(DP_year))
        PMID= re.findall(r'[P][M][I][D]\-\s(\d*)',data_descargada) # Hacer una lista de los PMIDs como palabra
        df = pd.DataFrame() # Generar un dataframe con ambas lista creadas
        df['PMID'] = PMID
        df['DP_year'] = DP_year

        #print(df)
    elif tipo=='AU':
        PMIDs_y_AUs = []
        AUs = []
        for line in data_descargada.splitlines():
            if line.startswith("PMID-")+line.startswith("AU  -"): # Buscar las lineas que comiencen con PMID
                PMIDs_y_AUs.append(line[:])                       # Para de esa manera ordenar los autores segun PMID
            new_text = "".join([str(_) for _ in PMIDs_y_AUs]) # Se repiten los pasos mencionados 
            text1 = re.sub(r'PMID-', ';PMID- ', new_text) # utiliza estos comandos para separar cada PMID y AU 
            text2 = re.sub(r'AU  -', ' : AU  - ', text1)
        search = text2.split(';') # Se separa la lista en elementos en cada ;
        search.pop(0) # Se elimina el primer elemento que corresponde a un espacio en blanco
        se = len(search)
        ## Para fragmentar una lista
        n=1
        output=[search[i:i + n] for i in range(0, se, n)] # Se framenta la multilista generada
        #print(output)
        ###
        Papers=[]
        New_Papers=[]
        for each in range(len(output)):
            Papers=output[each]
            #print("\n", Papers)
            new_text1 = "".join([str(_) for _ in Papers])
            text_1 = re.sub(r' AU  -', 'AU  -', new_text1) # quita el espacio entre : y AU
            #print("\n", new_text1)
            sepa = text_1.split(':') # Se separa las multilistas en nuevos elementos cada :
            sepa.pop(0) 
            New_Papers.append(sepa) # Se guarda la informacion en una lista vacia creada anteriormente 

            ## Conteo de numero de autores mediante:
        #print(New_Papers)
        num_auth=[] 
        for new_each in range(len(New_Papers)):
            num_AUs=len(New_Papers[new_each])
            num_auth.append(num_AUs)

        #print(num_auth)
        #len(num_auth)
    ### Generacion de data frame
        PMID= re.findall(r'[P][M][I][D]\-\s(\d*)',data_descargada)
        df = pd.DataFrame()
        df['PMID'] = PMID
        df['num_auth'] = num_auth
        #print (df2)
     
    ### Para obtener los paises y el numero de estos se repite los pasos antes mencionados 
    elif tipo=='AD':
        AUs_y_ADs = []
        AUs = []
        for line in data_descargada.splitlines():
            if line.startswith("AU  -")+line.startswith("AD  -"):
                AUs_y_ADs.append(line[:])
            new_text = "".join([str(_) for _ in AUs_y_ADs])
            text1 = re.sub(r'AU  -', '+AU  - ', new_text)
            text2 = re.sub(r'AD  -', ':AD  - ', text1)
        #print(AUs_y_ADs)
        #print(text2)
        search = text2.split('+')
        #search.pop(0)
        search.pop(0)
        se = len(search)
        ## Para fragmentar una lista
        n=1
        output=[search[i:i + n] for i in range(0, se, n)]
    
        #print(output)

        Papers=[]
        New_Papers=[]
        for each in range(len(output)):
            Papers=output[each]
            #print("\n", Papers)
            new_text1 = "".join([str(_) for _ in Papers])
            text_1 = re.sub(r' AU  -', 'AU  -', new_text1)
            #print("\n", new_text1)
            sepa = text_1.split(':')
            sepa.pop(0)
            #print(sepa)
            New_Papers.append(sepa)

        #print(len(New_Papers))
        #print(New_Papers)

        new_text2 = "".join([str(_) for _ in New_Papers])

        ### Para los paises que tiene 2 nombres con patrón , NombreUno NombreDos.'
        ## , United Kingdom.'
        text_2 = re.findall(r'\,\s([A-Z]{1}[a-z]{1}\w+\s[A-Z]{1}[a-z]{1}\w+)\.\'',  new_text2)

        #print(len(text_2))
        #print(text_2)
        ### Para los paises con un solo nombre que tengan el patrón , Pais.'
        text_3 = re.findall(r'\,\s([A-Z]{1}[a-z]{1}\w+)\.\'', new_text2)
        #print(len(text_3))
        #print(text_3)
        ### Para USA y UK: patrones como: 
        text_4 = re.findall(r'\,\s([U]{1}[A-Z]{1,2})\.\'', new_text2)
        #print(len(text_4)) #109
        #print(text_4)

        ### Para USA y UK
        text_5 = re.findall(r'\s[\sA-Za-z{1:50}]+\,\s([A-Z]{3})\.\'', new_text2)
        #print(len(text_5)) #43
        #print(text_5)

        ### Pais con un parrafo que se separa con espacios, puntos o comas y es solo texto en mayusculas 
        ### para centrarse en USA
        text_6 = re.findall(r'\s[\s\'A-Za-zÀ-ÿ{1:50}]+\s([U]{1}[A-Z]{1,2})\.\'', new_text2)
        #print(len(text_6)) #41
        #print(text_6)

        ## #Paices con cuatro palabra
        text_7 = re.findall(r'\,\s([A-Z]{1}[a-z]{1,20}\s[A-Z]{1}[a-z]{1,20}\s[a-z]{2}\s[A-Z]{1}[a-z]{1,20})\.\'', new_text2)
        #print(len(text_7)) #6
        #print(text_7)

        ### Para los paises que tiene 2 nombres con patrón , NombreUno NombreDos'
        ## , United Kingdom'
        text_8 = re.findall(r'\,\s([A-Z]{1}[a-z]{1}\w+\s[A-Z]{1}[a-z]{1}\w+)\'',  new_text2)

        #print(len(text_8))#1
        #print(text_8)

        ### Para los paises cuyo patrón es , Nombre. [correo electrónico]'
        ## , Spain. bgzorn@ucm.es.'
        text_9 = re.findall(r'\,\s([A-Z]{1}[a-z]{1}\w+)\.\s[a-z0-9_\.-]+@[\da-z\.-]+\.[a-z\.]{2,6}\.\'',  new_text2)

        #print(len(text_9)) #15
        #print(text_9)

        ### Para los paises cuyo patrón es , Nombre; [correo electrónico]'
        ## , Canada; joseph.orkin@upf.edu amanda.melin@ucalgary.ca.'
        text_10 = re.findall(r',\s([\sA-Za-z{1:50}]+)\;\s[a-z0-9_\.-]+@[\da-z\.-]+\.[a-z\.]{1,6}\s',  new_text2)

        #print(len(text_10)) #2
        #print(text_10)

        ### Para los estados de USA , Philadelphia, PA 19107.'

        text_11 = re.findall(r'\,\s([A-Z]{1}[a-z]{1}\w+)\,\s[A-Z]{2}\s\d*\.\'',  new_text2)

        #print(len(text_11)) #4
        #print(text_11)

        ### Para los paises con patron: , USA. Electronic address: sfitz@msu.edu.'
        ## Paises como Ecuador

        text_12 = re.findall(r'\,\s([A-Z]{1}[a-z]{1}\w+)\.\s[E]{1}[a-z]{9}',  new_text2)

        #print(len(text_12)) #2
        #print(text_12)

        ## Paises como USA

        text_13 = re.findall(r'\,\s([U]{1}[A-Z]{1,2}\w+)\.\s[E]{1}[a-z]{9}',  new_text2)

        #print(len(text_13)) #1
        #print(text_13)
    
        ### Paises que tienen al final del parrafo ; 
        ### , United Kingdom;

        text_14 = re.findall(r'\,\s([\sA-Za-z{1:50}]+)\;\'', new_text2)

        #print(len(text_14)) #4
        #print(text_14)

        # Barcelona, Spain."

        text_15 = re.findall(r'\,\s([A-Z]{1}[a-z]{1}\w+)\.\"', new_text2)

        #print(len(text_15)) #9
        #print(text_15)

        # , Panama c.jiggins@zoo.cam.ac.uk.'

        text_16 = re.findall(r'\,\s([A-Z]{1}[a-z]{1}\w+)\s\w*\.\w*\@\w*\.\w*\.\w*\.w*', new_text2)

        #print(len(text_16)) #1
        #print(text_16)

        # Santa Cruz Ecuador.'

        text_17 = re.findall(r'[A-Z]{1}[a-z]{1}\w+\s[A-Z]{1}[a-z]{1}\w+\s([A-Z]{1}[a-z]{1}\w+)\.\'', new_text2)

        #print(len(text_17)) #16
        #print(text_17)

        # Santa Cruz USA.'

        text_18 = re.findall(r'[A-Z]{1}[a-z]{1}\w+\s[A-Z]{1}[a-z]{1}\w+\s([U]{1}[A-Z]{1,2})\.\'', new_text2)

        #print(len(text_18)) #12
        #print(text_18)

        # INIAP) Quito Ecuador.'

        text_19 = re.findall(r'\)\s[A-Z]{1}[a-z]{1}\w+\s([A-Z]{1}[a-z]{1}\w+)\.\'', new_text2)

        #print(len(text_19)) #1
        #print(text_19)

        # Idaho Moscow ID USA.'

        text_20 = re.findall(r'[A-Z]{1}\w+\s[A-Z]{2}\s([U]{1}[A-Z]{1,2})\.\'', new_text2)

        #print(len(text_20)) #22
        #print(text_20)
    
        #, NY USA.

        text_21 = re.findall(r'\,\s[A-Z]+\s([U]{1}[A-Z]{1,2})\.\'', new_text2)

        #print(len(text_21)) #4
        #print(text_21)

        # Quito, Ecuador;'

        text_22 = re.findall(r'\,\s([A-Z]{1}[a-z]{1}\w+)\;\'', new_text2)

        #print(len(text_22)) #1
        #print(text_22)

        # , USA;'

        text_23 = re.findall(r'\,\s([U]{1}[A-Z]{1,2})\;\'', new_text2)

        #print(len(text_23)) #1
        #print(text_23)

        #, Ecuador .'

        text_24 = re.findall(r'\,\s([A-Z]{1}[a-z]{1}\w+)\s\.\'', new_text2)

        #print(len(text_24)) #7
        #print(text_24) 
    
    ### Se unen todas las listas creadas anteriormente
        text_2.extend(text_3)
        text_2.extend(text_4)
        text_2.extend(text_5)
        text_2.extend(text_6)
        text_2.extend(text_7)
        text_2.extend(text_8)
        text_2.extend(text_9)
        text_2.extend(text_10)
        text_2.extend(text_11)
        text_2.extend(text_12)
        text_2.extend(text_13)
        text_2.extend(text_14)
        text_2.extend(text_15)
        text_2.extend(text_16)
        text_2.extend(text_17)
        text_2.extend(text_18)
        text_2.extend(text_19)
        text_2.extend(text_20)
        text_2.extend(text_21)
        text_2.extend(text_22)
        text_2.extend(text_23)
        text_2.extend(text_24)
        #print(text_2)
        
        ### Se unifica la escritura del nombre de algunos paises 
        country=[]
        Country=[]
        for e in range(len(text_2)):
            country=text_2[e]
            #print(country)
            if country == "United States":
                country = 'USA'
            if country == "United States of America":
                country = 'USA'
            if country == "United Kingdom":
                country = 'UK'
            Country.append(country)

        #print(Country)
    
        unique_country = list(set(Country)) # se crea una lista unica con los nombres de los paises 
        
        unique_c=sorted(unique_country) ## Ordenar alfabeticamente una lista

        #print(unique_c)

        #print(len(unique_c))

        #unique_c[:57]
    
        # Se activa el paquete csv, que permite leer archivos con terminación .csv
        # Se abre el archivo coordenadas.csv el cual consta de los paises, las latitudes y longitudes.

        import csv
        coordenadas = {}
        with open('data/coordenadas.csv') as file:
            csvr = csv.DictReader(file)
            for row in csvr: # Se escoje que etiquetas se usara y se las convierte en filas
                coordenadas[row['name']] = [(row['latitude']),(row['longitude'])]

        # Se crea las listas para los nombres de los paises, la longitud, latitud, y el conteo de
        # repeticiones.

        country_name = []
        country_count = []
        # Se populiza las listas antes creadas

        for p in unique_c:
            if p in coordenadas.keys():
                country_name.append(p)
                country_count.append(Country.count(p))
    #### Creacion de dataframe
        df = pd.DataFrame()
        df['country_name'] = country_name
        df['country_count'] = country_count
        #print (df3)
    return(df) 