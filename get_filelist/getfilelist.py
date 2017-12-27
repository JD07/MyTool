# -*- coding: utf-8 -*-
# 遍历指定路径下的所有jpg和png图片
import os
import argparse
import sys
from PIL import Image
import re

FLAGS = None

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

def ChangeImagePx(filelist, dst_w, dst_h, savepath):
    '''
    改变图像的分辨率，并按照指定的名称保存图像
    输入：
        filelist：含有图像路径的list
        dst_w,dst_h：目标图像的宽和高
        savepath:结果保存路径
    输出：    
    '''
    imgName = "img_"
    if not os.path.exists(savepath):
        os.makedirs(savepath)
        
    for i,filepath in enumerate(filelist):
        im=Image.open(filepath)
        out = im.resize((dst_w, dst_h),Image.ANTIALIAS) 
        outName = imgName + str(i+1) + ".JPEG"
        outPath = os.path.join(savepath, outName)
        out.save(outPath) 

def main(_):
    path = FLAGS.file_dir
    #获取文件夹下所有路径
    filelist = getfilelist(path)

    ChangeImagePx(filelist, FLAGS.dst_w, FLAGS.dst_h, FLAGS.savepath)
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
      '--filelist_dir',
      type=str,
      default='',
      help="Path to files"
    )
    parser.add_argument(
      '--dst_w',
      type=int,
      default=1080,
      help="width"
    )
    parser.add_argument(
      '--dst_h',
      type=int,
      default=1920,
      help="height"
    )
    parser.add_argument(
      '--savepath',
      type=str,
      default="result",
      help="where to save the result"
    )

    FLAGS, unparsed = parser.parse_known_args()
    main([sys.argv[0]] + unparsed)

  