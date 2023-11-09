from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
import json

driver = webdriver.Firefox()
driver.get("https://hottescorts.com/")
driver.find_element(By.ID, "acceptCookie").click()
keys = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]
lista = []
for key in keys:
    driver.find_element(By.ID, "cerca_poblacio").send_keys(Keys.BACKSPACE)
    driver.find_element(By.ID, "cerca_poblacio").send_keys(key)
    time.sleep(2)
    enlaces = driver.find_element(By.ID, "camps-suggerits").find_elements(
        By.TAG_NAME, "a"
    )
    for enlace in enlaces:
        lista.append(enlace.get_attribute('data2'))


file = open('data/hott.json', 'w', encoding='utf-8')
json.dump(lista, file)
file.close()