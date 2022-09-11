import socket
import datetime
from time import sleep
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ChromeOptions

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from os import getenv, popen
from dotenv import load_dotenv

load_dotenv()

from logging import *

basicConfig(filename="info.log", level=INFO)
hostname = socket.gethostname()


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
                el("username").send_keys(getenv("USERNAME"))
                el("password").send_keys(getenv("PASSWORD"))
                el("login-account").click()
                info("Bit-Web OK!")
                sleep(2)
                driver.close()
                break

        except:
            warning("Bit-Web Failed!")
            driver.close()
            continue


def send(content):
    address = getenv("EMAIL")

    message = MIMEMultipart("mixed")
    message["From"] = message["To"] = address
    message["Subject"] = hostname + "的 IPv4 地址已更新"
    message.attach(MIMEText(content, "plain"))

    with smtplib.SMTP_SSL(getenv("SERVER")) as server:
        server.login(address, getenv("CODE"))
        server.sendmail(address, address, message.as_string())


login()
ip = [a for a in popen("route print").readlines() if " 0.0.0.0 " in a][0].split()[-2]

current = Path("current")
old_ip = current.read_text() if current.exists() else current.touch()

info("old_ip:" + old_ip)
info("ip:" + ip)
if old_ip == ip:
    info("本机的 IPv4 地址仍为" + ip)
else:
    if old_ip != None:
        open("history", "a").write(old_ip)
    current.write_text(ip)

    content = f"更新至 {ip} \n于{datetime.datetime.now()}"
    info(content)
    send(content)
