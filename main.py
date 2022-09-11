import socket
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ChromeOptions

from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

from logging import *

basicConfig(filename="info.log", level=INFO)
hostname = socket.gethostname()

login_config = config["login"]


def login():
    while True:
        opts = ChromeOptions()
        opts.add_argument("--headless")
        driver = Chrome(options=opts)
        sleep(1)

        el = lambda id: driver.find_element(By.ID, id)
        try:
            driver.get("https://go.ruc.edu.cn")
            sleep(1)

            # file = open("page_source.html", "w", encoding='utf-8')
            # file.write(driver.page_source)
            # file.close()

            try:
                if el("used-flow"):
                    info("Bit-Web still OK!")
                    driver.close()
                    break
            except:
                el("username").clear()
                el("password").clear()
                el("username").send_keys(login_config["username"])
                el("password").send_keys(login_config["password"])
                el("login-account").click()
                info("Bit-Web OK!")
                sleep(2)
                driver.close()
                break

        except:
            warning("Bit-Web Failed!")
            driver.close()
            continue


login()
