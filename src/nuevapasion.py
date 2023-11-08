from selenium.webdriver.common.by import By
from utils import *
import requests
import logging
import sys
from bs4 import BeautifulSoup
import pandas as pd
import time

fmt = '[%(asctime)-15s] [%(levelname)s] %(name)s: %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger('NuevaPasion')

base = 'https://nuevapasion.com/anuncios?page={}'
npages = 547
if not os.path.exists('databases/nuevapasion/'):
    os.makedirs('databases/nuevapasion/')
url_shows = 'https://nuevapasion.com{}'
logger.info('Comenzando extracción')
for i in range(1, 1+npages):
    if not os.path.exists('databases/nuevapasion/{}'.format(i)):
        os.mkdir('databases/nuevapasion/{}'.format(i))
    url = base.format(i)
    logger.info('Realizando petición de {}'.format(url))
    response = requests.get(url)
    logger.info('Creando sopa')
    soup = BeautifulSoup(response.text, 'html.parser')
    logger.info('Obteniendo enlaces de anuncios')
    articles = list(soup.find_all('a', class_='d-flex flex-grow-1 my-2 card_np'))
    hrefs = list(map(lambda x: url_shows.format(x.attrs.get('href')), articles))
    # hrefs = []
    # for article in articles:
    #     hrefs.append(url_shows.format(article.attrs.get('href')))
    save_soup(soup,'databases/nuevapasion/{}'.format(i), str(i) + '.html')
    for href in hrefs:
        logger.info('Obteniendo anuncio {}'.format(href))
        show_id = href.split('/')[-1]
        if not os.path.exists('databases/nuevapasion/{}/{}'.format(i, show_id)):
            os.mkdir('databases/nuevapasion/{}/{}'.format(i, show_id))
        try:
            show_response = requests.get(href)
        except:
            try:
                time.sleep(1)
                show_response = requests.get(href)
            except:
                logger.info('Error en el anuncio {}'.format(href))
                csv = pd.read_csv('errores.csv')
                csv.loc[len[csv]] = [href]
                csv.to_csv('errores.csv', index=False)
        show_soup = BeautifulSoup(show_response.text, 'html.parser')
        save_soup(show_soup, 'databases/nuevapasion/{}/{}'.format(i, show_id), show_id + '.html')
        images = show_soup.select('.grouped_elements')
        logger.info('Obteniendo imagenes del anuncio')
        images_href = list(map(lambda x: url_shows.format(x.attrs.get('href')), images))

        for image in images_href:
            get_image_from_url(image, 'databases/nuevapasion/{}/{}'.format(i, show_id))
    