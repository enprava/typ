from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
import requests
from selenium.webdriver.common.by import By
import pickle
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import numpy as np
import math


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
    # options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    return driver


def get_drivers(paginas):
    # return np.vectorize(init_driver)(paginas)
    return np.frompyfunc(init_driver, 1, 1)(paginas)


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
    np.frompyfunc(lambda x: x.close(), 1, 1)(drivers)


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


def get_imgs_from_node(node, path):
    if not os.path.exists(os.path.join(path, "imagenes")):
        os.makedirs(os.path.join(path, "imagenes"))

    img_tags = node.find_elements(By.TAG_NAME, "img")
    for img_tag in img_tags:
        img_url = img_tag.get_attribute("src")

        img_name = os.path.join(path, "imagenes", os.path.basename(img_url))

        try:
            response = requests.get(img_url)
            if response.status_code == 200:
                with open(img_name, "wb") as img_file:
                    img_file.write(response.content)

        except:
            # print("Error al descargar la imagen {}".format(img_url))
            continue


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
                # print(f"Error al descargar la imagen: {e}")
                continue
        else:
            print("La URL de la imagen es nula o no válida")


def save_drivers(drivers, path):
    if not os.path.exists(path):
        os.makedirs(path)


def save_node(node, path, file_name):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, file_name), "w", encoding="utf-8") as file:
        file.write(node.page_source)


def save_soup(soup, path, file_name):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, file_name), "w", encoding="utf-8") as file:
        file.write(soup.prettify())
        file.close()


def save_pages(drivers, path):
    if not os.path.exists(path):
        os.makedirs(path)
    for i in range(len(drivers)):
        save_node(drivers[i], path, str(pags[i]) + ".html")


def deserialize_pickle_node(path):
    with open(path, "rb") as archivo:
        html_content = pickle.load(archivo)
        soup = BeautifulSoup(html_content, "html.parser")
        return soup


def do_click(driver, actions):
    apply_actions(driver, actions).click()


def do_click_per_driver(drivers, actions):
    return np.frompyfunc(lambda x: do_click(x, actions), 1, 1)(drivers)


def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")


def drop_nones(nodes):
    return nodes[nodes != None]


def download_images(soup, path):
    imgs = soup.find("div", attrs={"class": "col-xs-12 col-md-6 colonna-r"}).find_all(
        "img"
    )
    srcs = list(map(lambda x: x.attrs.get("src"), imgs))
    for i in range(len(srcs)):
        response = requests.get(srcs[i])
        extension = srcs[i].split(".")[-1]
        with open(os.path.join(path, str(i) + "." + extension), "wb") as file:
            file.write(response.content)
            file.close()


def download(hrefs, path):
    if not os.path.exists(path):
        os.makedirs(path)
    for href in hrefs:
        response = requests.get(href)
        soup = BeautifulSoup(response.text, "html.parser")
        anuncio_id = href.split("/")[-1]
        print("Descargando {}".format(anuncio_id))
        custom_path = os.path.join(path, anuncio_id)
        if not os.path.exists(custom_path):
            os.makedirs(custom_path)

        save_soup(soup, custom_path, anuncio_id + ".html")
        download_images(soup, custom_path)


def get_array_1_len(number):
    arrays = []
    for i in range(1, number + 1, 1):
        arrays.append(list(range(i, i + 5)))

    def remove_index(arr, number):
        if arr[-1] > number:
            del arr[-1]
            remove_index(arr, number)

    remove_index(arrays[-1], number)
    return arrays
