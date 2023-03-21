import time


class Export:
    def __init__(self, delimiter):
        self.delimiter = delimiter

    def write_txt(self, username, password):
        with open('./newAccounts/' + time.strftime("%Y%m%d-") + 'accounts.txt', 'a') as f:
            f.write(f"{username}{self.delimiter}{password}\n")
