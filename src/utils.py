from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import requests
from selenium.webdriver.common.by import By
import pickle
# # from selenium.webdriver.common.by import By

def apply_action(driver, action):
    return driver.find_element(action[0], action[1])

def apply_actions(driver, actions):
    for action in actions:
        driver = apply_action(driver, action)
    return driver

def get_pages(url,n_pages):
    return list(map(lambda x: url.format(x), n_pages))

def init_driver(url):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    return driver
def get_drivers(paginas):

    return list(map(lambda x: init_driver(x), paginas))

def get_nodes_from_driver(drivers,action):
    return list(map(lambda x: x.find_elements(action[0],action[1]),drivers))
def get_href_from_nodes(nodes):

    return list(map(lambda x: x.get_attribute("href"), nodes))

def get_imgs_from_node(node,pag_path):

    if not os.path.exists(os.path.join(pag_path, "imagenes")):
        os.makedirs(os.path.join(pag_path, "imagenes"))

    img_tags = node.find_elements(By.TAG_NAME, "img")
    for img_tag in img_tags:
        img_url = img_tag.get_attribute("src")

        img_name = os.path.join(pag_path, "imagenes", os.path.basename(img_url))

        try:
            response = requests.get(img_url)
            if response.status_code == 200:
                with open(img_name, 'wb') as img_file:
                    img_file.write(response.content)

        except:
            print("Error al descargar la imagen")


def serialize_pickle_node(node,path,file_name):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, file_name), 'wb') as pickle_file:
        pickle.dump(node.page_source, pickle_file)

# def deserialize_pickle_node(path):
#     with open(path, 'rb') as archivo:
#         html_content = pickle.load(archivo)
#
#         soup = BeautifulSoup(html_content, 'html.parser')
#         return soup

