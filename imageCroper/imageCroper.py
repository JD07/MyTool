'''
该py程序用于将图片按照指定RBOX坐标进行切割并保存，主要是为了配合ArtQun——project1中的CRNN训练使用
该py要求txt文件中每一行只包含了RBOX框左上角和右下角的坐标，且坐标为相对坐标而不是绝对坐标
所以如果用作他用，请酌情修改。具体要求可见附例
'''
from PIL import Image

import argparse
import shutil  
import sys
import os

FLAGS = None

def imageCroper(imgPath, txtPath):
    '''
        读取imgPath对应的图片和txtPath对应的txt文件。
        并按照txt文件记录的坐标对图片进行切割
        输入：
            imgPath：要切割的图片的路径
            txtPath：记录了RBOX坐标信息的txt文本路径
    '''
    #获得文件名（不含。jpg等）
    basename = os.path.basename(imgPath).split('.')[0]
    #建立结果保存路径
    dstPath = os.path.join(os.path.dirname(imgPath), basename)
    if not os.path.exists(dstPath):#如果不存在，则创立文件夹
        os.mkdir(dstPath)
    else:#已经存在，则删除文件夹，重新建立
        shutil.rmtree(dstPath)
        os.mkdir(dstPath)

    img = Image.open(imgPath)
    img_w, img_h = img.size
    offset = min(img_w, img_h)//100

    #读取RBOX框位置信息，并对图片进行切割
    txtFile = open(txtPath, 'r')
    lines = txtFile.readlines()
    lenc = len(lines)
    for i in range(1, lenc):
        #将一行末尾的'/n'去掉，并将str转化为float
        line = lines[i]
        line = list(map(float, line.replace('\n', '').split(' ')))
        #左上角
        x1 = int(line[0]*img_w) - offset
        y1 = int(line[1]*img_h) - offset
        #右下角
        x2 = int(line[2]*img_w) + offset
        y2 = int(line[3]*img_h) + offset
        box = (x1, y1, x2, y2)
        dst_img = img.crop(box).resize((100, 30))
        index = str(i) + '.jpg'
        savePath = os.path.join(dstPath, index)
        dst_img.save(savePath)    

def main(_):
    imageCroper(FLAGS.imgPath, FLAGS.txtPath)

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
      '--imgPath',
      type=str,
      default='test.jpg',
      help="Path to the img"
    )
    parser.add_argument(
      '--txtPath',
      type=str,
      default='test.txt',
      help="Path to the txt"
    )

    FLAGS, unparsed = parser.parse_known_args()
    main([sys.argv[0]] + unparsed)  