import os
import time
import random
import socket
from dotenv import load_dotenv
from logging import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()
basicConfig(filename='info.log', encoding='utf-8', level=INFO)

def login(usrname,passwd):
    while(1):
        opts = ChromeOptions()
        opts.add_argument("--headless")
        driver = webdriver.Chrome(options=opts, service=Service(ChromeDriverManager().install()))
        el = lambda id : driver.find_element(By.ID, id)

        time.sleep(1)
        try:
            driver.get('https://go.ruc.edu.cn')
            time.sleep(1)

            # file = open("page_source.html", "w", encoding='utf-8')
            # file.write(driver.page_source)
            # file.close()

            try: 
                if el("realname"):
                    info("Bit-Web still OK!")
                    driver.close()
                    time.sleep(random.randint(3,7))
                    break
            except:
                el("username").clear()
                el("password").clear()
                el("username").send_keys(usrname)
                el("password").send_keys(passwd)
                el("login-account").click()
                time.sleep(2)
                info("Bit-Web OK!")
                break
            
        except:
            driver.close()
            warning("Bit-Web Failed!")
            continue

def get_host_ip():
    global _local_ip
    s = None
    try:
        if not _local_ip:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            _local_ip = s.getsockname()[0]
        return _local_ip
    finally:
        if s:
            s.close()


if __name__ == '__main__':
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    login(username, password)
