'''
该文件主要用于将原始数据集分割为train和test两部分。注意该py文件的工作要求是所有的jpg文件和与其同名的label文件在同一个目录下。
而该程序会将图像分成两部分另存到对应的文件夹下，并在两个文件夹下建立对应的总label文件。
该py文件是针对EAST数据集的分割编写的，通用性不强，需要根据实际情况进行修改
'''
import argparse
import random
import shutil
import sys
import os

FLAGS = None

def getfilelist(path, suffix = '.jpg'):
    #迭代获取当前路径下所有的jpg文件或txt文件，并返回其路径
    filelist = []
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path, i)):#确认是否是文件
            if i.endswith(suffix):#确认后缀
                filelist.append(os.path.join(path, i))
        else:
            filelist+=(getfilelist(os.path.join(path, i)))
    return filelist

def datasetDivisionSaver(imageList, labelList, savePath):
    '''
    按照imageList读取图片并转存到savePath下去。
    同时会按照labelList读取txt文本，并将所有txt文本的内容按照“文件名 内容”的格式保存在savePath下的一个txt文本中
    输入：
        fileList:由图片绝对路径组成的list
        labelList:由图片对应的标签文件绝对路径组成的list
        savePath:图片转存的路径
    '''
    resultList = []
    lenc = len(imageList)
    assert len(labelList) == lenc
    #拷贝文件并读取标签文件内容
    for i in range(lenc):
        fileName = os.path.basename(imageList[i])#获取图片名称
        f = open(labelList[i])#打开对应的标签文件
        label = f.readline()
        result = [fileName, label]
        resultList.append(result)
        f.close()
        copyPath = os.path.join(savePath, fileName)
        shutil.copy(imageList[i], copyPath)
    #将标签文件内容保存
    txtPath = os.path.join(savePath, 'sample.txt')
    f = open(txtPath, "w")
    for result in resultList:
        line = ' '.join(result)
        f.write(line)
        #f.write('\n')
    f.close()

def datasetDivision(fileListDir, ratio):
    '''
        对指定路径下的数据集按照指定的比例分为train和test两部分，该数据及由jpg图像以及与图像同名的txt格式label文件组成
        输入：
            fileListDir：需要分割的数据集路径
            ratio：分割比例
        输出：
    '''
    #建立结果保存路径
    trainPath = os.path.join(fileListDir, 'Train')
    testPath = os.path.join(fileListDir, 'Test')
    if not os.path.exists(trainPath):#如果不存在，则创立文件夹
        os.mkdir(trainPath)
    if not os.path.exists(testPath):#如果不存在，则创立文件夹
        os.mkdir(testPath)    

    #获得路径列表
    imageList = getfilelist(fileListDir)
    labelList = getfilelist(fileListDir, '.txt')

    #检查image和label是否顺序对应
    lenc = len(imageList)
    for i in range(lenc):
        image = os.path.basename(imageList[i]).split('.')[0]
        label = os.path.basename(labelList[i]).split('.')[0]
        if(image!=label):
            print("check fail")   
    
    #随机分割为train和test
    index = list(range(lenc))
    random.shuffle(index)
    gate = int(lenc * ratio)
    testImageList = [imageList[i] for i in index[0 : gate]]
    testLabelList = [labelList[i] for i in index[0 : gate]]
    trainImageList = [imageList[i] for i in index[gate : lenc]]
    trainLabelList = [labelList[i] for i in index[gate : lenc]]

    #保存风格结果
    datasetDivisionSaver(testImageList, testLabelList, testPath)
    datasetDivisionSaver(trainImageList, trainLabelList, trainPath)   

def main(_):
    datasetDivision(FLAGS.fileListDir, FLAGS.ratio)

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
      '--fileListDir',
      type=str,
      default='',
      help="Path to files"
    )
    parser.add_argument(
      '--ratio',
      type=int,
      default=0.2,
      help="the ratio of test"
    )

    FLAGS, unparsed = parser.parse_known_args()
    main([sys.argv[0]] + unparsed)  