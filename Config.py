import yaml
from yaml.parser import ParserError
from rich import print
from pathlib import Path


class Config:
    def __init__(self, configPath: str) -> None:
        try:
            configPath = self.__findConfig(configPath)
            with open(configPath, "r", encoding='utf-8') as f:
                config = yaml.safe_load(f)
                self.msedgedriverPath = config.get("msedgedriverPath")
                self.newPassword = config.get("newPassword")
                self.accountFilePath = config.get("accountFilePath")
        except FileNotFoundError as ex:
            print(f"[red]严重错误: 配置文件不存在 \n")
            print("按任意键退出")
            input()
            raise ex
        except (ParserError, KeyError) as ex:
            print(f"[red]严重错误: 配置文件格式错误")
            print("按任意键退出")
            input()
            raise ex

    def __findConfig(self, configPath):
        configPath = Path(configPath)
        if configPath.exists():
            return configPath
