import time
import traceback


class Export:
    def __init__(self, delimiter):
        self.delimiter = delimiter

    def writeSuccAcc(self, username, password):
        try:
            with open('./newAccounts/' + time.strftime("%Y%m%d-") + 'accounts.txt', 'a') as f:
                f.write(f"{username}{self.delimiter}{password}\n")
        except Exception:
            traceback.print_exc()

