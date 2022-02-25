from Bio import Entrez
from Bio import Medline
import re

parametro = input ("ingrese un parámetro de restricción:")

def download_pubmed(keyword):
    
    """Esta función etá destinada a la minería de datos, y sirve para realizar una busqueda de los
    diferentes papers.
    En esta se debe ingresar como dato de entrada las palabras claves para realizar la búsqueda. 
    Además el parámetro de busqueda del tema de interés, será ingresado manualmente, previamente.
    Se empleo el paquete de Biopython Entrez y Medline para poder buscar y obtener la data.
    La información a retornar será toda la data extraida y el la cantidad de artículos."""
    
    Entrez.email = "camila.freire@est.ikiam.edu.ec"
####### db = la base de datos que desea buscar,
####### term = Declarar los filtros de busqueda, en las declaraciones de búsqueda no deben contener comillas.
    handle1 = Entrez.esearch(db="pubmed", term=keyword+parametro)
    record1 = Entrez.read(handle1)
### The default number of records that Entrez.esearch returns is 20. This is 
### to prevent overloading NCBI's servers. To get the full list of records, 
### change the retmax parameter:
    count=record1["Count"]

    handle = Entrez.esearch(db="pubmed", term=keyword+parametro,  retmax=count, usehistory ="y")
    record = Entrez.read(handle)

    ids=record["IdList"]
    print ("Total: ", record["Count"])

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
#### retmax =
    handle_efetch = Entrez.efetch(db="pubmed", rettype="medline", retmode = "text", retstart=0, retmax=1300, webenv=webenv, query_key=query_key)
    info = handle_efetch.read()
    #print(info)
    info2 = re.sub(r'\n\s{6}', ' ', info)
    
    return(info2)

def mining_pubs(tipo):
    
    """La siguiente función depende de la función download_pubmed, ya que de aquí salen todos los 
    datos a extraer. Por otra parte, en esta funcion solo se puede obtener tres tipos de datas: 
    Año de la publicacion, escribiendo DP, numero de autores por artículos, mediante en ingreso de 
    AU y el número de paises, escribiendo AD
    Como dato de entrada, se debe ingresar el codigo mencionado de cualquiera de estols tipos de 
    data. 
    Como retorno se obtiene un data frame de la información."""
    
    if tipo=='DP':
        DPs = []
        for line in info2.splitlines():
            if line.startswith("DP  -"):
                DPs.append(line[:])
            #print(DPs)
        form_text = "".join([str(_) for _ in DPs])
        DP_year = re.findall(r'\d{4}', form_text)
        #print (DP_year)
        #print(len(DP_year))
        PMID = ids
        df = pd.DataFrame()
        df['PMID'] = PMID
        df['DP_year'] = DP_year

        print(df)
    elif tipo=='AU':
        PMIDs_y_AUs = []
        AUs = []
        for line in info2.splitlines():
            if line.startswith("PMID-")+line.startswith("AU  -"):
                PMIDs_y_AUs.append(line[:])
            new_text = "".join([str(_) for _ in PMIDs_y_AUs])
            text1 = re.sub(r'PMID-', ';PMID- ', new_text)
            text2 = re.sub(r'AU  -', ' : AU  - ', text1)
        search = text2.split(';')
        search.pop(0)
        se = len(search)
        ## Para fragmentar una lista
        n=1
        output=[search[i:i + n] for i in range(0, se, n)]
        #print(output)
        ###
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
            New_Papers.append(sepa)

        #print(New_Papers)
        num_auth=[]
        for new_each in range(len(New_Papers)):
            num_AUs=len(New_Papers[new_each])
            num_auth.append(num_AUs)

        #print(num_auth)
        #len(num_auth)
    
        PMID = ids
        df2 = pd.DataFrame()
        df2['PMID'] = PMID
        df2['num_auth'] = num_auth
        print (df2)
    elif tipo=='AD':
        AUs_y_ADs = []
        AUs = []
        for line in info2.splitlines():
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
    
        unique_country = list(set(Country))

        #print(unique_country)

        #print(len(unique_country))

        #unique_country[:]
    
        # Se activa el paquete csv, que permite leer archivos con terminación .csv
        # Se abre el archivo coordenadas.csv el cual consta de los paises, las latitudes y longitudes.

        import csv
        coordenadas = {}
        with open('coordenadas.csv') as file:
            csvr = csv.DictReader(file)
            for row in csvr: # Se escoje que etiquetas se usara y se las convierte en filas
                coordenadas[row['name']] = [(row['latitude']),(row['longitude'])]

        # Se crea las listas para los nombres de los paises, la longitud, latitud, y el conteo de
        # repeticiones.

        country_name = []
        country_count = []
        # Se populiza las listas antes creadas

        for p in unique_country:
            if p in coordenadas.keys():
                country_name.append(p)
                country_count.append(Country.count(p))
    
        df3 = pd.DataFrame()
        df3['country_name'] = country_name
        df3['country_count'] = country_count
        print (df3)
    return() 