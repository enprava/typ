from utils import *
import time
import math
import logging
import sys

fmt = "[%(asctime)-15s] [%(levelname)s] %(name)s: %(message)s"
logging.basicConfig(format=fmt, level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger("Escort Advisor")
info = [
    {"609": "https://www.escort-advisor.xxx/escort/acoruna/{}"},
    {"336": "https://www.escort-advisor.xxx/escort/alava/{}"},
    {"86": "https://www.escort-advisor.xxx/escort/albacete/{}"},
    {"680": "https://www.escort-advisor.xxx/escort/alicante/{}"},
    {"112": "https://www.escort-advisor.xxx/escort/almeria/{}"},
    {"463": "https://www.escort-advisor.xxx/escort/asturias/{}"},
    {"21": "https://www.escort-advisor.xxx/escort/avila/{}"},
    {"274": "https://www.escort-advisor.xxx/escort/badajoz/{}"},
    {"2853": "https://www.escort-advisor.xxx/escort/barcelona/{}"},
    {"100": "https://www.escort-advisor.xxx/escort/burgos/{}"},
    {"81": "https://www.escort-advisor.xxx/escort/caceres/{}"},
    {"127": "https://www.escort-advisor.xxx/escort/cadiz/{}"},
    {"350": "https://www.escort-advisor.xxx/escort/cantabria/{}"},
    {"100": "https://www.escort-advisor.xxx/escort/castellon/{}"},
    {"5": "https://www.escort-advisor.xxx/escort/ceuta/{}"},
    {"206": "https://www.escort-advisor.xxx/escort/ciudadreal/{}"},
    {"172": "https://www.escort-advisor.xxx/escort/cordoba/{}"},
    {"114": "https://www.escort-advisor.xxx/escort/cuenca/{}"},
    {"17": "https://www.escort-advisor.xxx/escort/fuerteventura/{}"},
    {"165": "https://www.escort-advisor.xxx/escort/girona/{}"},
    {"116": "https://www.escort-advisor.xxx/escort/grancanaria/{}"},
    {"262": "https://www.escort-advisor.xxx/escort/granada/{}"},
    {"148": "https://www.escort-advisor.xxx/escort/guadalajara/{}"},
    {"323": "https://www.escort-advisor.xxx/escort/guipuzcoa/{}"},
    {"50": "https://www.escort-advisor.xxx/escort/huelva/{}"},
    {"134": "https://www.escort-advisor.xxx/escort/huesca/{}"},
    {"279": "https://www.escort-advisor.xxx/escort/islasbaleares/{}"},
    {"174": "https://www.escort-advisor.xxx/escort/jaen/{}"},
    {"221": "https://www.escort-advisor.xxx/escort/larioja/{}"},
    {"12": "https://www.escort-advisor.xxx/escort/lanzarote/{}"},
    {"301": "https://www.escort-advisor.xxx/escort/leon/{}"},
    {"97": "https://www.escort-advisor.xxx/escort/lleida/{}"},
    {"115": "https://www.escort-advisor.xxx/escort/lugo/{}"},
    {"3643": "https://www.escort-advisor.xxx/escort/madrid/{}"},
    {"602": "https://www.escort-advisor.xxx/escort/malaga/{}"},
    {"1": "https://www.escort-advisor.xxx/escort/melilla/{}"},
    {"345": "https://www.escort-advisor.xxx/escort/murcia/{}"},
    {"299": "https://www.escort-advisor.xxx/escort/navarra/{}"},
    {"86": "https://www.escort-advisor.xxx/escort/ourense/{}"},
    {"40": "https://www.escort-advisor.xxx/escort/palencia/{}"},
    {"430": "https://www.escort-advisor.xxx/escort/pontevedra/{}"},
    {"199": "https://www.escort-advisor.xxx/escort/salamanca/{}"},
    {"21": "https://www.escort-advisor.xxx/escort/segovia/{}"},
    {"356": "https://www.escort-advisor.xxx/escort/sevilla/{}"},
    {"26": "https://www.escort-advisor.xxx/escort/soria/{}"},
    {"139": "https://www.escort-advisor.xxx/escort/tarragona/{}"},
    {"107": "https://www.escort-advisor.xxx/escort/tenerife/{}"},
    {"21": "https://www.escort-advisor.xxx/escort/teruel/{}"},
    {"172": "https://www.escort-advisor.xxx/escort/toledo/{}"},
    {"1062": "https://www.escort-advisor.xxx/escort/valencia/{}"},
    {"193": "https://www.escort-advisor.xxx/escort/valladolid/{}"},
    {"349": "https://www.escort-advisor.xxx/escort/vizcaya/{}"},
    {"16": "https://www.escort-advisor.xxx/escort/zamora/{}"},
    {"928": "https://www.escort-advisor.xxx/escort/zaragoza/{}"},
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
            response = requests.get(url.format(i))
            soup = BeautifulSoup(response.text, 'html.parser')
            logger.info("Guardando listas")

            save_soup(soup, f"databases/escort-advisor/lists/{categoria}", str(i) + ".html")

            anuncios = soup.find_all('div',attrs={'class':'serp_block_container'})
            hrefs = []
            for anuncio in anuncios:
                a = anuncio.find('a')
                if a:
                    hrefs.append(f"https://www.escort-advisor.xxx{a.attrs.get('href')}")
            logger.info("Comenzando extracción de shows")
            download(
                hrefs, f"databases/escort-advisor/shows/{categoria}"
            )
            end_time = time.time()
        logger.info(
            "Se ha descargado {} en {} segundos".format(url, end_time - start_time)
        )
global_end_time = time.time()

logger.info(
    "Se ha descargado todo en {} segundos".format(global_end_time - global_start)
)
