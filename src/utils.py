from selenium import webdriver
from selenium.webdriver.firefox.options import Options
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
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    return driver


def get_drivers(paginas):
    return np.vectorize(init_driver)(paginas)


def get_html_from_url(pagina):
    response = requests.get(pagina, timeout=5)
    response.raise_for_status()
    html_content = response.text
    return html_content


def get_html_from_urls(paginas):
    return np.vectorize(get_html_from_url)(paginas)


def get_nodes_from_driver(drivers, action):
    return np.vectorize(lambda x: x.find_elements(action[0], action[1]))(drivers)


def get_nodes_from_htmls(htmls):
    return [BeautifulSoup(html, "html.parser") for html in htmls]


def close_drivers(drivers):
    np.vectorize(lambda x: x.close())(drivers)


def get_href_nodes_from_nodes(nodes):
    return np.apply_along_axis(get_href_from_nodes, axis=1, arr=nodes)


def get_href_from_nodes(nodes):
    return list(map(lambda x: x.get_attribute("href"), nodes))


def write_html(row):
    # print(row)
    node = row[0]
    path = row[1]
    file_name = row[2]
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, file_name), "w", encoding="utf-8") as file:
        file.write(node)


def download_images_from_rows(htmls, paths):
    array_zip = np.stack((htmls, paths), axis=-1)
    np.apply_along_axis(get_imgs_from_node_bs4, axis=1, arr=array_zip)


def serialize_nodes_html(nodes, num_pag, common_path, files_name):
    nodes_write_path = np.vectorize(lambda x: common_path.format(x))(num_pag)

    array_zip = np.stack((nodes, nodes_write_path, files_name), axis=-1)
    np.apply_along_axis(write_html, axis=1, arr=array_zip)
    return nodes_write_path


def get_imgs_from_node(row):
    node = BeautifulSoup(row[0], "html.parser")
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
    return [x.find("a")["href"] for x in nodes]


def apply_action_to_bs4_nodes(nodes, actions):
    return [x.find_all(actions[0], actions[1]) for x in nodes]


def get_imgs_from_node_bs4(row):
    node = BeautifulSoup(row[0], "html.parser")
    pag_path = row[1]
    if not os.path.exists(os.path.join(pag_path, "imagenes")):
        os.makedirs(os.path.join(pag_path, "imagenes"))

    img_tags = node.find_all("img")
    img_tags = [
        img_tag
        for img_tag in img_tags
        if os.path.basename(img_tag.get("src"))[0].isdigit()
    ]
    if len(img_tags) > 5:
        img_tags = img_tags[:6]
    for img_tag in img_tags:
        img_url = img_tag.get("src")
        if img_url:
            img_name = os.path.join(pag_path, "imagenes", os.path.basename(img_url))

            try:
                response = requests.get(img_url, timeout=5)
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
    return np.vectorize(lambda x: do_click(x, actions))(drivers)


def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")


def drop_nones(nodes):
    return nodes[nodes != None]


def download_images(srcs, path):
    for i in range(len(srcs)):
        try:
            response = requests.get(srcs[i])
        except:
            continue
        extension = srcs[i].split(".")[-1]
        if '/' in extension:
            extension = extension[:extension.find('/')]
        with open(os.path.join(path, str(i) + "." + extension), "wb") as file:
            file.write(response.content)
            file.close()


def download(driver, forum_id, path):
    tbody_id = f"threadbits_forum_{forum_id}"
    aes = driver.find_element(By.ID, tbody_id).find_elements(By.TAG_NAME, "a")
    enlaces = {}
    for a_tag in aes:
        try:
            a = a_tag.get_attribute('href')
            b = a_tag.get_attribute("id").split("_")[-1]
            enlaces[b] = a
        except Exception:
            continue
    for anuncio_id, a in enlaces.items():
        print("Descargando anuncio con id {}".format(anuncio_id))
        driver.get(a)
        try:
            text = driver.find_element(By.TAG_NAME, 'body').text
            index = text.find('Página')
            aux = text[index:index+14][-2:]
            paginas = int(aux)
        except:
            paginas = 1
        current_path = os.path.join(path, anuncio_id)
        if not os.path.exists(current_path):
            os.makedirs(current_path)
        else: 
            continue
        i = 1
        imgs = driver.find_elements(By.TAG_NAME, "img")

        fotos = list(
            filter(
                lambda y: "postimg" in y, map(lambda x: x.get_attribute("src"), imgs)
            )
        )
        # print("Descargando fotos")
        img_path = os.path.join(current_path, "imagenes")
        if not os.path.exists(img_path):
            os.makedirs(img_path)
        download_images(fotos, img_path)
        # print("Descargando paginas")
        enlace = driver.current_url[:driver.current_url.find('.html')]
        enlace = enlace + '/index{}/html'
        with open(
                os.path.join(current_path, "1.html"), "w", encoding="utf-8"
            ) as file:
                file.write(driver.page_source)
                file.close()
        for i in range(2,paginas+1):
            current_enlace = enlace.format(i)
            print('Descargando pagina {}'.format(i))
            driver.get(current_enlace)
            with open(
                os.path.join(current_path, str(i) + ".html"), "w", encoding="utf-8"
            ) as file:
                file.write(driver.page_source)
                file.close()
