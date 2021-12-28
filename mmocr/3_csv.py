import csv
import cv2
import os
import re
output_dir = os.path.join("work_dir", "ezzocr")
with open('output3.csv', 'w',encoding='utf-8') as csvfile:
  a = os.listdir(output_dir)
  a.sort()
  for i in a:
    #print(os.path.join(output_dir, i))
    str_name = i.replace("_", ",")
    str_name_array = str_name.split(",")
    img_name = str_name_array[0]+"_"+str_name_array[1]
    text = str(str_name_array[11][:-4])
    text = text.replace(" ", "")
    #print(text)
    if text == "":
      text = "###"
    if text == " ":
      text = "###"
    if text == "  ":
      text = "###"
    if str_name_array[2][0] == "-" or str_name_array[3][0] == "-" or str_name_array[4][0] == "-" or str_name_array[5][0] == "-" or str_name_array[6][0] == "-" or str_name_array[7][0] == "-" or str_name_array[8][0] == "-" or str_name_array[9][0] == "-":
      print(i)
      continue 
    if [str_name_array[2], str_name_array[3]] == [str_name_array[4], str_name_array[5]] or [str_name_array[2], str_name_array[3]] == [str_name_array[6], str_name_array[7]] or [str_name_array[2], str_name_array[3]] == [str_name_array[8], str_name_array[9]]:
      print(os.path.join(output_dir, i))
      continue
    if [str_name_array[4], str_name_array[5]] == [str_name_array[6], str_name_array[7]] or [str_name_array[4], str_name_array[5]] == [str_name_array[8], str_name_array[9]] or [str_name_array[4], str_name_array[5]] == [str_name_array[2], str_name_array[3]]:
      print(os.path.join(output_dir, i))
      continue
    if [str_name_array[6], str_name_array[7]] == [str_name_array[8], str_name_array[9]] or [str_name_array[6], str_name_array[7]] == [str_name_array[2], str_name_array[3]] or [str_name_array[6], str_name_array[7]] == [str_name_array[4], str_name_array[5]]:
      print(os.path.join(output_dir, i))
      continue
    if [str_name_array[8], str_name_array[9]] == [str_name_array[2], str_name_array[3]] or [str_name_array[8], str_name_array[9]] == [str_name_array[4], str_name_array[5]] or [str_name_array[8], str_name_array[9]] == [str_name_array[6], str_name_array[7]]:
      print(os.path.join(output_dir, i))
      continue
    writer = csv.writer(csvfile)
    remove_nota = u'[’·°–!"#$%&\'()*+,-./:;<=>?@，。?★、…【】（）《》？“”‘’！[\\]^_`{|}~]+'
    print(re.sub(remove_nota, '', text))
    if text == "":
      print("yes")
      text = "###"
    writer.writerow([img_name, str_name_array[4], str_name_array[5], str_name_array[6], str_name_array[7], str_name_array[8],
                  str_name_array[9], str_name_array[2], str_name_array[3], text])