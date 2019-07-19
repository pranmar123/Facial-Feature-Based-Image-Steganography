import facial_features
import time
import os
import math
import numpy as numpy
from utils import *
from scipy import fftpack
from PIL import Image
from huffman import HuffmanTree




def main():

    picture, img_path = facial_features.select_image()
    chosen_feature, points = facial_features.do_facial_feature_recog(picture, img_path)

    print("The important information: \n Picture chosen: {} \n Chosen feature: {} \n Points of chosen feature: {}".format(picture, chosen_feature, points))
    time.sleep(2)
    facial_features.kill_example_pictures()
    steg(picture,img_path,chosen_feature,points)

def steg(picture,img_path,chosen_feature,points):
    print(pylab.rcParams[picture])

main()
