from selenium.webdriver.common.by import By
from utils import *
import time

npaginas = range(1,3)

paginas = get_pages("https://es-es.escort-advisor.com/escort/madrid/{}",npaginas)
print(paginas)
drivers = get_drivers(paginas)
print(drivers)
d_c = do_click_per_driver(drivers, [[By.CLASS_NAME, 'btn.btn-primary.btn-lg.cookie_disclaimer_button']])
print(d_c)
# nodes = get_nodes_from_driver(drivers,[By.CLASS_NAME,"serp_block_container"])

# nodes = list(map(lambda x: list(map(lambda y: apply_action(y, [By.TAG_NAME,"a"]), x)), nodes))
# nodes = drop_nones(nodes)
# print(nodes)
# hrefs = list(map(lambda x: get_href_from_nodes(x), nodes))
# shows = list(map(lambda x: get_drivers(x), hrefs))
# # print(shows)
