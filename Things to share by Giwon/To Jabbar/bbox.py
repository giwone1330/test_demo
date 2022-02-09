import json
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
from tqdm import tqdm


def drawbbox_dir(dir, thickness=2, mode="withlabel"):
    pbar = tqdm(total=len(os.listdir(dir)))
    for myfile in os.listdir(dir):
        file_name, file_ext = os.path.splitext(myfile)
        if file_ext == ".json":  # myfile = filename.ext
            name_dir = dir + "/" + file_name
            drawbbox(name_dir, thickness=thickness, mode=mode)
        pbar.update(1)
    pbar.close()


def drawbbox(name_dir, thickness=2, mode="withlabel"):
    font = cv2.FONT_HERSHEY_SIMPLEX
    json_dir = name_dir + ".json"
    png_dir = name_dir + ".png"
    dir, name_png = os.path.split(png_dir)
    image = cv2.imread(png_dir)
    json_file = open(json_dir)
    json_data = json.load(json_file)  # loads json as dictionary
    shapes = json_data["shapes"]  # type(shapes) = list of all the objects
    colordict = {}
    color = (0, 0, 255)
    for obj in shapes:  # obj is dictionary of obj annotation information

        obj_label = obj["label"]  # class name
        obj_pointarray = np.array(obj["points"])  # (N, 2) numpy array

        if obj_label in colordict:
            color = colordict[obj_label]
        else:
            color = tuple(np.random.random(size=3) * 256)
            colordict[obj_label] = color

        max = np.amax(obj_pointarray, axis=0)
        min = np.amin(obj_pointarray, axis=0)
        max_int = max.astype(int)
        min_int = min.astype(int)
        cv2.rectangle(image, min_int, max_int, color, thickness)

        if mode == "withlabel":
            text_size, _ = cv2.getTextSize(obj_label, font, 1, 2)
            text_w, text_h = text_size
            cv2.rectangle(image, (max_int[0], max_int[1]),
                          (max_int[0]+text_w, max_int[1]-text_h), (0, 0, 0), -1)
            cv2.putText(image, obj_label,
                        (max_int[0], max_int[1]), font, 1, color, 1)

    outpath = 'bbox/'+dir
    os.makedirs(outpath, exist_ok=True)
    outname = outpath + "/" + name_png
    cv2.imwrite(outname, image)
