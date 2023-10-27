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
    drivers = get_drivers(paginas)
    #sacamos el path comun
    common_path = os.path.join("databases","destacamos",categoria,"{}")
    #escribimos en local todos los html
    serialize_nodes_html(drivers,num_pag,common_path,["destacamos_"+categoria+"_page_"+str(i)+".html" for i in num_pag])


    #sacamos los nodos de los anuncios dentro de cada driver
    pag_nodes = get_nodes_from_driver(drivers,[By.CLASS_NAME,"titulo"])

    nodes_list_atr_a = [np.vectorize(lambda x: apply_action(x, [By.TAG_NAME,"a"]))(node) for node in pag_nodes]
    # #obtenemos el nodo de la url de cada uno de ellos
    get_nodes_hrefs = get_href_nodes_from_nodes(nodes_list_atr_a)

    #cerramos los drivers anteriores para abaratar la carga
    # close_drivers(drivers)

    # drivers_shows = np.apply_along_axis(get_drivers,axis=1,arr=get_nodes_hrefs)
    drivers_shows_list = []
    cnt = num_pag[0]
    for a in get_nodes_hrefs:


        init_file_name = "destacamos_"+categoria+"_page_"+str(cnt)
        cnt_show = 1
        for b in a:
            try:
                init_path = os.path.join("databases","destacamos", categoria, str(cnt),str(cnt_show))
                file_name = init_file_name + "_" + str(cnt_show) + ".html"

                response = requests.get(b,timeout=5)
                response.raise_for_status()
                html_content = response.text
                # print("Sacando el show numero ", cnt_show)
                drivers_shows_list.append([html_content,init_path])
                if not os.path.exists(init_path):
                    os.makedirs(init_path)
                with open(os.path.join(init_path, file_name), 'w', encoding='utf-8') as file:
                    file.write(html_content)
            except requests.exceptions.RequestException as e:
                print(f"Error en la solicitud: {e}")
                response = None
            cnt_show = cnt_show+1
        cnt = cnt+1


    for nod in drivers_shows_list:
        soup = BeautifulSoup(nod[0],"html.parser")

        get_imgs_from_node_bs4(soup,nod[1])



num_paginas_a_scrapear = 1320
categoria_a_scrapear = "1-chicas-escorts"
for i in range(1,int(num_paginas_a_scrapear/2)):
    try:
        descargar_datos_destacamos(range(2*i,(2*i)+2),categoria_a_scrapear)
    except:
        print("Error encontrado descargando la página")
    end_time = time.time()
    print("El proceso descargando por la página " +str(2*i)+" tardando: ",end_time - start_time)


