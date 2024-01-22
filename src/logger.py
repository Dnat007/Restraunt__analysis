import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)

# if there is a file then apppend in that
os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

FORMAT = '[%(asctime)s ] %(lineno)d %(name)s - %(levelname)s  - %(message)s'
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format=FORMAT,
    level=logging.INFO,

)

if __name__ == "__main__":
    logging.info("Logging has been started")
