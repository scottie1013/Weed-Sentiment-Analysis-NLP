import json

import pandas

import os

# 指定目录路径
directory = '../'

counts_ = []
# 使用os.walk()函数获取目录下的所有文件

allows = """
01-ALAMEDA
02-ALPINE
03-AMADOR
04-BUTTE
05-CALAVERAS
06-COLUSA
07-CONTRA COSTA
08-DEL NORTE
09-ELDORADO
10-FRESNO
11-GLENN
12-HUMBOLDT
13-IMPERIAL
14-INYO
15-KERN
16-KINGS
17-LAKE
18-LASSEN
19-LOS ANGELES
20- MADERA
21-MARIN
22-MARIPOSA
23-MENDOCINO
24-MERCED
25-MODOC
26-MONO
27-MONTEREY
28-NAPA
29-NEVADA
30-ORANGE
31-PLACER
32-PLUMAS
33-RIVERSIDE
34-SACRAMENTO
35-SAN BENITO
36-SAN BERNARDINO
37-SAN DIEGO
38-SAN FRANCISCO
39-SANJOAQUIN
40-SAN LUIS OBISPO
41-SAN MATEO
42-SANTA BARBARA
43-SANTA CLARA
44-SANTA CRUZ
45-SHASTA
46-SIERRA
47-SISKIYOU
48-SOLANO
49-SONOMA
50-STANISLAUS
51-SUTTER
52-TEHAMA
53-TRINITY
54-TULARE
55-TUOLUMNE
56-VENTURA
57-YOLO
58-YUBA
""".split('\n')

allows_ = [str(i.split("-")[-1]).lower() for i in allows if i.strip() != '']

def get_match(address):
    address = str(address).lower()
    for il in allows_:
        if il in address:
            return il
    return ''


for root, dirs, files in os.walk(directory):
    for file in files:
        # 打印所有文件的路径和文件名
        fullpath = os.path.join(root, file)
        if 'tepm.txt' in fullpath:

            print(fullpath)

            with open(fullpath,'r',encoding='utf-8') as f:
                lines = [json.loads(i.strip()) for i in f.readlines()]
            for line in lines:
                if ', California' in line["地理位置"]:
                #     print(line)
                #     line["行政区"] = get_match(line['地理位置'])
                #     if line["行政区"] == "":
                #         continue
                    counts_.append(line)
pandas.DataFrame(counts_).to_excel("处理结果.xlsx",index=False)
