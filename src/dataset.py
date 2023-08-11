"""
doc
"""
import os
import xml.etree.ElementTree as ET
from pathlib import Path

import hydra
import opendatasets as od
import pandas as pd
from omegaconf import DictConfig

data_raw = Path("data/raw")
DATA_URL = "https://www.kaggle.com/datasets/jessicali9530/stanford-dogs-dataset"


def download_data(data_dir=data_raw):
    """
    DOC
    """
    try:
        od.download_kaggle_dataset(dataset_url=DATA_URL, data_dir=data_dir)
        return True
    except Exception:
        return False


def read_xml_annotation(xml_file_path):
    """
    doc
    """
    try:
        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Extract relevant information from the XML
        folder = root.find("folder").text
        filename = root.find("filename").text
        database = root.find("source/database").text
        width = int(root.find("size/width").text)
        height = int(root.find("size/height").text)
        depth = int(root.find("size/depth").text)
        object_name = root.find("object/name").text
        pose = root.find("object/pose").text
        truncated = int(root.find("object/truncated").text)
        difficult = int(root.find("object/difficult").text)
        xmin = int(root.find("object/bndbox/xmin").text)
        ymin = int(root.find("object/bndbox/ymin").text)
        xmax = int(root.find("object/bndbox/xmax").text)
        ymax = int(root.find("object/bndbox/ymax").text)

        # Create a dictionary to hold the extracted information
        annotation_info = {
            "folder": folder,
            "filename": filename,
            "database": database,
            "width": width,
            "height": height,
            "depth": depth,
            "object_name": object_name,
            "pose": pose,
            "truncated": truncated,
            "difficult": difficult,
            "xmin": xmin,
            "ymin": ymin,
            "xmax": xmax,
            "ymax": ymax,
        }

        return annotation_info

    except ET.ParseError as error:
        print(f"Error parsing XML file: {error}")
        return None
    except Exception as error:
        print(f"Error reading XML file: {error}")
        return None


def metadat_func(annotation_dir, save_path):
    """doc"""
    main_dataframe = pd.DataFrame()
    list_dataframes = []
    for _, labels_dir, _ in os.walk(annotation_dir, topdown=True):
        for breed_class in labels_dir:
            class_dir = os.path.join(annotation_dir, breed_class)
            class_files = list_files_in_directory(class_dir)
            for file in class_files:
                data_dict = read_xml_annotation(file)
                data_df = pd.DataFrame([data_dict])
                list_dataframes.append(data_df)
    main_df = pd.concat([main_dataframe] + list_dataframes)
    main_df.drop("Unnamed: 0", axis=1)
    main_df.to_csv(save_path)


def list_files_in_directory(directory_path):
    """_summary_

    Parameters
    ----------
    directory_path : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """

    try:
        # Get a list of files and directories in the specified path
        files_and_directories = os.listdir(directory_path)

        # Filter out only the files from the list
        files_list = [
            file
            for fille in files_and_directories
            if os.path.isfile(file := os.path.join(directory_path, fille))
        ]

        return files_list

    except FileNotFoundError:
        print(f"Directory not found: {directory_path}")
    except Exception as error:
        print(f"Error while listing files: {error}")


@hydra.main(config_name="config", config_path="config", version_base="1.2")
def main(cfg: DictConfig):
    """main script"""

    download_data()
    metadat_func(
        annotation_dir=cfg.files.raw.annotation_dir, save_path=cfg.files.raw.meta_data
    )


if __name__ == "__main__":
    main()
