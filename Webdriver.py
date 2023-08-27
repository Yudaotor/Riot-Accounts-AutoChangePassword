from traceback import format_exc

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from rich import print
from I18n import _, _log
from Logger import log
from Config import config


def add_webdriver_options(options):
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
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu-shader-disk-cache")
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-cache")
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41"
    options.add_argument(f'user-agent={user_agent}')
    return options


class Webdriver:
    def __init__(self, browser):
        self.browser = browser
        self.driver_path = ""
        self.options = None
        self.service = None
        self.manager = None
        self.init_webdriver()

    def create_driver_instance(self):
        driver_instance = webdriver.Chrome(service=self.service, options=self.options)
        try:
            driver_instance.get('https://auth.riotgames.com/login#acr_values=urn%3Ariot%3Agold&client_id=accountodactyl-prod&redirect_uri'
                                '=https%3A%2F%2Faccount.riotgames.com%2Foauth2%2Flog-in&response_type=code&scope=openid%20email%20profile'
                                '%20riot%3A%2F%2Friot.atlas%2Faccounts.edit%20riot%3A%2F%2Friot.atlas%2Faccounts%2Fpassword.edit%20riot'
                                '%3A%2F%2Friot.atlas%2Faccounts%2Femail.edit%20riot%3A%2F%2Friot.atlas%2Faccounts.auth%20riot%3A%2F'
                                '%2Fthird_party.revoke%20riot%3A%2F%2Fthird_party.query%20riot%3A%2F%2Fforgetme%2Fnotify.write%20riot%3A'
                                '%2F%2Friot.authenticator%2Fauth.code%20riot%3A%2F%2Friot.authenticator%2Fauthz.edit%20riot%3A%2F%2Frso'
                                '%2Fmfa%2Fdevice.write%20riot%3A%2F%2Friot.authenticator%2Fidentity.add&state=547c8cd2-9eb0-4302-b9b2'
                                '-f29ee843a4bd&ui_locales=zh-Hans')
        except Exception:
            print(_("改密网站载入失败", "red", config.language))
            log.error(_log("改密网站载入失败"))
            log.error(format_exc())
            input(_log("按回车键退出...", config.language))
            exit()
        driver_instance.implicitly_wait(10)
        return driver_instance

    def init_webdriver(self):
        try:
            match self.browser:
                case "chrome":
                    custom_path = ".\\driver"
                    chrome_driver_manager = ChromeDriverManager(cache_manager=DriverCacheManager(custom_path))
                    self.driver_path = chrome_driver_manager.install()
                    self.options = add_webdriver_options(webdriver.ChromeOptions())
                    self.service = ChromeService(self.driver_path)
                case "edge":
                    custom_path = ".\\driver"
                    edge_chromium_driver_manager = EdgeChromiumDriverManager(cache_manager=DriverCacheManager(custom_path))
                    self.driver_path = edge_chromium_driver_manager.install()
                    self.options = add_webdriver_options(webdriver.EdgeOptions())
                    self.service = EdgeService(self.driver_path)
                case _:
                    print(_("选择了不支持的浏览器", "red", config.language))
        except Exception:
            print(_("初始化webdriver失败,请检查是否对应浏览器是否已经是最新版本.", "red", config.language))
            log.error(_log("初始化webdriver失败,请检查是否对应浏览器是否已经是最新版本.", config.language))
            log.error(format_exc())


web_driver_manager = Webdriver(config.browser)
