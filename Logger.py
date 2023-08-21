import logging
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path

FILE_SIZE = 1024 * 1024 * 100
BACKUP_COUNT = 5
PROGRAM_NAME = "AutoChangePassword"
GITHUB_ADDRESS = "https://github.com/Yudaotor/Riot-Accounts-AutoChangePassword"
version = "2.6"


class Logger:
    @staticmethod
    def createLogger(log_path=Path("./logs")):
        """
        Create and return a logger instance
        Args:
            log_path (Path, optional): The path where the log file is saved. Defaults to Path("./logs/programs").
        Returns:
            logging.Logger: Logger instance.
        """
        log_path.mkdir(parents=True, exist_ok=True)
        level = logging.INFO
        fileHandler = RotatingFileHandler(
            log_path / f"{PROGRAM_NAME}-{time.strftime('%b-%d-%H-%M')}.log",
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
        logg = logging.getLogger(PROGRAM_NAME)
        logg.info("-" * 50)
        logg.info(f"{'-' * 22} Program started {version}   {'-' * 23}")
        logg.info(f"{'-' * 22} Open Source on github  {'-' * 22}")
        logg.info(f"{'-' * 7} Address: {GITHUB_ADDRESS} {'-' * 6}")
        logg.info(f"{'-' * 16} Please give me a star,Thanks(*^_^*)  {'-' * 15}")
        logg.info("-" * 50)
        logg.info(f"请我喝杯咖啡吧~https://github.com/Yudaotor")
        return logg


log = Logger().createLogger()


