import logging
import os
import yaml
from yaml.parser import ParserError
from rich import print
from pathlib import Path
from I18n import _, _log


class Config:
    def __init__(self, log: logging.Logger, configPath: str) -> None:
        try:
            configPath = self.__findConfig(configPath)
            if configPath is None:
                print("[red]Config file not found")
                log.error("Config file not found")
                input("Press Enter to exit...")
                os.kill(os.getpid(), 9)
            with open(configPath, "r", encoding='utf-8') as f:
                config = yaml.safe_load(f)
                self.newPassword = config.get("newPassword")
                self.accountFilePath = config.get("accountFilePath").strip('u202a')
                self.accountDelimiter = config.get("accountDelimiter", "----")
                self.browser = config.get("browser", "edge")
                self.imapServer = config.get("imapServer", "")
                self.imapUsername = config.get("imapUsername", "")
                self.imapPassword = config.get("imapPassword", "")
                self.imapDelay = config.get("imapDelay", 10)
                self.language = config.get("language", "zh_CN")
                self.format()
        except (ParserError, KeyError):
            log.error("Config file format error")
            print("[red]Config file format error")
            input("Press Enter to exit...")
            os.kill(os.getpid(), 9)
        except Exception:
            log.error("Config file read error")
            print("[red]Config file read error")
            input("Press Enter to exit...")
            os.kill(os.getpid(), 9)

    def __findConfig(self, configPath):
        configPath = Path(configPath)
        if configPath.exists():
            return configPath
        else:
            return None

    def format(self):
        if self.language not in ["zh_CN", "en_US", "zh_TW"]:
            self.language = "zh_CN"
            print(_("语言格式错误, 已重置为默认值zh_CN", "red", self.language))
        if isinstance(self.imapDelay, str):
            try:
                self.imapDelay = int(self.imapDelay)
            except ValueError:
                self.imapDelay = 10
        else:
            self.imapDelay = 10

        if isinstance(self.accountDelimiter, str):
            if self.accountDelimiter == "":
                self.accountDelimiter = "----"
        else:
            print(_("分隔符格式错误, 已重置为默认值----", "red", self.language))
            logging.error(_log("分隔符格式错误, 已重置为默认值----", self.language))
            self.accountDelimiter = "----"

        if isinstance(self.browser, str):
            if self.browser not in ["edge", "chrome"]:
                print(_("浏览器格式错误, 已重置为默认值edge", "red", self.language))
                logging.error(_log("浏览器格式错误, 已重置为默认值edge", self.language))
                self.browser = "edge"
        else:
            print(_("浏览器格式错误, 已重置为默认值edge", "red", self.language))
            logging.error(_log("浏览器格式错误, 已重置为默认值edge", self.language))
            self.browser = "edge"
        if isinstance(self.imapServer, str):
            if self.imapServer == "":
                self.imapServer = ""
        else:
            print(_("imap服务器格式错误, 已重置为空", "red", self.language))
            logging.error(_log("imap服务器格式错误, 已重置为空", self.language))
            self.imapServer = ""
        if isinstance(self.imapUsername, str):
            if self.imapUsername == "":
                self.imapUsername = ""
        else:
            print(_("imap用户名格式错误, 已重置为空", "red", self.language))
            logging.error(_log("imap用户名格式错误, 已重置为空", self.language))
            self.imapUsername = ""
        if isinstance(self.imapPassword, str):
            if self.imapPassword == "":
                self.imapPassword = ""
        else:
            print(_("imap密码格式错误, 已重置为空", "red", self.language))
            logging.error(_log("imap密码格式错误, 已重置为空", self.language))
            self.imapPassword = ""
        if self.imapServer == "imap.qq.com":
            print(_("检测到您使用的是QQ邮箱, 请注意QQ邮箱的IMAP功能需要手动开启,以及需要的是授权码而非密码", "yellow", self.language))
            logging.warning(_log("检测到您使用的是QQ邮箱, 请注意QQ邮箱的IMAP功能需要手动开启,以及需要的是授权码而非密码", self.language))
        elif self.imapServer == "imap.163.com" or self.imapServer == "imap.126.com":
            print(_("检测到您使用的是网易邮箱, 请注意网易邮箱的IMAP功能需要手动开启,以及需要的是授权码而非密码", "yellow", self.language))
            logging.warning(_log("检测到您使用的是网易邮箱, 请注意网易邮箱的IMAP功能需要手动开启,以及需要的是授权码而非密码", self.language))
