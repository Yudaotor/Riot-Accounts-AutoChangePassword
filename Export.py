import time
from traceback import print_exc


class Export:
    def __init__(self, delimiter):
        self.delimiter = delimiter

    def writeSuccAcc(self, username, password):
        """
        Writes the successful account details to a file.

        Args:
            username (str): The username of the successful account.
            password (str): The password of the successful account.

        Returns:
            None
        """
        try:
            with open('./newAccounts/' + time.strftime("%Y%m%d-") + 'accounts.txt', 'a') as f:
                f.write(f"{username}{self.delimiter}{password}\n")
        except Exception:
            print_exc()

