import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from utils import get_image_from_url

import logging
import sys
fmt = '[%(asctime)-15s] [%(levelname)s] %(name)s: %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger('Emasex')

base_url = "https://emasex.com/"
pattern = r"^[a-zA-Z0-9_\-]+/[0-9]+$"
errores = pd.read_csv('data/errores.csv')

def get_anuncios(tags):
    return list(
        filter(
            lambda x: x is not None,
                map(
                    lambda x: x
                    if x.split("/")[-1].isdigit()
                    else None,
                    tags,
                ),
        )
    )


with open("data/emasex.txt", "r", encoding="utf-8") as file:
    urls = list(set(file.read().split("\n")))
    file.close()

for url in urls:
    trozos = url.split("/")
    provincia = trozos[-1]
    categoria = trozos[-2]

    logger.info('Extrayendo {} de {}'.format(categoria, provincia))

    path = "databases/emasex/{}/{}"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    a_tag = soup.find_all("a")
    try:
        anuncios = get_anuncios(list(map(lambda x: x.attrs.get("href"), a_tag)))
    except:
        try:
            anuncios = get_anuncios(list(map(lambda x: x.attrs.get("href"), a_tag)))
        except:
            errores.loc[len(errores)] = [url, 'lista']
            errores.to_csv('data/errores.csv', index=False)

    if not os.path.exists(path.format(categoria, provincia)):
        os.makedirs(path.format(categoria, provincia))
    logger.info('Guardando lista')
    with open(
        os.path.join(path.format(categoria, provincia), "list.html"),
        "w",
        encoding="utf-8",
    ) as soup_file:
        soup_file.write(soup.prettify())
        soup_file.close()

    for anuncio in anuncios:
        anuncio_id = anuncio.split("/")[-1]
        anuncio_path = os.path.join(path.format(categoria, provincia), anuncio_id)

        logger.info('Obteniendo anuncio con id {}'.format(anuncio_id))

        if not os.path.exists(anuncio_path):
            os.makedirs(anuncio_path)
        anuncio_soup = BeautifulSoup(requests.get(anuncio).text, "html.parser")
        logger.info('Guardando anuncio')
        with open(
            os.path.join(anuncio_path, str(anuncio_id) + ".html"), "w", encoding="utf-8"
        ) as anuncio_file:
            anuncio_file.write(anuncio_soup.prettify())

        divs = anuncio_soup.find('div', attrs={'class':'relative pb-96'})
        logger.info('Obteniendo imagenes del anuncio')
        try:
            imgs = list(map(lambda x: x.find('img').attrs.get("src"), divs))
            imgs.append(anuncio_soup.find('div', attrs={'id': 'foto'}).find('img').attrs.get('src'))
        except:
            try:
                imgs = list(map(lambda x: x.find('img').attrs.get("src"), divs))
                imgs.append(anuncio_soup.find('div', attrs={'id': 'foto'}).find('img').attrs.get('src'))
            except:
                errores.loc[len(errores)] = [url, 'imagenes']
                errores.to_csv('data/errores.csv', index=False)
            
        for x in imgs:
            get_image_from_url(x, anuncio_path)
