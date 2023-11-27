from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
from bs4 import BeautifulSoup
import os
from utils import *
import re

enlaces = {
    "AcompanantesMadrid": "/f4/",
    "CallejerasMadrid": "/f45/",
    "AgenciasMadrid": "/f40/",
    "ClubesMadrid": "/f5/",
    "Masde40Madrid": "/f6/",
    "ChicasVIPMadrid": "/f7/",
    "MasajesEroticosMadrid": "/f8/",
    "TravestisMadridyTransexuales": "/f13/",
    "SeXtremeMadrid": "/f87/",
    "FotosFalsasMadrid": "/f10/",
    "NuevosubforodeMasajistasyAcompanantes": "/f303/",
    "SUBFORODEINFORMACIONYOPINIONESDELACOMUNIDADVALENCIANAyMURCIA": "/f21/",
    "AcompanantesValencia": "/f29/",
    "AcompanantesAlicante": "/f48/",
    "AcompanantesMurcia": "/f47/",
    "AcompanantesCastellon": "/f49/",
    "TravestisValenciayTransexuales": "/f150/",
    "SUBFORODEINFORMACIONYOPINIONESDEEUSKADIYNAVARRA": "/f59/",
    "Acompanantesalava": "/f139/",
    "AcompanantesGuipuzcoa": "/f140/",
    "Vizcaya": "/f141/",
    "NuevosubforodeMasajistasyAcompanantesEuskadi": "/f304/",
    "AcompanantesNavarra": "/f219/",
    "FotosfalsasEuskadiyNavarra": "/f220/",
    "SUBFORODEINFORMACIONYOPINIONESDEGALICIA": "/f57/",
    "ACoruna": "/f144/",
    "AcompanantesLugo": "/f145/",
    "AcompanantesOurense": "/f146/",
    "AcompanantesPontevedra": "/f147/",
    "SUBFORODEINFORMACIONYOPINIONESDEARAGON": "/f19/",
    "Zaragoza": "/f28/",
    "AcompanantesTeruel": "/f123/",
    "AcompanantesHuesca": "/f122/",
    "SUBFORODEINFORMACIONYOPINIONESDEANDALUCiA": "/f18/",
    "Sevilla": "/f26/",
    "AcompanantesCordoba": "/f66/",
    "AcompanantesCadiz": "/f67/",
    "AcompanantesGranada": "/f64/",
    "AcompanantesHuelva": "/f68/",
    "AcompanantesJaen": "/f65/",
    "AcompanantesMalaga": "/f63/",
    "TravestisAndaluciayTransexuales": "/f149/",
    "AcompanantesAlmeria": "/f69/",
    "SUBFORODEINFORMACIONYOPINIONESDECASTILLA-LEON": "/f54/",
    "AcompanantesAvila": "/f131/",
    "AcompanantesBurgos": "/f132/",
    "AcompanantesLeon": "/f133/",
    "AcompanantesPalencia": "/f134/",
    "AcompanantesSalamanca": "/f135/",
    "AcompanantesSegovia": "/f136/",
    "AcompanantesSoria": "/f137/",
    "AcompanantesValladolid": "/f27/",
    "AcompanantesZamora": "/f138/",
    "SUBFORODEINFORMACIONDECASTILLALAMANCHA": "/f23/",
    "AcompanantesAlbacete": "/f126/",
    "AcompanantesCiudadReal": "/f127/",
    "AcompanantesCuenca": "/f128/",
    "AcompanantesGuadalajara": "/f129/",
    "AcompanantesToledo": "/f130/",
    "SUBFORODEINFORMACIONYOPINIONESDEEXTREMADURA": "/f55/",
    "AcompanantesBadajoz": "/f142/",
    "AcompanantesCaceres": "/f143/",
    "SUBFORODEINFORMACIONYOPINIONES:MASAUTONOMIAS": "/f24/",
    "AcompanantesAsturias": "/f20/",
    "AcompanantesBaleares": "/f53/",
    "AcompanantesCanarias": "/f60/",
    "AcompanantesCantabria": "/f56/",
    "AcompanantesCeuta": "/f61/",
    "AcompanantesLaRioja": "/f22/",
    "AcompanantesMelilla": "/f62/",
    "SUBFORODEINFORMACIONYOPINIONESDECATALUnA": "/f70/",
    "AcompanantesBarcelona": "/f72/",
    "PisosyAgenciasBarcelona": "/f73/",
    "ClubesBarcelona": "/f74/",
    "AcompanantesdelujoBarcelonayChicasVip": "/f75/",
    "AcompanantesGirona": "/f50/",
    "AcompanantesLleida": "/f51/",
    "AcompanantesTarragona": "/f52/",
    "FotosfalsasdeCataluna": "/f236/",
    "SUBFORODEINFORMACIONYOPINIONESDEELMUNDO": "/f71/",
    "TVMundo": "/f151/",
    "AcompanantesAmerica": "/f81/",
    "AcompanantesAfrica": "/f82/",
    "AcompanantesAsia": "/f83/",
    "AcompanantesEuropa": "/f84/",
    "AcompanantesOceania": "/f85/",
    "SUBFOROGENERALWWW.SPALUMI.COM": "/f3/",
    "TODOSOBRESPALUMI": "/f16/",
    "TemasGeneralesTodaslascomunidades": "/f15/",
    "ConsultaMedicaTodaslascomunidades": "/f9/",
}
enlace_base = "https://spalumi.com"
dir = 'databases/spalumi'

for name, url in enlaces.items():
    print('Extrayendo {}'.format(name))
    driver = webdriver.Firefox()
    forum_id = url.replace('/', '').replace('f', '')
    driver.get(enlace_base)
    driver.find_element(By.ID, 'navbar_username').send_keys('kanali')
    driver.find_element(By.ID, 'navbar_password').send_keys('indexa1234')
    driver.find_element(By.CLASS_NAME, 'button').click()
    time.sleep(10)
    driver.get(f'{enlace_base}{url}')
    table = driver.find_elements(By.CLASS_NAME,'tborder')[5]
    for td in table.find_elements(By.TAG_NAME, 'td'):
        if td.get_attribute('nowrap') is not None:
            ultima = td.find_element(By.TAG_NAME, 'a').get_attribute('href')
            ultima = ultima.split('/')[-1]
            ultima = ultima.removeprefix('index').removesuffix('.html')

    path = os.path.join(dir, url[1:])
    print(path)
    if not os.path.exists(path):
        os.makedirs(path)
    current_path = os.path.join(path, '1')
    if not os.path.exists(current_path):
        os.makedirs(current_path)

    with open(os.path.join(current_path, 'list.html',), 'w', encoding='utf-8') as file:
        print(os.path.join(current_path, 'list.html',))
        file.write(driver.page_source)
        file.close()
    download(driver, f'{enlace_base}{url}', forum_id, current_path)
    for i in range(2, int(ultima)+1):
        print('Extrayendo pagina {} de {}'.format(i, ultima))
        current_path = os.path.join(path, str(i))
        download(driver, f'{enlace_base}{url}index{i}.html', forum_id, current_path)
    driver.close()