import os
from traceback import format_exc
from pathlib import Path
from Handler import Handler
from VersionManager import VersionManager
from rich import print
from I18n import _, _log
from Logger import log
from Config import config
from Webdriver import web_driver_manager


def init():
    try:
        Path("./logs/").mkdir(parents=True, exist_ok=True)
        Path("./newAccounts/").mkdir(parents=True, exist_ok=True)
    except Exception:
        log.error(format_exc())


CURRENT_VERSION = 2.7
init()

if not VersionManager.isLatestVersion(CURRENT_VERSION):
    print("[yellow]--------------------------------------------------------------------[/]")
    print(f"{_('!!! 新版本可用 !!! 从此处下载:', color='yellow', lang=config.language)} https://github.com/Yudaotor/Riot-Accounts-AutoChangePassword/releases/latest")
    print("[yellow]--------------------------------------------------------------------[/]")


def main():
    print(f"[bold yellow]{'-' * 15}[/]"
          f"v {CURRENT_VERSION} "
          f"{_('程序启动', 'bold yellow', config.language)} "
          f"[bold yellow]{'-' * 15}[/]")
    print(f"{_('请我喝杯咖啡吧~https://github.com/Yudaotor', 'cyan', config.language)}")
    try:
        with open(config.account_file_path, encoding="utf-8") as f:
            line = f.readline()
            account_delimiter = config.account_delimiter
            imap_server = config.imap_server
            while line:
                sp = line.split(account_delimiter)
                if sp:
                    handler = Handler(web_driver_manager.create_driver_instance())
                    username = sp[0]
                    password = sp[1]
                    if password.endswith('\n'):
                        password = password[:-1]
                    if handler.automatic_login(username, password):
                        if imap_server != "":
                            if handler.imap_login():
                                if handler.change_password(username, password):
                                    handler.account_log_out()
                        elif handler.change_password(username, password):
                            handler.account_log_out()
                    line = f.readline()
                    handler.driver_instance.quit()
    except Exception:
        log.error(format_exc())


def quit_all():
    print(f'[bold yellow]----[/]                 {_("程序结束, 即将退出", "bold green", config.language)}                  [bold yellow]-----[/]')
    print(f"[bold yellow]----[/]     {_('请我喝杯咖啡吧~', 'cyan', config.language)} https://github.com/Yudaotor     [bold yellow]-----[/]")
    print(f'[bold yellow]----[/]   {_("修改成功的新账号密码请于newAccounts文件夹中查看", "bold green", config.language)}   [bold yellow]-----[/]')
    print(f'[bold yellow]----[/]           {_("本次运行结果可于log文件夹中查看", "bold green", config.language)}           [bold yellow]-----[/]')
    input()
    os.kill(os.getpid(), 9)


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        quit_all()
    quit_all()
