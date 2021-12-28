import numpy as np
import pandas as pd
import os
import cv2
import matplotlib.pyplot as plt
paths = "./runs/detect/exp2/labels"  # /labels
paths_img = "./data/images"
paths_save_img = "./runs/detect/exp2/order_imgs"
for lable in os.listdir(paths):
    path = os.path.join(paths, lable)
    img_name = lable[:-4]
    print(img_name)
    if os.path.exists(paths_save_img):
        pass
    else:
        os.makedirs(paths_save_img)
    words = []
    with open(path, "r") as f:
        for line in f.readlines():
            word = line.split(' ')
            words.append(float(word[1]) * float(word[2]))  # float(word[1])

        # 排序
        words_order = np.argsort(words)
        words_new = np.zeros(len(words_order))
        tmp = 0
        for i in words_order:
            words_new[i] = tmp
            tmp += 1
        print(words_order)
        print(words)
        print(words_new)
        count = 0
    with open(path, "r") as f:
        for line in f.readlines():
            img = cv2.imread(os.path.join(paths_img, img_name + ".png"))
            # ori w h
            ori_w = img.shape[1]
            ori_h = img.shape[0]
            # crop
            word = line.split(' ')
            w = round(float(word[3]) * ori_w)
            h = round(float(word[4].replace('\n', '')) * ori_h)
            x = round((float(word[1]) - float(word[3]) / 2) * ori_w)
            y = round((float(word[2]) - float(word[4].replace('\n', '')) / 2) * ori_h)
            crop_img = img[y:y+h, x:x+w]

            # Path
            each_img_path = os.path.join(paths_save_img, img_name)
            if os.path.exists(each_img_path):
                pass
            else:
                os.makedirs(each_img_path)         
            number = str(words_new[count])
            number = number[:-2]
            cv2.imwrite(os.path.join(each_img_path, number + ".png"), crop_img)
            count += 1
            # cv2.imshow("cropped", crop_img)
            # cv2.waitKey(0)