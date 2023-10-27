from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import requests
from selenium.webdriver.common.by import By
import pickle
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import numpy as np

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
    return np.vectorize(lambda x: url.format(x))(n_pages)
    # return np.frompyfunc(url.format, 1, 1)(np.array(n_pages))


def init_driver(url):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.ChromiumEdge(options=options)
    driver.get(url)
    return driver


def get_drivers(paginas):
    return np.vectorize(init_driver)(paginas)


def get_nodes_from_driver(drivers, action):
    return np.vectorize(lambda x: x.find_elements(action[0],action[1]))(drivers)

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
        file.write(node.page_source)




def serialize_nodes_html(nodes,num_pag, common_path, files_name):
    nodes_write_path = np.vectorize(lambda x: common_path.format(x))(num_pag)

    array_zip = np.stack((nodes,nodes_write_path,files_name), axis=-1)

    return np.apply_along_axis(write_html,axis=1,arr=array_zip)

def get_imgs_from_node(node, pag_path):
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


import os


def get_imgs_from_node_bs4(node, pag_path):
    if not os.path.exists(os.path.join(pag_path, "imagenes")):
        os.makedirs(os.path.join(pag_path, "imagenes"))

    img_tags = node.find_all('img')
    img_tags = [img_tag for img_tag in img_tags if os.path.basename(img_tag.get("src"))[0].isdigit()]
    if len(img_tags)>5:
        img_tags = img_tags[:6]
    for img_tag in img_tags:
        img_url = img_tag.get("src")
        if img_url:
            img_name = os.path.join(pag_path, "imagenes", os.path.basename(img_url))

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
