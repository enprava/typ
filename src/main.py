from selenium.webdriver.common.by import By
from utils import *
import time

npaginas = range(1)

paginas = get_pages("https://www.destacamos.com/3-travestis/{}/listings.html",npaginas)
drivers = get_drivers(paginas)

nodes = get_nodes_from_driver(drivers,[By.CLASS_NAME,"titulo"])

nodes = list(map(lambda x: list(map(lambda y: apply_action(y, [By.TAG_NAME,"a"]), x)), nodes))
hrefs = list(map(lambda x: get_href_from_nodes(x), nodes))
shows = list(map(lambda x: get_drivers(x), hrefs))

