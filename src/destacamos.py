from selenium.webdriver.common.by import By
from utils import *
import itertools
import time

#mirar porque se descarga solo 1
start_time = time.time()
def descargar_datos_destacamos(num_pag,categoria):


    paginas = get_pages("https://www.destacamos.com/"+categoria+"/{}/listings.html",num_pag)
    drivers = get_drivers(paginas)
    cnt = num_pag[0]

    #pasandole la lista de nombres tal y como en páginas con el range
    #hacer una función en utils que saque el pickle de cada nodo de una lista de drivers
    for driver in drivers:
        path_paginacion = os.path.join("databases", "destacamos", categoria, str(cnt))
        pickle_file_name = "destacamos_"+categoria+"_"+str(cnt)+".pkl"
        cnt = cnt+1

        serialize_pickle_node(driver,path_paginacion,pickle_file_name)

    pag_nodes = get_nodes_from_driver(drivers,[By.CLASS_NAME,"titulo"])

    #al igual que el anterior, se le pasa el range de contador para tener
    #este valor en cuenta
    #necesario quizás hacer una tupla de valores (driver,num_pag) para evitar
    #problemas de condición de corrida
    cnt = num_pag[0]
    for node in pag_nodes:
        node = list(map(lambda x: apply_action(x, [By.TAG_NAME, "a"]), node))

        hrefs = get_href_from_nodes(node)

        drivers_href = get_drivers(hrefs)
        cnt_href = 1
        for driver_href in drivers_href:
            path_paginacion_href = os.path.join("databases", "destacamos", categoria, str(cnt),str(cnt_href))
            pickle_file_name_href = "destacamos_" + categoria + "_" + str(cnt) + "_" + str(cnt_href)+ ".pkl"
            cnt_href = cnt_href + 1

            serialize_pickle_node(driver_href, path_paginacion_href, pickle_file_name_href)
            get_imgs_from_node(driver_href, path_paginacion_href)
        cnt = cnt + 1

descargar_datos_destacamos(range(1,3),"1-chicas-escorts")

end_time = time.time()

print(end_time-start_time)



