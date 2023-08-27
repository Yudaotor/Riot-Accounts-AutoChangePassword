import time
from traceback import print_exc


class Export:
    def __init__(self, delimiter):
        self.delimiter = delimiter

    def write_success_acc(self, username, password, email_verify=""):
        try:
            with open('./newAccounts/' + email_verify + time.strftime("%Y%m%d-") + 'accounts.txt', 'a', encoding="utf-8") as f:
                f.write(f"{username}{self.delimiter}{password}\n")
        except Exception:
            print_exc()

