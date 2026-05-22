import logging
import sys
sys.stdout.reconfigure(encoding='utf-8')

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # -------------------------
    # Console Handler
    # -------------------------
    console_handler = logging.StreamHandler(sys.stdout)
    console_format = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    console_handler.setFormatter(console_format)

    # -------------------------
    # File Handler (IMPORTANT)
    # -------------------------
    file_handler = logging.FileHandler("app.log")
    file_format = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    file_handler.setFormatter(file_format)

    # Avoid duplicate logs
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    logger.info("Logging initialized")