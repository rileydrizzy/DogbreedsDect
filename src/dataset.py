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


def list_files_in_directory(directory_path):

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
        return []
    except Exception as e:
        print(f"Error while listing files: {e}")
        return []


def main(dir, main_dataframe):
    list_dataframes = []
    for main_dir, labels_dir, filenames in os.walk(dir, topdown=True):
        for num, _class in enumerate(labels_dir):
            # print(_class)
            class_dir = os.path.join(dir, _class)
            class_files = list_files_in_directory(class_dir)
            # print(class_files[:5])
            for file in class_files:
                data = read_xml_annotation(file)
                data_df = pd.DataFrame([data])
                list_dataframes.append(data_df)
    return list_dataframes


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
