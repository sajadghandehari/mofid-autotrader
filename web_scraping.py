from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import time

# Replace these with your login credentials
username = "09135292286"
password = "sA4420802286"

# Create a WebDriver instance
chrome_driver_path = "chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

# Open the website
driver.get("https://account.emofid.com/Login")
time.sleep(3)

username_field = driver.find_element(by=By.XPATH, value='//*[@id="Username"]')
username_field.send_keys(username)

password_field = driver.find_element(by=By.XPATH, value='//*[@id="Password"]')
password_field.send_keys(password)

password_field.send_keys(Keys.RETURN) 

time.sleep(5)


driver.quit()