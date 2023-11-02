from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
import requests
from selenium.webdriver.common.by import By
import pickle
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import numpy as np
import logging

logging.basicConfig(filename='errores.log', level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def apply_action(driver, action):
    try:
        return driver.find_element(action[0], action[1])
    except NoSuchElementException:
        return None


def apply_actions(driver, actions):
    for action in actions:
        driver = apply_action(driver, action)
    return driver


def get_pages(url, n_pages):
    return np.frompyfunc(lambda x: url.format(x),1,1)(n_pages)
    # return np.frompyfunc(url.format, 1, 1)(np.array(n_pages))


def init_driver(url):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    return driver


def get_drivers(paginas):
    return np.vectorize(init_driver)(paginas)


def get_html_from_url(pagina):


    try:
        custom_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Languague': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Upgrade-Insecure-Requests' : '1'

        }
        response = requests.get(pagina,headers=custom_headers,timeout=15)
        response.raise_for_status()
        html_content = response.text
        return html_content
    except:
        logging.error(pagina)
        return None
def get_html_from_urls(paginas):
    return np.frompyfunc(get_html_from_url,1,1)(paginas)

def get_nodes_from_driver(drivers, action):
    return np.vectorize(lambda x: x.find_elements(action[0],action[1]))(drivers)

def get_nodes_from_htmls(htmls):

    return [BeautifulSoup(html, "html.parser") for html in htmls]
def close_drivers(drivers):
    np.vectorize(lambda x: x.close())(drivers)
def get_href_nodes_from_nodes(nodes):
    return np.apply_along_axis(get_href_from_nodes,axis=1,arr=nodes)
def get_href_from_nodes(nodes):
    return list(map(lambda x: x.get_attribute("href"), nodes))

def write_html(row):
    # print(row)
    node = row[0]
    path = row[1]
    file_name = row[2]
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path,file_name),'w',encoding='utf-8') as file:
        file.write(node)



def download_images_from_rows(htmls,paths):
    array_zip = np.stack((htmls, paths), axis=-1)
    np.apply_along_axis(get_imgs_from_node_bs4,axis=1,arr=array_zip)
def serialize_nodes_html(nodes,num_pag, common_path, files_name):
    nodes_write_path = np.frompyfunc(lambda x: common_path.format(x),1,1)(num_pag)

    array_zip = np.stack((nodes,nodes_write_path,files_name), axis=-1)
    np.apply_along_axis(write_html, axis=1, arr=array_zip)
    return nodes_write_path

def get_imgs_from_node(row):
    node = BeautifulSoup(row[0],"html.parser")
    pag_path = row[1]
    if not os.path.exists(os.path.join(pag_path, "imagenes")):
        os.makedirs(os.path.join(pag_path, "imagenes"))

    img_tags = node.find_elements(By.TAG_NAME, "img")
    for img_tag in img_tags:
        img_url = img_tag.get_attribute("src")

        img_name = os.path.join(pag_path, "imagenes", os.path.basename(img_url))

        try:
            response = requests.get(img_url)
            if response.status_code == 200:
                with open(img_name, "wb") as img_file:
                    img_file.write(response.content)

        except:
            print("Error al descargar la imagen")




def get_ahref_node_from_bs4_nodes(nodes):
    return [x.find("a")['href'] for x in nodes]
def apply_action_to_bs4_nodes(nodes,actions):


    return [x.find_all(actions[0],actions[1]) for x in nodes]
def get_imgs_from_node_bs4(row):
    node = BeautifulSoup(row[0], "html.parser")
    pag_path = row[1]
    if not os.path.exists(os.path.join(pag_path, "imagenes")):
        os.makedirs(os.path.join(pag_path, "imagenes"))

    img_tags = node.find_all('img')
    img_tags = [img_tag for img_tag in img_tags if os.path.basename(img_tag.get("src"))[0].isdigit()]
    if len(img_tags)>5:
        img_tags = img_tags[:6]
    for img_tag in img_tags:
        img_url = img_tag.get("src")
        if img_url:
            path_name = os.path.basename(img_url)
            if "?" in os.path.basename(img_url):
                path_name = path_name.split('?')[0]
            img_name = os.path.join(pag_path, "imagenes", path_name)

            try:
                response = requests.get(img_url,timeout=5)
                if response.status_code == 200:
                    with open(img_name, "wb") as img_file:
                        img_file.write(response.content)
            except requests.exceptions.RequestException as e:
                print(f"Error al descargar la imagen: {e}")
        else:
            print("La URL de la imagen es nula o no válida")


def save_node(node, path, file_name):
    with open(os.path.join(path, file_name), "wb") as file:
        file.write(node.page_source)


def deserialize_pickle_node(path):
    with open(path, "rb") as archivo:
        html_content = pickle.load(archivo)
        soup = BeautifulSoup(html_content, "html.parser")
        return soup


def do_click(driver, actions):
    apply_actions(driver, actions).click()


def do_click_per_driver(drivers, actions):

    return np.vectorize(lambda x: do_click(x,actions))(drivers)


def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")


def drop_nones(nodes):
    return nodes[nodes != None]
