import argparse
import logging
import sys
from traceback import format_exc
from pathlib import Path
from Handler import Handler
from VersionManager import VersionManager
from Webdriver import Webdriver
from selenium import webdriver
import time
from rich import print
from Config import Config
from Logger import Logger
from I18n import _, _log


# coding:utf-8


def init() -> tuple[logging.Logger, Config, webdriver.Edge, Handler]:
    global driver, config, log, handler
    try:
        parser = argparse.ArgumentParser(description='Riot Accounts Auto Change Password')
        parser.add_argument('-c', '--config', dest="configPath", default="./config.yaml", help='Path to a custom config file')
        args = parser.parse_args()
        Path("./logs/").mkdir(parents=True, exist_ok=True)
        Path("./newAccounts/").mkdir(parents=True, exist_ok=True)
        log = Logger.createLogger()
        config = Config(log, args.configPath)
        try:
            driver = Webdriver(browser=config.browser, config=config, log=log).createWebdriver()
            driver.get('https://auth.riotgames.com/login#acr_values=urn%3Ariot%3Agold&client_id=accountodactyl-prod&redirect_uri'
                       '=https%3A%2F%2Faccount.riotgames.com%2Foauth2%2Flog-in&response_type=code&scope=openid%20email%20profile'
                       '%20riot%3A%2F%2Friot.atlas%2Faccounts.edit%20riot%3A%2F%2Friot.atlas%2Faccounts%2Fpassword.edit%20riot'
                       '%3A%2F%2Friot.atlas%2Faccounts%2Femail.edit%20riot%3A%2F%2Friot.atlas%2Faccounts.auth%20riot%3A%2F'
                       '%2Fthird_party.revoke%20riot%3A%2F%2Fthird_party.query%20riot%3A%2F%2Fforgetme%2Fnotify.write%20riot%3A'
                       '%2F%2Friot.authenticator%2Fauth.code%20riot%3A%2F%2Friot.authenticator%2Fauthz.edit%20riot%3A%2F%2Frso'
                       '%2Fmfa%2Fdevice.write%20riot%3A%2F%2Friot.authenticator%2Fidentity.add&state=547c8cd2-9eb0-4302-b9b2'
                       '-f29ee843a4bd&ui_locales=zh-Hans')
        except Exception:
            print(_("webDriver创建失败!", "red", config.language))
            log.error(_log("webDriver创建失败!"))
            log.error(format_exc())
            input(_log("按回车键退出...", config.language))
            exit()
        # 载入网页
        driver.implicitly_wait(10)  # 隐式等待时间
        driver.maximize_window()  # 最大化窗口
        handler = Handler(log=log, driver=driver, config=config)
        handler.acceptCookies()
    except Exception:
        log.error(format_exc())
    return log, config, driver, handler


CURRENT_VERSION = 2.32
log, config, driver, handler = init()

if not VersionManager.isLatestVersion(CURRENT_VERSION):
    print("[yellow]--------------------------------------------------------------------")
    print(f"{_('!!! 新版本可用 !!! 从此处下载:', color='yellow', lang=config.language)} https://github.com/Yudaotor/Riot-Accounts-AutoChangePassword/releases/latest")
    print("[yellow]--------------------------------------------------------------------")


def main(config: Config):
    print(f"[bold yellow]{'-' * 15}[/bold yellow]"
          f"v{CURRENT_VERSION} "
          f"{_('程序启动', 'bold yellow', config.language)} "
          f"[bold yellow]{'-' * 15}[/bold yellow]")
    try:
        with open(config.accountFilePath) as f:
            line = f.readline()
            while line:
                sp = line.split(config.accountDelimiter)
                if sp:
                    if sp[1][-1] == '\n':
                        sp[1] = sp[1][:-1]
                    if handler.automaticLogIn(sp[0], sp[1]):
                        if config.imapServer != "":
                            if handler.imapLogIn(config.imapUsername, config.imapPassword, config.imapServer, config.imapDelay):
                                if handler.changePassword(sp[0], sp[1], config.newPassword, config.accountDelimiter):
                                    handler.accountLogOut()
                        elif handler.changePassword(sp[0], sp[1], config.newPassword, config.accountDelimiter):
                            handler.accountLogOut()
                line = f.readline()
    except Exception:
        log.error(format_exc())


if __name__ == '__main__':
    try:
        main(config)
    except (KeyboardInterrupt, SystemExit):
        print(f"[bold yellow]{'-' * 15}[/bold yellow]"
              f"{_('程序结束', 'bold yellow', config.language)} "
              f"[bold yellow]{'-' * 15}[/bold yellow]")
        sys.exit()
    print(_("----程序退出, 将在3秒后结束-----", "bold green", config.language))
    print(_("----修改成功的新账号密码请于newAccounts文件夹中查看-----", "bold green", config.language))
    print(_("----本次运行结果可于log文件夹中查看-----", "bold green", config.language))
    time.sleep(3)
    driver.quit()
    sys.exit()
