from selenium.webdriver.common.by import By
from utils import *



npaginas = range(1,3)

paginas = get_pages("https://www.destacamos.com/3-travestis/{}/listings.html",npaginas)
drivers = get_drivers(paginas)

nodes = get_nodes_from_driver(drivers,[By.CLASS_NAME,"titulo"])
for node in nodes:
    node = list(map(lambda x: apply_action(x, [By.TAG_NAME,"a"]),node))
    print(node)
    hrefs = get_href_from_nodes(node)
    print(hrefs)
