from utils import *
import time
with open('urls/escortadvisor.txt', 'r', encoding='utf-8') as f:
    urls = f.read()
    urls = urls.split('\n')
    urls = [url + '{}' for url in urls]

n_pages = range(1,3)

for url in urls:
    categoria = url.split('/')[-2]
    paginas = get_pages(url, n_pages)
    drivers = get_drivers(paginas)
    do_click_per_driver(drivers, [[By.CSS_SELECTOR, '.cookie_disclaimer_button']])
    save_node(drivers, f'databases/escort-advisor/lists/{categoria}')
    nodes = get_nodes_from_driver(drivers,[By.CLASS_NAME,"serp_block_container"])
    nodes = list(map(lambda x: list(map(lambda y: apply_action(y, [By.TAG_NAME,"a"]), x)), nodes))
    for node in nodes:
        del node[0]
    hrefs = list(map(lambda x: get_href_from_nodes(x), nodes))
    shows = list(map(lambda x: get_drivers(x), hrefs))
    
    break