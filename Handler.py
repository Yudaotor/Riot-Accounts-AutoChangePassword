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
from Logger import log
from Config import config


def imap_hook(username, password, server):
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
        print(_("IMAP连接失败", "red", config.language))
        log.error(_log("IMAP连接失败", config.language))
        log.error(format_exc())


class Handler:
    def __init__(self, driver_instance):
        self.driver_instance = driver_instance
        self.accept_cookies()

    def accept_cookies(self):
        """
        Accepts the cookies on the web page.

        Returns:
            None
        """
        try:
            time.sleep(1)
            self.driver_instance.implicitly_wait(2)
            cookie_button = self.driver_instance.find_elements(By.XPATH, '/html/body/div[1]/div[2]/div[2]/button[2]')
            if len(cookie_button) > 0:
                cookie_button[0].click()
            self.driver_instance.implicitly_wait(10)
        except Exception:
            print(_("接受Cookies发生错误", "red", config.language))
            log.error(_log("接受Cookies发生错误", config.language))
            log.error(format_exc())

    def automatic_login(self, username, password) -> bool:
        """
        Performs automatic login with the provided username and password.

        Args:
            username (str): The username for login.
            password (str): The password for login.

        Returns:
            bool: True if the login is successful, False otherwise.

        """
        try:
            self.driver_instance.implicitly_wait(10)
            time.sleep(2)
            wait = WebDriverWait(self.driver_instance, 10)
            username_input = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "input[name=username]")))
            username_input.send_keys(Keys.CONTROL, 'a')
            for character in username:
                username_input.send_keys(character)
                time.sleep(random.uniform(0.02, 0.1))
            time.sleep(1)
            password_input = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "input[name=password]")))
            password_input.send_keys(Keys.CONTROL, 'a')
            for character in password:
                password_input.send_keys(character)
                time.sleep(random.uniform(0.02, 0.1))
            time.sleep(1)
            submit_button = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "button[data-testid=btn-signin-submit]")))
            self.driver_instance.execute_script("arguments[0].click();", submit_button)
            try:
                captcha_iframe = WebDriverWait(self.driver_instance, 2).until(ec.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='captcha']")))
                captcha_div = WebDriverWait(self.driver_instance, 2).until(ec.presence_of_element_located((By.CSS_SELECTOR, "div.interface-wrapper")))
                print(_("遇到图片验证码", "red", config.language))
                if captcha_iframe:
                    self.driver_instance.switch_to.default_content()
                print(username + _(" 失败", "red", config.language))
                log.error(username + _log(" 失败", config.language))
                return False
            except Exception:
                pass
            return True
        except Exception:
            log.error(username + _log(" 失败", config.language))
            print(username + _(" 失败", "red", config.language))
            self.driver_instance.delete_all_cookies()
            self.driver_instance.refresh()
            print(_("登录时发生错误", "red", config.language))
            log.error(_log("登录时发生错误", config.language))
            log.error(format_exc())
            return False

    def change_password(self, username, password) -> bool:
        new_password = config.new_password
        delimiter = config.account_delimiter
        try:
            current_password_input = self.driver_instance.find_element(by=By.CSS_SELECTOR, value='input[data-testid=password-card__currentPassword]')
            for character in password:
                current_password_input.send_keys(character)
                time.sleep(random.uniform(0.02, 0.1))
            time.sleep(0.5)
            new_password_input = self.driver_instance.find_element(by=By.CSS_SELECTOR, value='input[data-testid=password-card__newPassword]')
            for character in new_password:
                new_password_input.send_keys(character)
                time.sleep(random.uniform(0.02, 0.1))
            time.sleep(0.5)
            confirm_new_password_input = self.driver_instance.find_element(by=By.CSS_SELECTOR, value='input[data-testid=password-card__confirmNewPassword]')
            for character in new_password:
                confirm_new_password_input.send_keys(character)
                time.sleep(random.uniform(0.02, 0.1))
            time.sleep(0.5)
            self.driver_instance.find_element(by=By.CSS_SELECTOR, value='button[data-testid=password-card__submit-btn]').click()
            time.sleep(1)
            Export(delimiter).write_success_acc(username, new_password, email_verify=config.imap_username)
            log.info(username + _log(" 成功", config.language))
            print(username + _(" 成功", "green", config.language))
            return True
        except Exception:
            log.error(username + _log(" 失败", config.language))
            print(username + _(" 失败", "red", config.language))
            print(_("改密时发生错误", "red", config.language))
            log.error(_log("改密时发生错误", config.language))
            log.error(format_exc())
            return False

    def account_log_out(self):
        try:
            time.sleep(2)
        except Exception:
            print(_("登出时发生错误", "red", config.language))
            log.error(_log("登出时发生错误", config.language))
            log.error(format_exc())

    def imap_login(self) -> bool:
        imap_delay = config.imap_delay
        imap_username = config.imap_username
        imap_password = config.imap_password
        imap_server = config.imap_server
        try:
            time.sleep(imap_delay)
            req = imap_hook(imap_username, imap_password, imap_server)
            if req is None:
                log.error(_log("IMAP获取验证码失败 请检查是否打开了IMAP", config.language))
                print(_("IMAP获取验证码失败 请检查是否打开了IMAP", "red", config.language))
                return False
            elif req.code == "":
                log.error(_log("获取对应邮件失败 请调整imapDelay到合适时间", config.language))
                print(_("获取对应邮件失败 请调整imapDelay到合适时间", "red", config.language))
                return False
            self.driver_instance.implicitly_wait(5)
            two_fa_code_input = self.driver_instance.find_element(by=By.CSS_SELECTOR, value='input[data-testid=input-mfa]')
            two_fa_code_input.send_keys(req.code)
            time.sleep(1)
            self.driver_instance.find_element(by=By.CSS_SELECTOR, value='button[type=submit]').click()
            time.sleep(3)
            self.driver_instance.implicitly_wait(10)
            if len(req.code) == 6:
                return True
            else:
                log.error(imap_username + _log(" 邮箱验证码获取失败", config.language))
                print(imap_username + _(" 邮箱验证码获取失败", "red", config.language))
                return False
        except Exception:
            log.error(imap_username + _log(" 邮箱验证码获取失败", config.language))
            print(imap_username + _(" 邮箱验证码获取失败", "red", config.language))
            self.driver_instance.delete_all_cookies()
            self.driver_instance.refresh()
            log.error(format_exc())
            return False
