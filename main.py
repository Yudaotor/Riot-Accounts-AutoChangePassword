import argparse
import logging
import sys
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium import webdriver
import time
from Config import Config
from Logger import Logger


# coding:utf-8


def changePwd(log: logging.Logger, config: Config, username, password, newPassword):
    global driver
    try:
        o = Options()
        o.add_experimental_option('excludeSwitches', ['enable-logging'])
        s = Service(config.msedgedriverPath)
        driver = webdriver.Edge(service=s, options=o)
        driver.get(
            'https://auth.riotgames.com/login#acr_values=urn%3Ariot%3Agold&client_id=accountodactyl-prod&redirect_uri'
            '=https%3A%2F%2Faccount.riotgames.com%2Foauth2%2Flog-in&response_type=code&scope=openid%20email%20profile'
            '%20riot%3A%2F%2Friot.atlas%2Faccounts.edit%20riot%3A%2F%2Friot.atlas%2Faccounts%2Fpassword.edit%20riot'
            '%3A%2F%2Friot.atlas%2Faccounts%2Femail.edit%20riot%3A%2F%2Friot.atlas%2Faccounts.auth%20riot%3A%2F'
            '%2Fthird_party.revoke%20riot%3A%2F%2Fthird_party.query%20riot%3A%2F%2Fforgetme%2Fnotify.write%20riot%3A'
            '%2F%2Friot.authenticator%2Fauth.code%20riot%3A%2F%2Friot.authenticator%2Fauthz.edit%20riot%3A%2F%2Frso'
            '%2Fmfa%2Fdevice.write%20riot%3A%2F%2Friot.authenticator%2Fidentity.add&state=547c8cd2-9eb0-4302-b9b2'
            '-f29ee843a4bd&ui_locales=zh-Hans')
        driver.implicitly_wait(10)  # 隐式等待时间
        driver.maximize_window()
        # login
        driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div/div[2]/div/div/div[2]/div/div/div/div[1]/div/input').send_keys(username)
        driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div/div[2]/div/div/div[2]/div/div/div/div[2]/div/input').send_keys(password)

        buttonLogin = driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div/div[2]/div/div/button')
        time.sleep(2)
        driver.execute_script("arguments[0].click();", buttonLogin)
        # change password
        driver.find_element(by=By.XPATH, value='//*[@id="riot-account"]/div/div[2]/div/div[2]/div[1]/div/div/input').send_keys(password)
        driver.find_element(by=By.XPATH, value='//*[@id="riot-account"]/div/div[2]/div/div[2]/div[3]/div/input').send_keys(newPassword)
        driver.find_element(by=By.XPATH, value='//*[@id="riot-account"]/div/div[2]/div/div[2]/div[2]/div/input').send_keys(newPassword)
        driver.find_element(by=By.XPATH, value='//*[@id="riot-account"]/div/div[1]/p').click()
        driver.find_element(by=By.XPATH, value='//*[@id="riot-account"]/div/div[2]/div/div[3]/button[2]').click()
        log.info(username + " Success")
        print(username + " Success")
        time.sleep(3)
    except Exception as e:
        log.error(username + " Fail")
        print(username + " Fail")
    finally:
        driver.quit()


def init() -> tuple[logging.Logger, Config]:
    parser = argparse.ArgumentParser(description='英雄联盟外服自动改密码')
    parser.add_argument('-c', '--config', dest="configPath", default="./config.yaml", help='Path to a custom config file')
    args = parser.parse_args()
    Path("./logs/").mkdir(parents=True, exist_ok=True)
    log = Logger.createLogger()
    config = Config(log, args.configPath)
    return log, config


def main(log: logging.Logger, config: Config):
    print("程序启动")
    try:
        with open(config.accountFilePath) as f:
            line = f.readline()
            while line:
                sp = line.split('----')
                if sp[1][-1] == '\n':
                    sp[1] = sp[1][:-1]
                changePwd(log, config, sp[0], sp[1], config.newPassword)
                line = f.readline()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    try:
        log, config = init()
        main(log, config)
    except (KeyboardInterrupt, SystemExit):
        print("程序退出")
        sys.exit()
    print("程序退出,将在3秒后结束")
    print("本次运行结果可于log文件夹中查看")
    time.sleep(3)
