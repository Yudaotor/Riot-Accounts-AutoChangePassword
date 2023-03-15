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


def init() -> tuple[logging.Logger, Config, webdriver.Edge]:
    global driver, config, log
    try:
        parser = argparse.ArgumentParser(description='英雄联盟外服自动改密码')
        parser.add_argument('-c', '--config', dest="configPath", default="./config.yaml", help='Path to a custom config file')
        args = parser.parse_args()
        Path("./logs/").mkdir(parents=True, exist_ok=True)
        log = Logger.createLogger()
        config = Config(log, args.configPath)
        try:
            driver = Webdriver(browser=config.browser, driverPath=config.webDriverPath).createWebdriver()
        except Exception as ex:
            print(ex)
            print("[red]找不到对应的webDriver!请检查路径是否正确或是否适配自己浏览器版本\n按任意键退出...")
            input()
            exit()
        # 载入网页
        driver.implicitly_wait(10)  # 隐式等待时间
        driver.maximize_window()  # 最大化窗口
    except Exception as e:
        print(e)
    return log, config, driver


CURRENT_VERSION = 2.0
log, config, driver = init()
handle = Handler(log=log, driver=driver)
if not VersionManager.isLatestVersion(CURRENT_VERSION):
    print("[red]!!! 新版本可用 !!! 从此处下载: https://github.com/Yudaotor/Riot-Accounts-AutoChangePassword/releases/latest")


def main(config: Config):
    print(f"[yellow]------------v{CURRENT_VERSION}程序启动-------------")
    try:
        with open(config.accountFilePath) as f:
            line = f.readline()
            while line:
                sp = line.split('----')
                if sp[1][-1] == '\n':
                    sp[1] = sp[1][:-1]
                    handle.automaticLogIn(sp[0], sp[1])
                    handle.automaticChangePassword(sp[0], sp[1], config.newPassword)
                    handle.automaticLogOut()
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
    exit()
