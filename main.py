import argparse
import logging
import sys
from pathlib import Path
from Handler import Handler
from VersionManager import VersionManager
from Webdriver import Webdriver
from selenium import webdriver
import time
from rich import print
from Config import Config
from Logger import Logger


# coding:utf-8


def init() -> tuple[logging.Logger, Config, webdriver.Edge, Handler]:
    global driver, config, log, handler
    try:
        parser = argparse.ArgumentParser(description='英雄联盟外服自动改密码')
        parser.add_argument('-c', '--config', dest="configPath", default="./config.yaml", help='Path to a custom config file')
        args = parser.parse_args()
        Path("./logs/").mkdir(parents=True, exist_ok=True)
        log = Logger.createLogger()
        config = Config(log, args.configPath)
        try:
            driver = Webdriver(browser=config.browser, driverPath=config.webDriverPath).createWebdriver()
            driver.get('https://auth.riotgames.com/login#acr_values=urn%3Ariot%3Agold&client_id=accountodactyl-prod&redirect_uri'
                       '=https%3A%2F%2Faccount.riotgames.com%2Foauth2%2Flog-in&response_type=code&scope=openid%20email%20profile'
                       '%20riot%3A%2F%2Friot.atlas%2Faccounts.edit%20riot%3A%2F%2Friot.atlas%2Faccounts%2Fpassword.edit%20riot'
                       '%3A%2F%2Friot.atlas%2Faccounts%2Femail.edit%20riot%3A%2F%2Friot.atlas%2Faccounts.auth%20riot%3A%2F'
                       '%2Fthird_party.revoke%20riot%3A%2F%2Fthird_party.query%20riot%3A%2F%2Fforgetme%2Fnotify.write%20riot%3A'
                       '%2F%2Friot.authenticator%2Fauth.code%20riot%3A%2F%2Friot.authenticator%2Fauthz.edit%20riot%3A%2F%2Frso'
                       '%2Fmfa%2Fdevice.write%20riot%3A%2F%2Friot.authenticator%2Fidentity.add&state=547c8cd2-9eb0-4302-b9b2'
                       '-f29ee843a4bd&ui_locales=zh-Hans')
        except Exception as ex:
            print(ex)
            print("[red]找不到对应的webDriver!请检查路径是否正确或是否适配自己浏览器版本\n按任意键退出...")
            log.error("找不到对应的webDriver!请检查路径是否正确或是否适配自己浏览器版本")
            input()
            exit()
        # 载入网页
        driver.implicitly_wait(10)  # 隐式等待时间
        driver.maximize_window()  # 最大化窗口
        handler = Handler(log=log, driver=driver)
        handler.acceptCookies()
    except Exception as e:
        print(e)
        log.error(e)
    return log, config, driver, handler


CURRENT_VERSION = 2.22
log, config, driver, handler = init()

if not VersionManager.isLatestVersion(CURRENT_VERSION):
    print("[red]!!! 新版本可用 !!! 从此处下载: https://github.com/Yudaotor/Riot-Accounts-AutoChangePassword/releases/latest")


def main(config: Config):
    print(f"[yellow]------------v{CURRENT_VERSION}程序启动-------------")
    try:
        with open(config.accountFilePath) as f:
            line = f.readline()
            while line:
                sp = line.split('----')
                if sp:
                    if sp[1][-1] == '\n':
                        sp[1] = sp[1][:-1]
                        if handler.automaticLogIn(sp[0], sp[1]):
                            if config.imapServer != "":
                                if handler.imapLogIn(config.imapUsername, config.imapPassword, config.imapServer):
                                    if handler.automaticChangePassword(sp[0], sp[1], config.newPassword):
                                        handler.automaticLogOut()
                            elif handler.automaticChangePassword(sp[0], sp[1], config.newPassword):
                                handler.automaticLogOut()
                line = f.readline()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    try:
        main(config)
    except (KeyboardInterrupt, SystemExit):
        print("[red]------程序退出------")
        sys.exit()
    print("[yellow]------程序退出, 将在3秒后结束------")
    print("[yellow]---本次运行结果可于log文件夹中查看---")
    time.sleep(3)
    driver.quit()
    exit()
