"""
doc
"""

import math
import os
import xml.etree.ElementTree as ET

import matplotlib as mpl
import matplotlib.pyplot as plt


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


if os.path.exists(xml_file_path):
    annotation_data = read_xml_annotation(xml_file_path)
    if annotation_data:
        print(annotation_data)
else:
    print("XML file not found.")


def display_detections(
    images, offsets, resizes, detections, classnames, ground_truth_boxes=[]
):
    # scale and offset the detected boxes back to original image coordinates
    boxes = [
        [(x, y, w, h) for _, x, y, w, h, score, klass in detection_list]
        for detection_list in detections
    ]
    boxes = [
        [(x - ofs[1], y - ofs[0], w, h) for x, y, w, h in boxlist]
        for boxlist, ofs in zip(boxes, offsets)
    ]
    boxes = [
        [(x * rsz, y * rsz, w * rsz, h * rsz) for x, y, w, h in boxlist]
        for boxlist, rsz in zip(boxes, resizes)
    ]
    classes = [
        [int(klass) for _, x, y, w, h, score, klass in detection_list]
        for detection_list in detections
    ]
    scores = [
        [score for _, x, y, w, h, score, klass in detection_list]
        for detection_list in detections
    ]
    display_with_boxes(images, boxes, classes, scores, classnames, ground_truth_boxes)


def no_decorations(ax):
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)


def display_with_boxes(
    images, boxes, classes, scores, classnames, ground_truth_boxes=[]
):
    N = len(images)
    sqrtN = int(math.ceil(math.sqrt(N)))
    aspect = sum([im.shape[1] / im.shape[0] for im in images]) / len(
        images
    )  # mean aspect ratio of images
    fig = plt.figure(figsize=(15, 15 / aspect), frameon=False)

    for k in range(N):
        ax = plt.subplot(sqrtN, sqrtN, k + 1)
        no_decorations(ax)
        plt.imshow(images[k])

        if ground_truth_boxes:
            for box in ground_truth_boxes[k]:
                x, y, w, h = (
                    box[0],
                    box[1],
                    box[2] - box[0],
                    box[3] - box[1],
                )  # convert x1 y1 x2 y2 into xywh
                # x, y, w, h = (box[0], box[1], box[2], box[3])
                rect = mpl.patches.Rectangle(
                    (x, y), w, h, linewidth=4, edgecolor="#FFFFFFA0", facecolor="none"
                )
                ax.add_patch(rect)

        for i, (box, klass) in enumerate(zip(boxes[k], classes[k])):
            x, y, w, h = (
                box[0],
                box[1],
                box[2] - box[0],
                box[3] - box[1],
            )  # convert x1 y1 x2 y2 into xywh
            # x, y, w, h = (box[0], box[1], box[2], box[3])
            # label = classnames[klass-1] # predicted classes are 1-based
            label = classnames[klass]
            if scores:
                label += " " + str(int(scores[k][i] * 100)) + "%"
            rect = mpl.patches.Rectangle(
                (x, y), w, h, linewidth=4, edgecolor="#00000080", facecolor="none"
            )
            ax.add_patch(rect)
            rect = mpl.patches.Rectangle(
                (x, y), w, h, linewidth=2, edgecolor="#FFFF00FF", facecolor="none"
            )
            ax.add_patch(rect)
            plt.text(
                x,
                y,
                label,
                size=16,
                ha="left",
                va="top",
                color="#FFFF00FF",
                bbox=dict(
                    boxstyle="round", ec="#00000080", fc="#0000004E", linewidth=3
                ),
            )
            plt.text(
                x,
                y,
                label,
                size=16,
                ha="left",
                va="top",
                color="#FFFF00FF",
                bbox=dict(
                    boxstyle="round", ec="#FFFF00FF", fc="#0000004E", linewidth=1.5
                ),
            )
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.02, hspace=0.02)
    plt.show()

def check_file_type(file_path):
    if os.path.isfile(file_path):
        return "Regular File"
    elif os.path.isdir(file_path):
        return "Directory"
    elif os.path.islink(file_path):
        return "Symbolic Link"
    else:
        return "Other"
