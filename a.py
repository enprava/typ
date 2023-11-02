from seleniumwire import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import requests
import yaml
import math


def get_driver():
    options = Options()
    options.headless = False
    driver = webdriver.Firefox(options=options)
    driver.get("https://es-es.escort-advisor.com/escort")
    driver.find_element(
        By.CLASS_NAME, "btn.btn-primary.btn-lg.cookie_disclaimer_button"
    ).click()
    return driver


def get_enlaces(url):
    enlaces = []
    driver = get_driver()
    driver.get(url)
    city_grid = driver.find_element(By.CLASS_NAME, "city_grid")
    city_items = city_grid.find_elements(By.CLASS_NAME, "city_grid_item")
    for item in city_items:
        cidudades = item.find_element(By.TAG_NAME, "ul").find_elements(
            By.TAG_NAME, "li"
        )
        for ciudad in cidudades:
            href = ciudad.find_element(By.TAG_NAME, "a").get_attribute("href")
            enlaces.append(href)
    file = open("enlaces.yaml", "w", encoding="utf-8")
    yaml.safe_dump(enlaces, file)
    file.close()
    driver.close()


def get_opinion_hrefs(path):
    hrefs = []
    file = open(path, "r", encoding="utf-8")
    enlaces = yaml.safe_load(file)
    file.close()
    driver = get_driver()
    for enlace in enlaces:
        i = 0
        driver.get(enlace)
        n_escorts = int(driver.find_element(By.CLASS_NAME, "page_subtitle").find_element(By.TAG_NAME, "strong").text)
        paginas = math.ceil(n_escorts/20)
        for i in range(paginas):
            driver.get(f'{enlace}/{i}')
            escorts = driver.find_elements(By.CLASS_NAME, 'serp_block_container')
            for escort in escorts:
                premium_id = escort.find_element(By.CLASS_NAME, 'serp_block_image').get_attribute('data-number')
                if premium_id is not None and premium_id != '':
                    continue
                opinion_href = escort.find_element(By.CLASS_NAME, 'serp_block_image').find_element(By.TAG_NAME, 'a').get_attribute('href')
                hrefs.append(opinion_href)
    file = open("opiniones.yaml", "w", encoding="utf-8")
    yaml.safe_dump(hrefs, file)
    file.close()
    driver.close()



# get_enlaces('https://es-es.escort-advisor.com/escort')
get_opinion_hrefs("enlaces.yaml")
