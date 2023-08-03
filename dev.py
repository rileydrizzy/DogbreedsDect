"""
doc
"""

from pathlib import Path

import opendatasets as od

from src.utils.logger import logger

data_raw = Path("data/raw")
DATA_URL = "https://www.kaggle.com/datasets/jessicali9530/stanford-dogs-dataset"


def download_data(data_dir):
    """
    DOC
    """
    try:
        od.download_kaggle_dataset(dataset_url=DATA_URL, data_dir=data_dir)
        return True
    except Exception:
        return False


def main():
    """
    doc
    """
    logger.info("Downloading data into Data Directory")
    results = download_data(data_dir=data_raw)
    if results:
        logger.success("Data has been successfully downloaded")
    else:
        logger.error("Data wasn't downloaded, an error occur")


if __name__ == "__main__":
    main()
