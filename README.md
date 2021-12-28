# T-Brain-Machine-Learning-Competition-Traditional-Chinese-Scene-Character-Recognition-Contest-Advance
繁體中文場景文字辨識競賽－高階賽：複雜街景之文字定位與辨識
步驟一 先至TextFuseNet資料夾產生detection結果
主要的資料夾位於mmocr/work_dir
下載SAR預訓練[模型](https://download.openmmlab.com/mmocr/textrecog/sar/sar_r31_parallel_decoder_chineseocr_20210507-b4be8214.pth "模型")至mmocr/work_dir
## 資料夾介紹:
**mmocr/work_dir/img**
為TextFuseNet產生的Text Detection
可使用以下指令複製
```python
cp -r /TextFuseNet/test_ctw1500/img/  mmocr/work_dir/
```

------------


**mmocr/work_dir/exp**
為1.py 產生的SAR模型難以分辨的檔案

------------


**mmocr/work_dir/ezzocr**
將mmocr/work_dir/exp的模型交由easyocr辨識

------------


**mmocr/work_dir/order_imgs**
為yolov5產生的字元級分割
可使用以下指令複製
```python
cp -r /yolov5/runs/detect/exp2/order_imgs   mmocr/work_dir/
```

------------


**mmocr/work_dir/outputs1**
為1.py產生的SAR預測結果

------------


## 程式介紹:
**1.py**
輸入: TextFuseNet產生的Text Detection images
輸出: SAR模型的預測結果位於 work_dir/outputs1
輸出: SAR模型難以辨識的結果位於 work_dir/exp

------------


**2.py**
輸入: yolov5產生的Text Detection 字元級輸出 位於 work_dir/order_imgs
輸出: SAR模型的預測結果位於 work_dir/order_imgs(檔名有做改動增加的就是SAR的預測輸出)

------------


**3_ezocr.py**
輸入: 為1.py 產生的SAR模型難以分辨的檔案 位於 work_dir/exp
輸出: easyocr產生的預測字串 位於 work_dir/ezzocr

------------


**1_csv.py**
輸入: SAR模型的預測結果位於 work_dir/outputs1
輸出: output.csv

------------


**2_csv.py**
輸入: SAR模型的預測結果位於 work_dir/order_imgs(檔名有做改動增加的就是SAR的預測輸出)
輸出: output2.csv

------------


**3_csv.py**
輸入: easyocr產生的預測字串 位於 work_dir/ezzocr
輸出: output3.csv

------------

## csv介紹(重要!):
因輸出有逗點沒消除因此csv檔輸出的逗號分隔檔有亂碼以及未分段的狀況，競賽期間沒發現，因此傳送email給比賽方查詢哪裡的問題，得知問題後手動刪除有問題的地方。
最終輸出為手動將output.csv, output1.csv, output2.csv 結合



