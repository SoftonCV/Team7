import pickle
import os
import glob
import cv2
import numpy as np
from time import time

QUERY_SET_ANN_PATH = "gt_corresps.pkl"
DB_FOLDER = "BBDD" # 2GB of RAM to load
QS_FOLDER = "qsd1_w1"

def load_images(db_path, ext="jpg"):
    """ Load images from path """
    print("Loading DB images...")
    t0 = time()
    
    file_list = glob.glob(os.path.join(db_path, "*."+ext))
    file_list.sort(key= lambda x: int(x.split(".")[-2][-5:]))
    img_list = [cv2.imread(img_p)[...,::-1] for img_p in file_list]
    
    print("Done in", time()-t0, " sec")
    return img_list

def load_db(db_path, load_mask_imgs=False):
    """ Load DB images """
    img_list = load_images(db_path)
    if load_mask_imgs:
        mask_list = load_images(db_path, "png")
    else:
        mask_list = None
    labels = list(range(len(img_list)))
    return img_list, labels, mask_list

def load_annotations(anno_path):
    """ Load annotations from path for query set. List of groundtruths [7, 2, 3, ..., 10] """
    if os.path.exists(anno_path):
        fd = open(anno_path, "rb")
        annotations = pickle.load(fd)
        return np.array(annotations).reshape(-1)
    else:
        return None

def load_query_set(db_path):
    """ Load query set db and annotations """ 
    img_list = load_images(db_path)
    labels = load_annotations(os.path.join(db_path, QUERY_SET_ANN_PATH))
    return img_list, labels

def to_pkl(results, result_path):
    """ Write results to pkl file in result_path """
    pass