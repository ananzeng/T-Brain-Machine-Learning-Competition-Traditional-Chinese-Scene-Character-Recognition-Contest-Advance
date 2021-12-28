# T-Brain-Machine-Learning-Competition-Traditional-Chinese-Scene-Character-Recognition-Contest-Advance
繁體中文場景文字辨識競賽－高階賽：複雜街景之文字定位與辨識

|  隊伍名稱 | Private leaderboard成績  | Private leaderboard名次  |
| ------------ | ------------ | ------------ |
|  TEAM_135 |  0.555602 |  22 |


------------



環境搭建請參考  
[mmocr](https://github.com/ananzeng/T-Brain-Machine-Learning-Competition-Traditional-Chinese-Scene-Character-Recognition-Contest-Advance/blob/main/MMOCR_Tutorial_env_install_train_dataset.ipynb "mmocr")  
[TextFuseNet](https://github.com/ananzeng/T-Brain-Machine-Learning-Competition-Traditional-Chinese-Scene-Character-Recognition-Contest-Advance/blob/main/TextFuseNet.ipynb "TextFuseNet")

------------


新增以下資料夾  
mmocr/work_dir  
mmocr/work_dir/exp  
mmocr/work_dir/ezzocr  
mmocr/work_dir/img  
mmocr/work_dir/order_imgs  
mmocr/work_dir/outputs1  
mmocr/data/chineseocr/labels  
yolov5/data/images  

------------


下載SAR預訓練[模型](https://download.openmmlab.com/mmocr/textrecog/sar/sar_r31_parallel_decoder_chineseocr_20210507-b4be8214.pth "模型")至mmocr/work_dir  
下載[last.pt](https://drive.google.com/file/d/1Aq32QROGIP8976485F_xF49RPA1j40Cl/view?usp=sharing "last.pt")複製至 yolov5/  
下載[文字檔](https://drive.google.com/file/d/1xRzidgcAIz29ufCLLvbdV5JEtSA9VqsS/view?usp=sharing "文字檔")至mmocr/data/chineseocr/labels/  

------------


**步驟一** 先至TextFuseNet資料夾產生detection結果 詳細可[參考](https://github.com/ananzeng/T-Brain-Machine-Learning-Competition-Traditional-Chinese-Scene-Character-Recognition-Contest-Advance/blob/main/TextFuseNet/README.md "參考")  
**步驟二** 複製TextFuseNet/test_ctw1500/img  至 mmocr/work_dir/ 並在mmocr資料夾內執行 1.py  
**步驟三** 複製TextFuseNet/test_ctw1500/yolo/ 至 yolov5/data/images 產生直式文字字元級分割結果 詳細可[參考](https://github.com/ananzeng/T-Brain-Machine-Learning-Competition-Traditional-Chinese-Scene-Character-Recognition-Contest-Advance/blob/main/yolov5/README.md "參考")  
**步驟四** 將產生的order_imgs 資料夾複製到 mmocr/work_dir/ 並在mmocr資料夾內執行 2.py  
**步驟五** 執行 3.py  
至此步驟所有的字元辨識已結束  
**步驟六** 執行 1_csv.py && 2_csv.py && 3_csv.py  
**步驟七** 因輸出有逗點沒消除因此csv檔輸出的逗號分隔檔有亂碼以及未分段的狀況，競賽期間沒發現，因此傳送email給比賽方查詢哪裡的問題，得知問題後手動刪除有問題的地方。 最終輸出為手動將output.csv, output1.csv, output2.csv 結合  



## mmocr/work_dir 資料夾介紹:  
**mmocr/work_dir/img**  
為TextFuseNet產生的Text Detection  
可使用以下指令複製  
```python
cp -r TextFuseNet/test_ctw1500/img  mmocr/work_dir/  
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



