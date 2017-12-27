import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import argparse
import sys

def getfilelist(path):
    filelist = []
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path, i)):#确认是否是文件
            if i.endswith('.jpg') or i.endswith('.png') or i.endswith('.JPEG'):#确认是否是jpg或png
                filelist.append(os.path.join(path, i))
        else:
            filelist+=(getfilelist(os.path.join(path, i)))
    return filelist

def main(_):
    imagelist = getfilelist(FLAGS.image_folder)
    error = []
    for imagepath in imagelist:
        try:
            img = Image.open(imagepath)
        except:
            error.append(imagepath)
    
    file=open('error.txt','w') 
    for line in error:
        file.write(str(line))
        file.write('\n')
    file.close() 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--image_folder',
        type=str,
        default='',
        help='Path to folders of images.'
    )

    FLAGS, unparsed = parser.parse_known_args()
    main([sys.argv[0]] + unparsed)