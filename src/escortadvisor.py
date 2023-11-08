from utils import *
import time
import math
import logging
import sys

fmt = "[%(asctime)-15s] [%(levelname)s] %(name)s: %(message)s"
logging.basicConfig(format=fmt, level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger("Escort Advisor")
info = [
    {"607": "https://es-es.escort-advisor.com/escort/acoruna/{}"},
    {"328": "https://es-es.escort-advisor.com/escort/alava/{}"},
    {"84": "https://es-es.escort-advisor.com/escort/albacete/{}"},
    {"680": "https://es-es.escort-advisor.com/escort/alicante/{}"},
    {"114": "https://es-es.escort-advisor.com/escort/almeria/{}"},
    {"455": "https://es-es.escort-advisor.com/escort/asturias/{}"},
    {"18": "https://es-es.escort-advisor.com/escort/avila/{}"},
    {"276": "https://es-es.escort-advisor.com/escort/badajoz/{}"},
    {"2840": "https://es-es.escort-advisor.com/escort/barcelona/{}"},
    {"98": "https://es-es.escort-advisor.com/escort/burgos/{}"},
    {"80": "https://es-es.escort-advisor.com/escort/caceres/{}"},
    {"128": "https://es-es.escort-advisor.com/escort/cadiz/{}"},
    {"356": "https://es-es.escort-advisor.com/escort/cantabria/{}"},
    {"101": "https://es-es.escort-advisor.com/escort/castellon/{}"},
    {"6": "https://es-es.escort-advisor.com/escort/ceuta/{}"},
    {"204": "https://es-es.escort-advisor.com/escort/ciudadreal/{}"},
    {"174": "https://es-es.escort-advisor.com/escort/cordoba/{}"},
    {"115": "https://es-es.escort-advisor.com/escort/cuenca/{}"},
    {"17": "https://es-es.escort-advisor.com/escort/fuerteventura/{}"},
    {"145": "https://es-es.escort-advisor.com/escort/girona/{}"},
    {"114": "https://es-es.escort-advisor.com/escort/grancanaria/{}"},
    {"257": "https://es-es.escort-advisor.com/escort/granada/{}"},
    {"148": "https://es-es.escort-advisor.com/escort/guadalajara/{}"},
    {"315": "https://es-es.escort-advisor.com/escort/guipuzcoa/{}"},
    {"50": "https://es-es.escort-advisor.com/escort/huelva/{}"},
    {"133": "https://es-es.escort-advisor.com/escort/huesca/{}"},
    {"272": "https://es-es.escort-advisor.com/escort/islasbaleares/{}"},
    {"177": "https://es-es.escort-advisor.com/escort/jaen/{}"},
    {"216": "https://es-es.escort-advisor.com/escort/larioja/{}"},
    {"11": "https://es-es.escort-advisor.com/escort/lanzarote/{}"},
    {"304": "https://es-es.escort-advisor.com/escort/leon/{}"},
    {"94": "https://es-es.escort-advisor.com/escort/lleida/{}"},
    {"119": "https://es-es.escort-advisor.com/escort/lugo/{}"},
    {"3632": "https://es-es.escort-advisor.com/escort/madrid/{}"},
    {"583": "https://es-es.escort-advisor.com/escort/malaga/{}"},
    {"1": "https://es-es.escort-advisor.com/escort/melilla/{}"},
    {"346": "https://es-es.escort-advisor.com/escort/murcia/{}"},
    {"295": "https://es-es.escort-advisor.com/escort/navarra/{}"},
    {"86": "https://es-es.escort-advisor.com/escort/ourense/{}"},
    {"38": "https://es-es.escort-advisor.com/escort/palencia/{}"},
    {"429": "https://es-es.escort-advisor.com/escort/pontevedra/{}"},
    {"198": "https://es-es.escort-advisor.com/escort/salamanca/{}"},
    {"20": "https://es-es.escort-advisor.com/escort/segovia/{}"},
    {"348": "https://es-es.escort-advisor.com/escort/sevilla/{}"},
    {"28": "https://es-es.escort-advisor.com/escort/soria/{}"},
    {"143": "https://es-es.escort-advisor.com/escort/tarragona/{}"},
    {"108": "https://es-es.escort-advisor.com/escort/tenerife/{}"},
    {"20": "https://es-es.escort-advisor.com/escort/teruel/{}"},
    {"169": "https://es-es.escort-advisor.com/escort/toledo/{}"},
    {"1064": "https://es-es.escort-advisor.com/escort/valencia/{}"},
    {"192": "https://es-es.escort-advisor.com/escort/valladolid/{}"},
    {"349": "https://es-es.escort-advisor.com/escort/vizcaya/{}"},
    {"15": "https://es-es.escort-advisor.com/escort/zamora/{}"},
    {"937": "https://es-es.escort-advisor.com/escort/zaragoza/{}"},
]
global_start = time.time()
for information in info:
    for anuncios, url in information.items():
        start_time = time.time()
        npages = math.ceil(int(anuncios) / 20)
        categoria = url.split("/")[-2]
        for i in range(1, npages + 1):
            logger.info(
                "Descargando página {} de {}. Ciudad: {}".format(i, npages, categoria)
            )
            driver = init_driver(url.format(i))
            try:
                logger.info("Aceptando política de mayoría de edad")
                do_click(driver, [[By.CSS_SELECTOR, ".cookie_disclaimer_button"]])
            except:
                logger.info("No hacemos click")
            logger.info("Guardando listas")
            save_node(
                driver, f"databases/escort-advisor/lists/{categoria}", str(i) + ".html"
            )
            nodes = driver.find_elements(By.CLASS_NAME, "serp_block_container")
            nodes = list(map(lambda y: apply_actions(y, [[By.TAG_NAME, "a"]]), nodes))
            del nodes[0]
            hrefs = get_href_from_nodes(nodes)
            logger.info("Comenzando extracción de shows")
            download_slow_as_a_turtle(
                hrefs, f"databases/escort-advisor/shows/{categoria}"
            )
            driver.close()
            end_time = time.time()
        logger.info(
            "Se ha descargado {} en {} segundos".format(url, end_time - start_time)
        )
global_end_time = time.time()

logger.info(
    "Se ha descargado todo en {} segundos".format(global_end_time - global_start)
)
