import logging
import yaml
from yaml.parser import ParserError
from rich import print
from pathlib import Path


class Config:
    def __init__(self, log: logging.Logger, configPath: str) -> None:
        try:
            configPath = self.__findConfig(configPath)
            with open(configPath, "r", encoding='utf-8') as f:
                config = yaml.safe_load(f)
                self.newPassword = config.get("newPassword")
                self.accountFilePath = config.get("accountFilePath").strip('u202a')
                self.browser = config.get("browser")
                self.webDriverPath = config.get("webDriverPath").strip('u202a')
                self.imapServer = config.get("imapServer", "")
                self.imapUsername = config.get("imapUsername", "")
                self.imapPassword = config.get("imapPassword", "")
        except FileNotFoundError as ex:
            log.error("配置文件找不到")
            print("[red]配置文件找不到")
            raise ex
        except (ParserError, KeyError) as ex:
            log.error("配置文件格式错误")
            print("[red]配置文件格式错误")
            raise ex

    def __findConfig(self, configPath):
        configPath = Path(configPath)
        if configPath.exists():
            return configPath
