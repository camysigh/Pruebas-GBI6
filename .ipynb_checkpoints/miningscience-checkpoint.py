from Bio import Entrez
from Bio import Medline
import re

parametro = input ("ingrese un parámetro de restricción:")

def download_pubmed(keyword):
    """Donstring, Holi"""
    Entrez.email = "camila.freire@est.ikiam.edu.ec"
####### db = la base de datos que desea buscar,
####### term = Declarar los filtros de busqueda, en las declaraciones de búsqueda no deben contener comillas.
    handle = Entrez.esearch(db="pubmed", term=keyword+parametro, usehistory ='Y')
    record = Entrez.read(handle)
    webenv = record["WebEnv"]
    query_key = record["QueryKey"]
    ids=record["IdList"]
    print ("Total: ", record["Count"])
#### retype = Tipo de recuperación. Hay dos valores permitidos para ESearch: 
            #'uilist' (predeterminado), que muestra la salida XML estándar, y 'count', 
            # que muestra solo la etiqueta <Count>.
#### remode =
#### retstart = Índice secuencial del primer UID del conjunto recuperado que se mostrará en la salida XML 
            #(predeterminado=0, correspondiente al primer registro de todo el conjunto). 
            # Este parámetro se puede usar junto con retmax para descargar un subconjunto arbitrario de 
            # UID recuperados de una búsqueda.
#### retmax =
    handle_efetch = Entrez.efetch(db="pubmed", id=ids, rettype="medline", retmode = "text", retstart=0, retmax=530, webenv=webenv,
                                  query_key=query_key)
    #info = handle_efetch.read()
    #print(info)
    info2 = re.sub(r'\n\s{6}', ' ', handle_efetch.read())
    print(info2)
    len(info2)

    return ()

#def mining_pubs('tipo'):
    
    #if tipo = DP 
    

    
    
    #return 