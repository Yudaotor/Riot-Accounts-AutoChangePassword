import argparse
import logging
import sys
from pathlib import Path
from selenium import webdriver
import time
from Config import Config
from Logger import Logger


# coding:utf-8


def changePwd(log: logging.Logger, config: Config, username, password, newPassword):
    global driver
    try:
        driver = webdriver.Edge(config.msedgedriverPath)
        driver.get(
            'https://auth.riotgames.com/login#acr_values=urn%3Ariot%3Agold&client_id=accountodactyl-prod&redirect_uri=https%3A%2F%2Faccount.riotgames.com%2Foauth2%2Flog-in&response_type=code&scope=openid%20email%20profile%20riot%3A%2F%2Friot.atlas%2Faccounts.edit%20riot%3A%2F%2Friot.atlas%2Faccounts%2Fpassword.edit%20riot%3A%2F%2Friot.atlas%2Faccounts%2Femail.edit%20riot%3A%2F%2Friot.atlas%2Faccounts.auth%20riot%3A%2F%2Fthird_party.revoke%20riot%3A%2F%2Fthird_party.query%20riot%3A%2F%2Fforgetme%2Fnotify.write%20riot%3A%2F%2Friot.authenticator%2Fauth.code%20riot%3A%2F%2Friot.authenticator%2Fauthz.edit%20riot%3A%2F%2Frso%2Fmfa%2Fdevice.write%20riot%3A%2F%2Friot.authenticator%2Fidentity.add&state=547c8cd2-9eb0-4302-b9b2-f29ee843a4bd&ui_locales=zh-Hans')
        driver.implicitly_wait(10)  # 隐式等待时间
        driver.set_window_size(1200, 800)  # 浏览器窗口大小
        driver.find_element_by_xpath(
            '/html/body/div[2]/div/div/div[2]/div/div/div[2]/div/div/div/div[1]/div/input').send_keys(username)
        driver.find_element_by_xpath(
            '/html/body/div[2]/div/div/div[2]/div/div/div[2]/div/div/div/div[2]/div/input').send_keys(password)
        driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div/div/button').click()
        # 密码
        driver.find_element_by_xpath('//*[@id="riot-account"]/div/div[2]/div/div[2]/div[1]/div/div/input').send_keys(
            password)
        driver.find_element_by_xpath('//*[@id="riot-account"]/div/div[2]/div/div[2]/div[3]/div/input').send_keys(
            newPassword)
        driver.find_element_by_xpath('//*[@id="riot-account"]/div/div[2]/div/div[2]/div[2]/div/input').send_keys(
            newPassword)
        driver.find_element_by_xpath('//*[@id="riot-account"]/div/div[1]/p').click()
        driver.find_element_by_xpath('//*[@id="riot-account"]/div/div[2]/div/div[3]/button[2]').click()
        print(username + " Success")
        log.info(username + " Success")
        time.sleep(3)
    except Exception:
        print(username + " Fail")
        log.error(username + " Fail")
    finally:
        driver.quit()


def init() -> tuple[logging.Logger, Config]:
    parser = argparse.ArgumentParser(description='英雄联盟外服自动改密码')
    parser.add_argument('-c', '--config', dest="configPath", default="./config.yaml",
                        help='Path to a custom config file')
    args = parser.parse_args()
    Path("./logs/").mkdir(parents=True, exist_ok=True)
    config = Config(args.configPath)
    log = Logger.createLogger()
    return log, config


def main(log: logging.Logger, config: Config):
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
        print("发生错误")


if __name__ == '__main__':
    try:
        log, config = init()
        main(log, config)
    except (KeyboardInterrupt, SystemExit):
        print('退出成功,欢迎使用本软件!')
        sys.exit()
