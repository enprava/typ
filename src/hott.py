import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
from utils import get_image_from_url
import os

import logging
import sys
fmt = '[%(asctime)-15s] [%(levelname)s] %(name)s: %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger('Hottescorts')

json_file = open("data/hott.json", "r", encoding="utf-8")
ciudades = json.load(json_file)
json_file.close()

base = "https://hottescorts.com/{}-{}"

descargados = pd.read_csv("data/descargados.csv")
for categoria in ["escorts", "travestis"]:
    for ciudad in ciudades:
        current = base.format(categoria, ciudad)
        response_list = requests.get(current)
        soup_list = BeautifulSoup(response_list.text, "html.parser")
        path = "databases/hottescorts/{}/lists/{}".format(categoria, ciudad)
        path_list = os.path.join(path, "list.html")
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path_list, "w", encoding="utf-8") as list_file:
            list_file.write(soup_list.prettify())
            list_file.close()

        galeria = soup_list.find("section", attrs={"class": "container-galeria"})
        hrefs = galeria.find_all("a")
        hrefs = list(map(lambda x: x.attrs.get("href"), hrefs))

        for href in hrefs:
            show_id = href.split(".com/")[-1]
            if (descargados['id']==show_id).any():
                continue
            show_true_id = show_id.split("/")[-1]
            path_show = "databases/hottescorts/{}/shows/{}".format(
                categoria, show_true_id
            )

            response_show = requests.get(href)
            soup_show = BeautifulSoup(response_show.text, "html.parser")
            if not os.path.exists(path_show):
                os.makedirs(path_show)
            with open(
                os.path.join(path_show, show_true_id + ".html"), "w", encoding="utf-8"
            ) as show_file:
                show_file.write(soup_show.prettify())
                descargados.loc[len(descargados)] = [show_id]
                descargados.to_csv('data/descargados.csv', index=False)
                show_file.close()
            images = soup_show.find(
                "div", attrs={"class": "contenidor-fotos-fitxa-desktop"}
            ).find_all("img")
            images = list(map(lambda x: x.attrs.get("src"), images))
            for image in images:
                get_image_from_url(image, path_show)
