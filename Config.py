import logging
import os
import yaml
from yaml.parser import ParserError
from rich import print
from pathlib import Path


class Config:
    def __init__(self, log: logging.Logger, configPath: str) -> None:
        try:
            configPath = self.__findConfig(configPath)
            if configPath is None:
                print("[red]配置文件找不到")
                log.error("配置文件找不到")
                input("按回车键退出...")
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
                self.format()
        except (ParserError, KeyError):
            log.error("配置文件格式错误")
            print("[red]配置文件格式错误")
            input("按回车键退出...")
            os.kill(os.getpid(), 9)
        except Exception:
            log.error("配置文件读取错误")
            print("[red]配置文件读取错误")
            input("按回车键退出...")
            os.kill(os.getpid(), 9)

    def __findConfig(self, configPath):
        configPath = Path(configPath)
        if configPath.exists():
            return configPath
        else:
            return None

    def format(self):
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
            print("[red]分隔符格式错误, 已重置为默认值----")
            logging.error("分隔符格式错误, 已重置为默认值----")
            self.accountDelimiter = "----"

        if isinstance(self.browser, str):
            if self.browser not in ["edge", "chrome"]:
                print("[red]浏览器格式错误, 已重置为默认值edge")
                logging.error("浏览器格式错误, 已重置为默认值edge")
                self.browser = "edge"
        else:
            print("[red]浏览器格式错误, 已重置为默认值edge")
            logging.error("浏览器格式错误, 已重置为默认值edge")
            self.browser = "edge"
        if isinstance(self.imapServer, str):
            if self.imapServer == "":
                self.imapServer = ""
        else:
            print("[red]imap服务器格式错误, 已重置为空")
            logging.error("imap服务器格式错误, 已重置为空")
            self.imapServer = ""
        if isinstance(self.imapUsername, str):
            if self.imapUsername == "":
                self.imapUsername = ""
        else:
            print("[red]imap用户名格式错误, 已重置为空")
            logging.error("imap用户名格式错误, 已重置为空")
            self.imapUsername = ""
        if isinstance(self.imapPassword, str):
            if self.imapPassword == "":
                self.imapPassword = ""
        else:
            print("[red]imap密码格式错误, 已重置为空")
            logging.error("imap密码格式错误, 已重置为空")
            self.imapPassword = ""
        if self.imapServer == "imap.qq.com":
            print("[yellow]提示:QQ邮箱需要的不是密码, 而是授权码,如已经是授权码请忽略")
