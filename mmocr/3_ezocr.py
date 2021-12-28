import os
import easyocr
import shutil
reader = easyocr.Reader(['ch_tra','en'])
path = os.path.join("work_dir", "exp")
a = os.listdir(path)
a.sort()
for name in a:
  ocr_text = ""
  img_path = os.path.join(path, name)
  print(name)
  bounds = reader.readtext(img_path)
  print(bounds)
  if len(bounds) != 0:
    for i in range(len(bounds)):
      if bounds[i][2] < 0.1 or "/" in str(bounds[i][1]):
        print("no")
      else:
      #print(i)  
        print("str：", bounds[i][1])
        print("seore：", bounds[i][2])     
        ocr_text+=str(bounds[i][1])
    text = name[:-4] +"_"+ ocr_text +".png"
    if len(ocr_text)>0:
      shutil.copyfile(os.path.join(path, name), os.path.join("work_dir", "ezzocr", text)) 