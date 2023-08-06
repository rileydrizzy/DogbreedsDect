"""
doc
"""

import os
import xml.etree.ElementTree as ET
from pathlib import Path
import mlflow

def read_xml_annotation(xml_file_path):
    """
    doc
    """
    try:
        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Extract relevant information from the XML
        folder = root.find('folder').text
        filename = root.find('filename').text
        database = root.find('source/database').text
        width = int(root.find('size/width').text)
        height = int(root.find('size/height').text)
        depth = int(root.find('size/depth').text)
        object_name = root.find('object/name').text
        pose = root.find('object/pose').text
        truncated = int(root.find('object/truncated').text)
        difficult = int(root.find('object/difficult').text)
        xmin = int(root.find('object/bndbox/xmin').text)
        ymin = int(root.find('object/bndbox/ymin').text)
        xmax = int(root.find('object/bndbox/xmax').text)
        ymax = int(root.find('object/bndbox/ymax').text)

        # Create a dictionary to hold the extracted information
        annotation_info = {
            'folder': folder,
            'filename': filename,
            'database': database,
            'width': width,
            'height': height,
            'depth': depth,
            'object_name': object_name,
            'pose': pose,
            'truncated': truncated,
            'difficult': difficult,
            'xmin': xmin,
            'ymin': ymin,
            'xmax': xmax,
            'ymax': ymax
        }

        return annotation_info

    except ET.ParseError as error:
        print(f"Error parsing XML file: {error}")
        return None
    except Exception as error:
        print(f"Error reading XML file: {error}")
        return None



def read(list_file_path):
     ran = len(list_file_path)
     
if os.path.exists(xml_file_path):
        annotation_data = read_xml_annotation(xml_file_path)
        if annotation_data:
            print(annotation_data)
else:
        print("XML file not found.")



