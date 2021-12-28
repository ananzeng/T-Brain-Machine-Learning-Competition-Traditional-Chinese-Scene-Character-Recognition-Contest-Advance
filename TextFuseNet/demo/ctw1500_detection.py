# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import argparse
import glob
import multiprocessing as mp
import os
import time
import cv2
import tqdm
import numpy as np
import os
from detectron2.config import get_cfg
from detectron2.data.detection_utils import read_image
from detectron2.utils.logger import setup_logger
from predictor import VisualizationDemo
from detectron2.engine import DefaultPredictor
from predictor import VisualizationDemo

# constants
WINDOW_NAME = "COCO detections"


def setup_cfg(args):
    # load config from file and command-line arguments
    cfg = get_cfg()
    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    # Set model
    cfg.MODEL.WEIGHTS = args.weights
    # Set score_threshold for builtin models
    cfg.MODEL.RETINANET.SCORE_THRESH_TEST = args.confidence_threshold
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = args.confidence_threshold
    cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = args.confidence_threshold
    cfg.freeze()
    return cfg


def get_parser():
    parser = argparse.ArgumentParser(description="Detectron2 Demo")
    parser.add_argument(
        "--config-file",
        default="./configs/ocr/ctw1500_101_FPN.yaml",
        metavar="FILE",
        help="path to config file",
    )

    parser.add_argument(
        "--weights",
        default="./out_dir_r101/ctw1500_model/model_ctw_r101.pth",
        metavar="pth",
        help="the model used to inference",
    )

    parser.add_argument(
        "--input",
        default="./input_images/*.jpg",
        nargs="+",
        help="the folder of ctw1500 test images"
    )

    parser.add_argument(
        "--output",
        default="./test_ctw1500/",
        help="A file or directory to save output visualizations. "
        "If not given, will show output in an OpenCV window.",
    )

    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.5,
        help="Minimum score for instance predictions to be shown",
    )
    parser.add_argument(
        "--opts",
        help="Modify config options using the command-line 'KEY VALUE' pairs",
        default=[],
        nargs=argparse.REMAINDER,
    )
    return parser


def compute_polygon_area(points):
    s = 0
    point_num = len(points)
    if(point_num < 3): return 0.0
    for i in range(point_num): 
        s += points[i][1] * (points[i-1][0] - points[(i+1)%point_num][0])
    return abs(s/2.0)
    

def save_result_to_txt(txt_save_path,prediction,polygons):

    file = open(txt_save_path,'w')

    classes = prediction['instances'].pred_classes

    for i in range(len(classes)):
        if classes[i] == 0:
            points = []
            for j in range(0,len(polygons[i][0]),2):
                points.append([polygons[i][0][j],polygons[i][0][j+1]])
            points = np.array(points)
            area = compute_polygon_area(points)

            if area > 70:
                str_out = ''
                for pt in polygons[i][0]:
                     str_out += str(pt)
                     str_out += ','
                file.writelines(str_out+'###')
                file.writelines('\r\n')

    file.close()

def order_points_old(pts):
	rect = np.zeros((4, 2), dtype="float32")
	s = pts.sum(axis=1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
	diff = np.diff(pts, axis=1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
	return rect

if __name__ == "__main__":

    args = get_parser().parse_args()

    cfg = setup_cfg(args)
    detection_demo = VisualizationDemo(cfg)
    predictor = DefaultPredictor(cfg)
    test_images_path = args.input
    output_path = args.output
    Character = ["text","0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
            "a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    start_time_all = time.time()
    img_count = 0
    aaa = 0
    out_dir_img = os.path.join("test_ctw1500", "img")
    out_dir_yolo = os.path.join("test_ctw1500", "yolo")
    if not os.path.isdir(out_dir_img):
        os.mkdir(out_dir_img)
    if not os.path.isdir(out_dir_yolo):
        os.mkdir(out_dir_yolo)
    for i in glob.glob(test_images_path):
        #print(i)
        name = i.split("/")[-1][:-4]
        img_name = os.path.basename(i)
        img_save_path = output_path + img_name.split('.')[0] + '.jpg'
        img = cv2.imread(i)
        img_1 = img.copy()
        start_time = time.time()

        prediction, vis_output, polygons = detection_demo.run_on_image(img)
        outputs = predictor(img)
        #print("outputs", outputs)
        bbox = outputs['instances'].pred_boxes.to("cpu")
        classes = outputs['instances'].pred_classes.to("cpu").numpy()
        mask = outputs['instances'].pred_masks.to("cpu").numpy()
        score = outputs['instances'].scores.to("cpu").numpy()
        for index, i in enumerate(bbox):
            pts = np.array(i, np.int32)
            if classes[index]==0:
                file_mask = 1 * np.array(mask[index]).astype('uint8')
                file_mask_copy = file_mask.copy()
                contours, hierarchy = cv2.findContours(file_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                if len(contours) == 1:
                    order = 0
                else:
                    area_temp = []
                    for i in range(len(contours)):
                        print(name)
                        aaa+=1
                        area1 = cv2.contourArea(contours[i])
                        area_temp.append(area1)
                        print("面積", area1)
            	    print("order", np.argmax(np.array(area_temp)))
            	    order = np.argmax(np.array(area_temp))
            rect = cv2.minAreaRect(contours[order])
            box = cv2.boxPoints(rect)
            box = order_points_old(box)
            box = np.int0(box)
            cv2.rectangle(img, (pts[0], pts[1]), (pts[2], pts[3]), (0, 255, 0), 2)
            for index1, i in enumerate(box):
              cv2.putText(img, str(index1), (np.array(i)[0], np.array(i)[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
            str_format = name+"_"+str(box[1][0])+"_"+str(box[1][1])+"_"+str(box[2][0])+"_"+str(box[2][1])+"_"+str(box[3][0])+"_"+str(box[3][1])+"_"+str(box[0][0])+"_"+str(box[0][1])+"_"+str(score[index])
            print("比賽格式："+str_format)
            cv2.polylines(img=img, pts=[box], isClosed=True, color=(255, 0, 0), thickness=2)
            file_mask_copy = file_mask_copy[pts[1]:pts[3] , pts[0]: pts[2]]

            file_mask_copy1 = np.expand_dims(file_mask_copy, axis=2)
            file_mask_copy2 = np.concatenate((file_mask_copy1, file_mask_copy1, file_mask_copy1), axis=-1)
            det = cv2.multiply(img_1[pts[1]:pts[3] , pts[0]: pts[2]], file_mask_copy2)

            (h, w, d) = det.shape # 讀取圖片大小

            pts2 = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
            pts2 = pts2.astype("float32")
            box = box.astype("float32")
            matrix = cv2.getPerspectiveTransform(box, pts2)
            result = cv2.warpPerspective(img_1, matrix, (w, h)) 
            if det.shape[0] > det.shape[1] and det.shape[0] // det.shape[1] > 2:
              cv2.imwrite(os.path.join("test_ctw1500", "yolo", str_format+".png"), result)    
            else:
              cv2.imwrite(os.path.join("test_ctw1500", "img", str_format+".png"), result) 

        img_save_path_my = output_path + img_name.split('.')[0] + '_my.jpg'
        cv2.imwrite(img_save_path_my, img)

        #txt_save_path = output_path + 'res_' + img_name.split('.')[0] + '.txt'
        #save_result_to_txt(txt_save_path,prediction,polygons)

        print("Time: {:.2f} s / img".format(time.time() - start_time))
        vis_output.save(img_save_path)
        img_count += 1
    print("Average Time: {:.2f} s /img".format((time.time() - start_time_all) / img_count))
    print("結束!")
    print("yolo資料夾有", len(os.listdir(os.path.join("test_ctw1500", "yolo"))))
    print("img資料夾有", len(os.listdir(os.path.join("test_ctw1500", "img"))))
