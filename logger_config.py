import logging


def setup_logger(level=logging.INFO):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create format
    formatter = logging.Formatter('%(asctime)s  %(threadName)s  [%(levelname)s]  %(name)s:  %(message)s')

    file_handler = logging.FileHandler('data_log.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Add log info to logger file
    logger.addHandler(file_handler)

    # # Tạo console handler và thiết lập formatter
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.INFO)
    # console_handler.setFormatter(formatter)
    #
    # # Thêm console handler vào logger
    # logger.addHandler(console_handler)

    return logger


app_logger = setup_logger()
