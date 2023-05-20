import time
from traceback import format_exc

from imaplib2 import imaplib2
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from rich import print
from IMAP import IMAP
from Export import Export
from selenium.webdriver.common.keys import Keys
from I18n import _, _log


class Handler:
    def __init__(self, log, driver, config) -> None:
        self.log = log
        self.driver = driver
        self.config = config

    def IMAPHook(self, username, password, server):
        """
        Establishes an IMAP connection and returns a mail object.

        Args:
            username (str): The username for the IMAP connection.
            password (str): The password for the IMAP connection.
            server (str): The server for the IMAP connection.

        Returns:
            IMAP: The mail object for the IMAP connection.

        """
        try:
            M = imaplib2.IMAP4_SSL(server)
            M.login(username, password)
            mail = IMAP(M, username)
            M.logout()
            return mail
        except Exception:
            print(_("IMAP连接失败", "red", self.config.language))
            self.log.error(_log("IMAP连接失败", self.config.language))
            self.log.error(format_exc())

    def acceptCookies(self):
        """
        Accepts the cookies on the web page.

        Returns:
            None
        """
        try:
            time.sleep(1)
            self.driver.implicitly_wait(2)
            cookieButton = self.driver.find_elements(By.XPATH, '/html/body/div[1]/div[2]/div[2]/button[2]')
            if len(cookieButton) > 0:
                cookieButton[0].click()
            self.driver.implicitly_wait(10)
        except Exception:
            print(_("接受Cookies发生错误", "red", self.config.language))
            self.log.error(_log("接受Cookies发生错误", self.config.language))
            self.log.error(format_exc())

    def automaticLogIn(self, username, password) -> bool:
        """
        Performs automatic login with the provided username and password.

        Args:
            username (str): The username for login.
            password (str): The password for login.

        Returns:
            bool: True if the login is successful, False otherwise.

        """
        try:
            self.driver.implicitly_wait(10)
            time.sleep(2)
            wait = WebDriverWait(self.driver, 10)
            usernameInput = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "input[name=username]")))
            usernameInput.send_keys(Keys.CONTROL, 'a')
            usernameInput.send_keys(username)
            time.sleep(1)
            passwordInput = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "input[name=password]")))
            passwordInput.send_keys(Keys.CONTROL, 'a')
            passwordInput.send_keys(password)
            submitButton = wait.until(ec.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/button")))
            self.driver.execute_script("arguments[0].click();", submitButton)
            return True
        except Exception:
            self.log.error(username + _log(" 失败", self.config.language))
            print(username + _(" 失败", "red", self.config.language))
            self.driver.delete_all_cookies()
            self.driver.refresh()
            print(_("登录时发生错误", "red", self.config.language))
            self.log.error(_log("登录时发生错误", self.config.language))
            self.log.error(format_exc())
            return False

    def changePassword(self, username, password, newPassword, delimiter) -> bool:
        """
        Changes the password for the given username.

        Args:
            username (str): The username for which the password is being changed.
            password (str): The current password.
            newPassword (str): The new password.
            delimiter (str): The delimiter for the exported file.

        Returns:
            bool: True if the password change is successful, False otherwise.
        """
        try:
            self.driver.find_element(by=By.XPATH, value='//*[@id="riot-account"]/div/div[2]/div/div[2]/div[1]/div/div/input').send_keys(password)
            time.sleep(1)
            self.driver.find_element(by=By.XPATH, value='//*[@id="riot-account"]/div/div[2]/div/div[2]/div[3]/div/input').send_keys(newPassword)
            time.sleep(1)
            self.driver.find_element(by=By.XPATH, value='//*[@id="riot-account"]/div/div[2]/div/div[2]/div[2]/div/input').send_keys(newPassword)
            time.sleep(1)
            self.driver.find_element(by=By.XPATH, value='//*[@id="riot-account"]/div/div[2]/div/div[2]/div[1]/div/div/input').click()
            time.sleep(1)
            self.driver.find_element(by=By.XPATH, value='//*[@id="riot-account"]/div/div[2]/div/div[3]/button[2]').click()
            time.sleep(2)
            Export(delimiter).writeSuccAcc(username, newPassword)
            self.log.info(username + _log(" 成功", self.config.language))
            print(username + _log(" 成功", self.config.language))
            return True
        except Exception:
            self.log.error(username + _log(" 失败", self.config.language))
            print(username + _(" 失败", "red", self.config.language))
            print(_("改密时发生错误", "red", self.config.language))
            self.log.error(_log("改密时发生错误", self.config.language))
            self.log.error(format_exc())
            return False

    def accountLogOut(self):
        """
        Logs out from the account.

        Returns:
            None
        """
        try:
            self.driver.find_element(by=By.XPATH, value='//*[@id="riotbar-account-bar"]/div/div').click()
            time.sleep(1)
            self.driver.find_element(by=By.XPATH, value='//*[@id="riotbar-account-dropdown-links"]/a[3]').click()
            time.sleep(2)
        except Exception:
            print(_("登出时发生错误", "red", self.config.language))
            self.log.error(_log("登出时发生错误", self.config.language))
            self.log.error(format_exc())

    def imapLogIn(self, imapUsername, imapPassword, imapServer, imapDelay) -> bool:
        """
        Logs in to the IMAP server and retrieves the verification code from the email.

        Args:
            imapUsername (str): The username for the IMAP connection.
            imapPassword (str): The password for the IMAP connection.
            imapServer (str): The server for the IMAP connection.
            imapDelay (int): The delay in seconds before fetching the email.

        Returns:
            bool: True if the IMAP login and verification code retrieval are successful, False otherwise.
        """
        try:
            time.sleep(imapDelay)
            req = self.IMAPHook(imapUsername, imapPassword, imapServer)
            if req is None or req.code == "":
                self.log.error(_log("IMAP获取验证码失败", self.config.language))
                print(_("IMAP获取验证码失败", "red", self.config.language))
                return False
            self.driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div/input').send_keys(req.code)
            self.driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div/div[2]/div/div/button').click()
            time.sleep(3)
            self.driver.implicitly_wait(10)
            buttonNumber = self.driver.find_elements(By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[2]/div[2]/div/div[1]')
            if len(req.code) == 6 and len(buttonNumber) > 0:
                return True
            else:
                self.driver.delete_all_cookies()
                self.driver.refresh()
                self.log.error(imapUsername + _log(" 邮箱验证码获取失败", self.config.language))
                print(imapUsername + _(" 邮箱验证码获取失败", "red", self.config.language))
                return False
        except Exception:
            self.log.error(imapUsername + _log(" 邮箱验证码获取失败", self.config.language))
            print(imapUsername + _(" 邮箱验证码获取失败", "red", self.config.language))
            self.driver.delete_all_cookies()
            self.driver.refresh()
            self.log.error(format_exc())
            return False
