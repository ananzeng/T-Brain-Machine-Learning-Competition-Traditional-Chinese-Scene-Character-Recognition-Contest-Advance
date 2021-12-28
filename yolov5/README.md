在yolov5路徑開啟CMD

CMD執行 python detect.py --weights last.pt --save-txt

之後將 try.py 的路徑改成 yolo生成的 exp (要改的有 paths, paths_save_img)

執行完後即可生成照順序排的個別中文單字

下載[last.pt](https://drive.google.com/file/d/1Aq32QROGIP8976485F_xF49RPA1j40Cl/view?usp=sharing "last.pt")複製至 yolov5資料夾下

輸入圖片放置在yolov5\data\images 內

產生的字元級分割會在yolov5\runs\detect\exp2\order_imgs 內