import requests, bs4
from datetime import datetime
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tkinter import ttk

url = 'https://www.mastersportal.com/search/#q=lv-master|tc-EUR&start='

# establish logging system
logging.basicConfig(filename= "logs\\"+datetime.now().strftime('%Y-%m-%d')+".txt", level=logging.INFO, format=' %(asctime)s - %(levelname)s- %(message)s')

logging.info('opening browser in background')
options = webdriver.ChromeOptions()
# options.add_argument('headless')
# #options.add_argument('user-data-dir=C:\\Users\\'+getpass.getuser()+'\\AppData\\Local\\Google\\Chrome\\User Data')
# options.add_argument('disable-gpu')
# options.add_argument('--disable-notifications')
# options.add_argument("--window-size=1920,1080")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument('disable-infobars')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-extensions')
# options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(executable_path='chromedriver\\chromedriver.exe',options= options)
driver.maximize_window()
logging.info('Browser is opened')


# Pop up configration
class endPopUp:
    def __init__(self, master, NoOfScholars):
        master.title('weMakeScholars')
        self.label = ttk.Label(master, text ="number of scraped shcolarships = "+str(NoOfScholars),width=50).pack()
        ttk.Button(master, text = 'OK',command = master.destroy).pack()


