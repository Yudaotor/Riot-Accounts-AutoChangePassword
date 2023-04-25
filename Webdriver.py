import traceback

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from rich import print


class Webdriver:
    def __init__(self, browser) -> None:
        self.browser = browser

    def createWebdriver(self):
        try:
            match self.browser:
                case "chrome":
                    driverPath = ChromeDriverManager(path=".\\driver").install()
                    options = self.addWebdriverOptions(webdriver.ChromeOptions())
                    service = ChromeService(driverPath)
                    return webdriver.Chrome(service=service, options=options)
                case "edge":
                    driverPath = EdgeChromiumDriverManager(path=".\\driver").install()
                    options = self.addWebdriverOptions(webdriver.EdgeOptions())
                    service = EdgeService(driverPath)
                    return webdriver.Edge(service=service, options=options)
                case _:
                    print("选择了不支持的浏览器")
        except Exception:
            print("[red]创建webdriver失败,请检查是否对应浏览器是否已经是最新版本.")
            traceback.print_exc()

    def addWebdriverOptions(self, options):
        prefs = {
            "profile.password_manager_enabled": False,
            "credentials_enable_service": False,
            'profile.default_content_setting_values': {
                'notifications': 2
            }
        }
        options.add_experimental_option('prefs', prefs)
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument('disable-infobars')
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41"
        options.add_argument(f'user-agent={user_agent}')
        return options
