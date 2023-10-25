from selenium import webdriver
from selenium.webdriver.common.by import By
from utils import *

driver = webdriver.Firefox()
driver.get('http://trackwine.indexageodata.com/')
acciones = [[By.CLASS_NAME, 'welcome']]
print(apply_actions(driver, acciones))
driver.close()
