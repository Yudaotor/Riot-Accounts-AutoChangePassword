import random
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
            for character in username:
                usernameInput.send_keys(character)
                time.sleep(random.uniform(0.02, 0.1))
            time.sleep(1)
            passwordInput = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "input[name=password]")))
            passwordInput.send_keys(Keys.CONTROL, 'a')
            for character in password:
                passwordInput.send_keys(character)
                time.sleep(random.uniform(0.02, 0.1))
            time.sleep(1)
            submitButton = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "button[data-testid=btn-signin-submit]")))
            self.driver.execute_script("arguments[0].click();", submitButton)
            try:
                captchaIframe = WebDriverWait(self.driver, 5).until(ec.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='captcha']")))
                captchaDiv = WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.CSS_SELECTOR, "div.interface-wrapper")))
                print(_("遇到图片验证码", "red", self.config.language))
                if captchaIframe:
                    self.driver.switch_to.default_content()
                print(username + _(" 失败", "red", self.config.language))
                self.log.error(username + _log(" 失败", self.config.language))
                return False
            except Exception:
                pass
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
            currentPasswordInput = self.driver.find_element(by=By.CSS_SELECTOR, value='input[data-testid=password-card__currentPassword]')
            for character in password:
                currentPasswordInput.send_keys(character)
                time.sleep(random.uniform(0.02, 0.1))
            time.sleep(0.5)
            newPasswordInput = self.driver.find_element(by=By.CSS_SELECTOR, value='input[data-testid=password-card__newPassword]')
            for character in newPassword:
                newPasswordInput.send_keys(character)
                time.sleep(random.uniform(0.02, 0.1))
            time.sleep(0.5)
            confirmNewPasswordInput = self.driver.find_element(by=By.CSS_SELECTOR, value='input[data-testid=password-card__confirmNewPassword]')
            for character in newPassword:
                confirmNewPasswordInput.send_keys(character)
                time.sleep(random.uniform(0.02, 0.1))
            time.sleep(0.5)
            self.driver.find_element(by=By.CSS_SELECTOR, value='button[data-testid=password-card__submit-btn]').click()
            time.sleep(1)
            Export(delimiter).writeSuccAcc(username, newPassword)
            self.log.info(username + _log(" 成功", self.config.language))
            print(username + _(" 成功", "green", self.config.language))
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
            # self.driver.find_element(by=By.XPATH, value='//*[@id="riotbar-account-bar"]/div/div').click()
            # time.sleep(1)
            # self.driver.find_element(by=By.XPATH, value='//*[@id="riotbar-account-dropdown-links"]/a[3]').click()
            # time.sleep(2)
            # self.driver.delete_all_cookies()
            # self.driver.refresh()
            pass
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
                self.log.error(_log("IMAP获取验证码失败 请检查是否打开了IMAP", self.config.language))
                print(_("IMAP获取验证码失败 请检查是否打开了IMAP", "red", self.config.language))
                return False
            twoFaCodeInput = self.driver.find_element(by=By.CSS_SELECTOR, value='input[data-testid=input-mfa]')
            twoFaCodeInput.send_keys(req.code)
            time.sleep(1)
            self.driver.find_element(by=By.CSS_SELECTOR, value='button[type=submit]').click()
            time.sleep(3)
            self.driver.implicitly_wait(10)
            if len(req.code) == 6:
                return True
            else:
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
