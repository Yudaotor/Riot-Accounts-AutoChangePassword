import os
from traceback import format_exc

import yaml
from yaml.parser import ParserError
from rich import print
from pathlib import Path
from I18n import _, _log
from Logger import log
import sys
from Password import Password

class Config:
    def __init__(self, config_path):
        try:
            config_path = self.find_config(config_path)
            if config_path is None:
                print("[red]Config file not found[/]")
                log.error("Config file not found")
                input("Press Enter to exit...")
                os.kill(os.getpid(), 9)
            with open(config_path, "r", encoding='utf-8') as f:
                configg = yaml.safe_load(f)
                self.new_password = configg.get("newPassword")
                if self.new_password == "":
                    self.new_password = Password().value
                    
                self.account_file_path = configg.get("accountFilePath").strip('u202a')
                self.account_delimiter = configg.get("accountDelimiter", "----")
                self.browser = configg.get("browser", "edge")
                self.imap_server = configg.get("imapServer", "")
                self.imap_username = configg.get("imapUsername", "")
                self.imap_password = configg.get("imapPassword", "")
                self.imap_delay = configg.get("imapDelay", 10)
                self.language = configg.get("language", "zh_CN")
                self.format()
        except (ParserError, KeyError):
            log.error("Config file format error")
            log.error(format_exc())
            print("[red]Config file format error[/]")
            input("Press Enter to exit...")
            os.kill(os.getpid(), 9)
        except Exception:
            log.error("Config file read error")
            log.error(format_exc())
            print("[red]Config file read error[/]")
            input("Press Enter to exit...")
            os.kill(os.getpid(), 9)

    def find_config(self, config_path):
        """
        Finds the configuration file at the specified path.

        Args:
            config_path (str): The path to the configuration file.

        Returns:
            Union[Path, None]: The path to the configuration file if it exists, None otherwise.
        """
        config_path = Path(config_path)
        if config_path.exists():
            return config_path
        else:
            return None

    def format(self):
        """
        Formats the configuration values to ensure they are in the correct format.

        Returns:
            None
        """
        if self.language not in ["zh_CN", "en_US", "zh_TW"]:
            self.language = "zh_CN"
            print(_("语言格式错误, 已重置为默认值zh_CN", "red", self.language))
        valid, message = self.check_password_strength(self.new_password)
        if not valid:
            print(message)
            log.error(_log("密码强度不足", self.language))
            input("Press Enter to exit...")
            os.kill(os.getpid(), 9)
        if isinstance(self.imap_delay, str):
            try:
                self.imap_delay = int(self.imap_delay)
            except ValueError:
                self.imap_delay = 10
                print(_("延迟格式错误, 已重置为默认值10", "red", self.language))
        elif not isinstance(self.imap_delay, int):
            self.imap_delay = 10
            print(_("延迟格式错误, 已重置为默认值10", "red", self.language))
        if isinstance(self.account_delimiter, str):
            if self.account_delimiter == "":
                self.account_delimiter = "----"
        else:
            print(_("分隔符格式错误, 已重置为默认值----", "red", self.language))
            log.error(_log("分隔符格式错误, 已重置为默认值----", self.language))
            self.account_delimiter = "----"

        if isinstance(self.browser, str):
            if self.browser not in ["edge", "chrome"]:
                print(_("浏览器格式错误, 已重置为默认值edge", "red", self.language))
                log.error(_log("浏览器格式错误, 已重置为默认值edge", self.language))
                self.browser = "edge"
        else:
            print(_("浏览器格式错误, 已重置为默认值edge", "red", self.language))
            log.error(_log("浏览器格式错误, 已重置为默认值edge", self.language))
            self.browser = "edge"
        if isinstance(self.imap_server, str):
            if self.imap_server == "":
                self.imap_server = ""
        else:
            print(_("imap服务器格式错误, 已重置为空", "red", self.language))
            log.error(_log("imap服务器格式错误, 已重置为空", self.language))
            self.imap_server = ""
        if isinstance(self.imap_username, str):
            if self.imap_username == "":
                self.imap_username = ""
        else:
            print(_("imap用户名格式错误, 已重置为空", "red", self.language))
            log.error(_log("imap用户名格式错误, 已重置为空", self.language))
            self.imap_username = ""
        if isinstance(self.imap_password, str):
            if self.imap_password == "":
                self.imap_password = ""
        else:
            print(_("imap密码格式错误, 已重置为空", "red", self.language))
            log.error(_log("imap密码格式错误, 已重置为空", self.language))
            self.imap_password = ""
        if self.imap_server == "imap.qq.com":
            print(_("检测到您使用的是QQ邮箱, 请注意QQ邮箱的IMAP功能需要手动开启,以及需要的是授权码而非密码", "yellow", self.language))
            log.warning(_log("检测到您使用的是QQ邮箱, 请注意QQ邮箱的IMAP功能需要手动开启,以及需要的是授权码而非密码", self.language))
        elif self.imap_server == "imap.163.com" or self.imap_server == "imap.126.com":
            print(_("检测到您使用的是网易邮箱, 请注意网易邮箱的IMAP功能需要手动开启,以及需要的是授权码而非密码", "yellow", self.language))
            log.warning(_log("检测到您使用的是网易邮箱, 请注意网易邮箱的IMAP功能需要手动开启,以及需要的是授权码而非密码", self.language))
        if self.imap_server == "imap.gmail.com":
            print(_("检测到您使用的是谷歌邮箱, 请注意谷歌邮箱不可用 但是可以通过在谷歌邮箱设置中配置转发到其他可以支持的邮箱来获取验证码", "yellow", self.language))
            log.warning(_log("检测到您使用的是谷歌邮箱, 请注意谷歌邮箱不可用 但是可以通过在谷歌邮箱设置中配置转发到其他可以支持的邮箱来获取验证码", self.language))
        if self.imap_server:
            print(_("读取邮件延迟当前为: ", color='bold yellow', lang=self.language) + str(self.imap_delay) + _("秒", color='bold yellow', lang=self.language))
            log.info(_log("读取邮件延迟当前为: ", self.language) + str(self.imap_delay) + _log("秒", self.language))

    def check_password_strength(self, password):
        if len(password) < 8:
            return False, _("密码长度必须大于等于8", color="red", lang=self.language)

        if not any(char.isalpha() for char in password) or not any(char.isnumeric() or not char.isalnum() for char in password):
            return False, _("密码必须包含至少一个字母和一个非字母字符", color="red", lang=self.language)
        return True, ""

config_file = "./config.yaml"
if len(sys.argv) > 1:
    config_file = sys.argv[1]

print("使用配置文件：", config_file)

config = Config("./config.yaml")
