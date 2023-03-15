from selenium import webdriver
from selenium_driver_updater import DriverUpdater
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService


class Webdriver:
    def __init__(self, browser, driverPath) -> None:
        self.browser = browser
        self.driverPath = driverPath

    def createWebdriver(self):
        match self.browser:
            case "chrome":
                options = self.addWebdriverOptions(webdriver.ChromeOptions())
                service = ChromeService(self.driverPath)
                return webdriver.Chrome(service=service, options=options)
            case "firefox":
                options = self.addWebdriverOptions(webdriver.FirefoxOptions())
                service = FirefoxService(self.driverPath)
                return webdriver.Firefox(service=service, options=options)
            case "edge":
                options = self.addWebdriverOptions(webdriver.EdgeOptions())
                service = EdgeService(self.driverPath)
                return webdriver.Edge(service=service, options=options)

    def addWebdriverOptions(self, options):
        options.add_argument("log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41"
        options.add_argument(f'user-agent={user_agent}')
        return options
