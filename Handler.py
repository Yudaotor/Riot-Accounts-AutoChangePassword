import time
from imaplib2 import imaplib2
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from rich import print
from IMAP import IMAP


class Handler:
    def __init__(self, log, driver) -> None:
        self.log = log
        self.driver = driver

    def IMAPHook(self, username, password, server):
        try:
            M = imaplib2.IMAP4_SSL(server)
            M.login(username, password)
            M.select("INBOX")
            idler = IMAP(M)
            idler.start()
            idler.join()
            M.logout()
            return idler
        except Exception as e:
            print(e)

    def automaticLogIn(self, username, password) -> bool:
        try:
            time.sleep(1)
            wait = WebDriverWait(self.driver, 10)
            self.driver.implicitly_wait(2)
            cookieButton = self.driver.find_elements(By.XPATH, '/html/body/div[1]/div[2]/div[2]/button[2]')
            if len(cookieButton) > 0:
                cookieButton.click()
            time.sleep(1)
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
        except Exception as e:
            self.log.error(username + " Fail")
            print(username + " [red]Fail")
            return False

    def automaticChangePassword(self, username, password, newPassword) -> bool:
        try:
            self.driver.implicitly_wait(10)
            self.driver.find_element(by=By.XPATH, value='//*[@id="riot-account"]/div/div[2]/div/div[2]/div[1]/div/div/input').send_keys(password)
            time.sleep(1)
            self.driver.find_element(by=By.XPATH, value='//*[@id="riot-account"]/div/div[2]/div/div[2]/div[3]/div/input').send_keys(newPassword)
            time.sleep(1)
            self.driver.find_element(by=By.XPATH, value='//*[@id="riot-account"]/div/div[2]/div/div[2]/div[2]/div/input').send_keys(newPassword)
            time.sleep(1)
            self.driver.find_element(by=By.XPATH, value='//*[@id="riot-account"]/div/div[1]/p').click()
            self.driver.find_element(by=By.XPATH, value='//*[@id="riot-account"]/div/div[2]/div/div[3]/button[2]').click()
            time.sleep(2)
            self.log.info(username + " Success")
            print(username + " [green]Success")
            return True
        except Exception as e:
            self.log.error(username + " Fail")
            print(username + " [red]Fail")
            return False

    def automaticLogOut(self):
        self.driver.find_element(by=By.XPATH, value='//*[@id="riotbar-account-bar"]/div/div').click()
        self.driver.find_element(by=By.XPATH, value='//*[@id="riotbar-account-dropdown-links"]/a[3]').click()
        time.sleep(2)

    def imapLogIn(self, imapUsername, imapPassword, imapServer) -> bool:
        try:
            req = self.IMAPHook(imapUsername, imapPassword, imapServer)
            self.driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div/input').send_keys(req.code)
            self.driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div/div[2]/div/div/button').click()
            if len(req.code) == 6:
                return True
            else:
                return False
        except Exception as e:
            self.log.error(imapUsername + " 邮箱验证码获取失败")
            print(imapUsername + " [red]邮箱验证码获取失败")
            return False
