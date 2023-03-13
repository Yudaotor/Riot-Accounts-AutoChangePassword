import logging
from logging.handlers import RotatingFileHandler

FILE_SIZE = 1024 * 1024 * 100  # 100 MB
BACKUP_COUNT = 5  # keep up to 5 files


class Logger:
    @staticmethod
    def createLogger():
        level = logging.INFO
        fileHandler = RotatingFileHandler(
            "./logs/passwordChange.log",
            mode="a+",
            maxBytes=FILE_SIZE,
            backupCount=BACKUP_COUNT,
            encoding='utf-8'
        )

        logging.basicConfig(
            format="%(asctime)s %(levelname)s: %(message)s",
            level=level,
            handlers=[fileHandler],
        )
        log = logging.getLogger("改密码")
        log.info("-------------------------------------------------")
        log.info(f"----------- Program started   ---------------")
        log.info(f"----------- 本项目开源于github   ---------------")
        log.info(f"----------- 地址:https://github.com/Yudaotor/Riot-Accounts-AutoChangePassword ---------------")
        log.info("-------------------------------------------------")
        return log