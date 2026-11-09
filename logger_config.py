import logging


def setup_logger():
    logger = logging.getLogger("call_center")
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="[%(asctime)s] | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
        )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


log = setup_logger()