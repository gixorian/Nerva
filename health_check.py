import os
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


def check_path(path):
    if os.path.exists(path):
        logger.info(f"{path} found.")
        return True
    else:
        logger.error(f"{path} not found.")
        return False


if __name__ == "__main__":
    target = os.getenv("CHECK_PATH", "/app")

    if check_path(target):
        sys.exit(0)
    else:
        sys.exit(1)
