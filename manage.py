import sys
import time
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime
from PyQt5.QtWidgets import *
from selenium import webdriver
from PyQt5.uic import loadUiType
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC


login, _ = loadUiType('fornt/login_page.ui')
ui, _ = loadUiType('fornt/main_page.ui')


class Login(QMainWindow, login):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.setWindowTitle("Login page")
        self.setWindowIcon(QIcon('python.png'))

        self.Handel_Buttons()

    def handel_login(self):

        try:
            username = self.username.text()
            password = self.password.text()
        except:
            print(self.username)

        if username !='' and password !='':
            self.login(username, password)
        else:
            self.meesage_error((183, 4, 4), "Your Username or password must be not empty !")

    def Handel_Buttons(self):

        self.LoginpageButton.clicked.connect(self.handel_login)

    def login(self, username, password):
        self.window = MainApp(username, password)
        self.hide()
        self.window.setFixedSize(600, 306)
        self.window.show()
        app.exec_()

    def meesage_error(self, color, message):

        palette = self.statusBar().palette()
        palette.setColor(self.statusBar().foregroundRole(),
                         QColor(*color))
        self.statusBar().setPalette(palette)
        self.statusBar().showMessage(message)


class MainApp(QMainWindow, ui):

    def __init__(self, username, password):
        self.username = username 
        self.password = password

        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("App")
        self.setWindowIcon(QIcon('python.png'))
        self.Handel_Buttons()

    def Handel_Buttons(self):

        self.StartButton.clicked.connect(self.web_scraping)

    def web_scraping(self):

        stock_name = self.stock_name.text()
        stock_num = self.stock_num.text()

        selected_time = self.timeEdit.time().toString("hh:mm:ss")
        print(f'Selected time: {selected_time}')

        chrome_driver_path = "chromedriver.exe"
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

        # Open the website
        driver.get("https://account.emofid.com/Login")
        time.sleep(3)

        username_field = driver.find_element(by=By.XPATH, value='//*[@id="Username"]')
        username_field.send_keys(self.username)

        password_field = driver.find_element(by=By.XPATH, value='//*[@id="Password"]')
        password_field.send_keys(self.password)
        time.sleep(3)
        password_field.send_keys(Keys.RETURN) 

        login_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/a[1]'))
        )        
        login_field.send_keys(Keys.RETURN)

        search_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/main/div[2]/div[1]/ul[1]/li[2]/span/i'))
        )       
        search_field.click()
        time.sleep(4)
        stock_field = driver.find_element(by=By.XPATH, value='//*[@id="searchInputControl"]')
        stock_field.send_keys(stock_name)

        select_stock_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="0"]/div[1]/div/div'))
                )        
        select_stock_field.click()

        while True:  
            time.sleep(1)
            current_time = datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S")
            print("Current time :", formatted_time)

            if formatted_time == selected_time:
                for i in range(15):
                    
                    buy_expath = '//*[@id="root"]/main/div[3]/div/div/as-split/as-split-area/app-layout-selector/app-layout1/div/div/as-split/as-split-area[2]/as-split/as-split-area[1]/div[1]/button[1]'
                    find_buy_element = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, buy_expath))
                            )        
                    find_buy_element.click()
                    time.sleep(0.2)
                    buy = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/main/div[3]/d-order-list/div/div[3]/order-form/div/div/form/div[3]/button[1]/span'))
                            )        
                    buy.click()
                break

        time.sleep(3)
        driver.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Login()
    window.setFixedSize(600, 300)
    window.show()
    app.exec_()
