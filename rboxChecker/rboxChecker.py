'''
该py用于检查标定的rbox坐标是否与同名图片对应
用法：在该py文件所在目录下新建data文件夹，把要检查的图片和记录rbox坐标的txt放在data目录下。注意。txt要和image同名
'''
import numpy as np

import argparse
import random
import sys
import cv2
import os

#通过该函数遍历文件夹下的jpg等
def getfilelist(path):
    filelist = []
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path, i)):#确认是否是文件
            if i.endswith('.jpg') or i.endswith('.png') or  i.endswith('.jpeg'):#确认是否是jpg或png
                filelist.append(os.path.join(path, i))
        else:
            filelist+=(getfilelist(os.path.join(path, i)))
    return filelist

def draw_illu(illu, rst):
    '''
        根据坐标在图上画框并保存
        输入：
            illu：图片
            rst：点坐标字符串组成的list，注意，list中的数据格式如下：
                ["67,409,368,409,368,512,67,512,92\n",
                "69,507,355,507,355,612,69,612,60\n"
                ......
                每一行前8位为RBOX坐标，最后一位为框内内容（目前为无意义的随机数）
        返回：画好框的图
    '''
    for n in rst:
        t = list(map(int, n.replace('\n', '').split(',')))#将字符串转化为list并消除换行符
        d = np.array([t[0], t[1], t[2], t[3], t[4],
                      t[5], t[6], t[7]], dtype='int32')
        d = d.reshape(-1, 2)
        cv2.polylines(illu, [d], isClosed=True, color=(255, 255, 0))
    return illu

def rboxChecker(path):
    #建立结果保存路径
    resPath = os.path.join(path, 'rst')
    if not os.path.exists(resPath):
        os.makedirs(resPath)
        
    imgList = getfilelist(path)

    for imgPath in imgList:
        img = cv2.imread(imgPath)
        imgName = os.path.basename(imgPath).split('.')[0]#获得图片基本名（不含格式）
        #获得图片对应txt的路径并读取
        dirName = os.path.dirname(imgPath)
        txtName = imgName + '.txt'
        txtPath = os.path.join(dirName, txtName)

        outPath = os.path.join(resPath, os.path.basename(imgPath))

        #读取txt中RBOX信息
        f = open(txtPath)
        lines = f.readlines()
        #画框并保存
        cv2.imwrite(outPath, draw_illu(img.copy(), lines))
        f.close()

def main(_):
    rboxChecker(FLAGS.path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', 
                        type=str, 
                        help='The path of data',
                        default='data')

    FLAGS, unparsed = parser.parse_known_args()
    main([sys.argv[0]] + unparsed)
