import torch, torchvision
print(torch.__version__, torch.cuda.is_available())
import mmdet
print(mmdet.__version__)
import mmcv
print(mmcv.__version__)
import mmocr
print(mmocr.__version__)
from mmocr.apis import init_detector, model_inference
import os
from opencc import OpenCC
import cv2
from mmocr.datasets import build_dataset
from mmcv import Config
import shutil
import numpy as np

cc = OpenCC('s2t')  # convert from Simplified Chinese to Traditional Chinese

path = os.path.join("work_dir", "img")
print(len(os.listdir(path)))
out_dir = os.path.join("work_dir", "outputs1")
if not os.path.isdir(out_dir):
  os.mkdir(out_dir)
checkpoint = "./work_dir/sar_r31_parallel_decoder_chineseocr_20210507-b4be8214.pth"
config_file = "configs/textrecog/sar/sar_r31_parallel_decoder_chinese.py"  
#config_file = "configs/textrecog/sar/testdata.py"
model = init_detector(config_file, checkpoint, device="cuda:0")
for index, i in enumerate(os.listdir(path)):
  img = os.path.join(path, i)
  image = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
  image = np.expand_dims(image, axis = 2)
  #print(image.shape)
  area = image.shape[0]*image.shape[1]
  out_file = os.path.join(out_dir, i)
  if float(img.split("_")[-1][:-4]) < 0.2 or area < 300:
    converted = "###"
    if model.cfg.data.test['type'] == 'MultiRotateAugOCR':
        model.cfg.data.test.pipeline = model.cfg.data.test['datasets'][0].pipeline
    result = model_inference(model, image)  
    result["text"] = converted  
  else:
    if model.cfg.data.test['type'] == 'MultiRotateAugOCR':
        model.cfg.data.test.pipeline = model.cfg.data.test['datasets'][0].pipeline
    result = model_inference(model, image)
    #print(f'result: {result}')
    #print(result["score"])
    #if result["score"] < 0.55:
    #  shutil.copyfile(os.path.join(path, i), os.path.join("work_dir", "exp", i))
    #  continue
    converted = cc.convert(result["text"])
    print(converted)
    if "/" in converted: 
      converted = converted.replace("/", "")
    
    result["text"] = converted
  out_file = out_file[:-4] + "_" + str(converted) + ".png"
  if result["score"] < 0.55:
    #print("糟糕")
    shutil.copyfile(os.path.join(path, i), os.path.join("work_dir", "exp", i))
    continue
  img = model.show_result(img, result, out_file=out_file, show=False)
  #print(str(index) + "/" + str(len(os.listdir(path))), "out_file", out_file)
  mmcv.imwrite(img, out_file)
print("最後數量：", len(os.listdir(out_dir)))
print("最後數量：", len(os.listdir(os.path.join("work_dir", "exp"))))