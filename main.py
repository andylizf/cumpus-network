import os
import time
import socket
from logging import *
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()
basicConfig(filename='info.log', level=INFO)

def login():
    while True:
        opts = ChromeOptions()
        opts.add_argument("--headless")
        driver = Chrome(options=opts, service=Service(ChromeDriverManager().install()))
        time.sleep(1)

        el = lambda id : driver.find_element(By.ID, id)
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
                    break
            except:
                el("username").clear()
                el("password").clear()
                el("username").send_keys(os.getenv("USERNAME"))
                el("password").send_keys(os.getenv("PASSWORD"))
                el("login-account").click()
                time.sleep(2)
                info("Bit-Web OK!")
                break
            
        except:
            warning("Bit-Web Failed!")
            driver.close()
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
    login()

