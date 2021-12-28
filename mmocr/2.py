from mmocr.datasets import build_dataset
from mmcv import Config
from mmocr.apis import init_detector, model_inference
import os
from opencc import OpenCC
import cv2
import numpy as np
cc = OpenCC('s2t')  # convert from Simplified Chinese to Traditional Chinese

path = os.path.join("work_dir", "order_imgs")
print(len(os.listdir(path)))

checkpoint = "./work_dir/sar_r31_parallel_decoder_chineseocr_20210507-b4be8214.pth"
config_file = "configs/textrecog/sar/sar_r31_parallel_decoder_chinese.py"  
model = init_detector(config_file, checkpoint, device="cuda:0")
for index, i in enumerate(os.listdir(path)):
  yolov5_output_dir = os.path.join(path, i)
  ocr_result = ""
  a = os.listdir(yolov5_output_dir)
  a.sort()
  for split_img in a:
    #print(os.path.join(yolov5_output_dir, split_img))
    img = cv2.imread(os.path.join(yolov5_output_dir, split_img))
    #img = np.expand_dims(img, axis = 2)
    img = cv2.resize(img, (128, 128))
    """
    s = []
    t = []
    rotate_array = [90, 0, -90]
    for i in range(3):
      (h, w, d) = img.shape # 讀取圖片大小
      center = (w // 2, h // 2) # 找到圖片中心
      
      # 第一個參數旋轉中心，第二個參數旋轉角度(-順時針/+逆時針)，第三個參數縮放比例
      M = cv2.getRotationMatrix2D(center, rotate_array[i], 1.0)
      
      # 第三個參數變化後的圖片大小
      img = cv2.warpAffine(img, M, (w, h))
      result = model_inference(model, img)
      print(result)
      s.append(result["score"])
      t.append(result["text"])
    print(np.argmax(s))

    converted = cc.convert(t[np.argmax(s)])
    """
    result = model_inference(model, img)
    converted = cc.convert(result["text"])
    if "/" in converted: 
      converted = converted.replace("/", "")
    result["text"] = converted[0]
    ocr_result += result["text"]
  os.rename(yolov5_output_dir, yolov5_output_dir+"_"+ocr_result)
  print(str(index) + "/" + str(len(os.listdir(path))))