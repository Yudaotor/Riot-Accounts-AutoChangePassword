import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from rich import print


class Handler:
    def __init__(self, log, driver) -> None:
        self.log = log
        self.driver = driver

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
