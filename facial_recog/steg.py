import facial_features
import time
import os
from PIL import Image
import numpy as np 
import matplotlib.pyplot as plt
import scipy
import LSB
import shutil


def main():
    choice = 0
    while choice != '1' and choice != '2': 
        choice = input("Choose 1 to encode or 2 to decode: ")

    if choice == '1':
        menuEncode()
    else:
        menuDecode()

def menuEncode():
    picture, imgPath = facial_features.select_image()
    chosenFeature, pointsList, pixelsList = facial_features.do_facial_feature_recog(picture, imgPath)
    print("The important information: \n Picture chosen: {} \n Chosen feature: {} ".format(picture, chosenFeature))
    msg = str(input("Enter message to encode: "))
    try:
        LSB.encodeMessage(picture, imgPath, pointsList, pixelsList, msg)
    except ValueError:
        print("Message is too large to be encoded.")
    


def menuDecode():
    #picture = str(input("Enter the image with extension (ex: example.png): "))
    print("This is the current path: ", os.getcwd())
    #imgPath = str(input("Enter the path to the image: "))
    #facialFeature = str(input("Enter the facial feature (eyes, mouth, nose): "))
    #we are passing 1 in to the facial_feature_recog function to tell that function to decode
    picture = '1.png'
    imgPath = '/home/pranmar123/Multi-Facial-Steganography/facial_recog/dataset/1.png'
    #toGetPoints is there so that we get THE ORIGINAL points of the PNG instead of the modified points.
    toGetPoints = '/home/pranmar123/Multi-Facial-Steganography/facial_recog/original_dataset/1.png'
    facialFeature = 'mouth'
    pointsList = facial_features.do_facial_feature_recog(picture, toGetPoints, 1, facialFeature)
    pointsList = pointsList[1]
    msg = LSB.decodeMessage(picture, imgPath, pointsList)
    print(msg)
    #after decoding, replace the encoded image with the original_dataset copy
    shutil.copyfile(toGetPoints, imgPath)  



if __name__ == '__main__':
    main()
