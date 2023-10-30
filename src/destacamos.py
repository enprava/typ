import requests
from selenium.webdriver.common.by import By
from utils import *
import itertools
import time


start_time = time.time()

def descargar_datos_destacamos(num_pag,categoria):
    #obtenemos las url de las páginas

    paginas = get_pages("https://www.destacamos.com/"+categoria+"/{}/listings.html",num_pag)

    #obtener los drivers de estas url
    # drivers = get_drivers(paginas)
    html_pages = get_html_from_urls(paginas)
    #sacamos el path comun
    common_path = os.path.join("databases","destacamos",categoria,"{}")
    #escribimos en local todos los html
    serialize_nodes_html(html_pages,num_pag,common_path,["destacamos_"+categoria+"_page_"+str(i)+".html" for i in num_pag])


    #sacamos los nodos de los anuncios dentro de cada driver
    # pag_nodes = get_nodes_from_driver(drivers,[By.CLASS_NAME,"titulo"])
    pag_nodes = get_nodes_from_htmls(html_pages)
    #sacamos los show
    pag_nodes_shows = apply_action_to_bs4_nodes(pag_nodes,["h2",{"class":"titulo"}])

    #sacamos los nodos a de cada uno de los nodos

    #buscamos elementos
    # nodes_list_atr_a = [np.vectorize(lambda x: apply_action(x, [By.TAG_NAME,"a"]))(node) for node in pag_nodes]
    nodes_list_atr_a = [get_ahref_node_from_bs4_nodes(nodes) for nodes in pag_nodes_shows]


    html_shows_pages = np.vectorize(get_html_from_urls)(nodes_list_atr_a)

    cnt = num_pag[0]
    drivers_shows_list = []
    for i in range(len(html_shows_pages)):

        path_comun = os.path.join("databases", "destacamos", categoria, str(i+num_pag[0]), "{}")
        range_show = range(1,len(html_shows_pages[i])+1)

        # escribimos en local todos los html
        s_nodes = serialize_nodes_html(html_shows_pages[i],range_show , path_comun,
                             ["destacamos_" + categoria + "_page_" + str(i+num_pag[0]) + "_" + str(w) + ".html"
                              for w in range_show])

        download_images_from_rows(html_shows_pages[i],s_nodes)


num_paginas_a_scrapear = 1320
categoria_a_scrapear = "9-escorts-lujo"
for i in range(1,int(num_paginas_a_scrapear/2)):

    descargar_datos_destacamos(range(2*i,(2*i)+2),categoria_a_scrapear)


    end_time = time.time()
    print("El proceso descargando por la página " +str(2*i)+" tardando: ",end_time - start_time)


