import facial_features
import time
import os
from PIL import Image
import numpy as np 
import matplotlib.pyplot as plt
import scipy
import LSB

def main():

    picture, imgPath = facial_features.select_image()
    chosenFeature, points_list, pixels_list = facial_features.do_facial_feature_recog(picture, imgPath)

    print("The important information: \n Picture chosen: {} \n Chosen feature: {} \n Points of chosen feature: {}".format(picture, chosenFeature, points_list))
    time.sleep(2)
    facial_features.kill_example_pictures()
    LSB.encode(picture,imgPath,chosenFeature,points_list,pixels_list)
    imgPath = "/home/pranmar123/Multi-Facial-Steganography/facial_recog/dataset/save.png"
    print("Decoded: {}".format(LSB.decode(picture,imgPath,chosenFeature,points_list, pixels_list)))

main()
