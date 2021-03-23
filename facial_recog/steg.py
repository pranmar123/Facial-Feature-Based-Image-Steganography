import facial_features
import time
import os
from PIL import Image
import numpy as np 
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
    try:
        LSB.encode(picture,imgPath,pointsList,pixelsList)
    except ValueError:
        print("The message is too large to be encoded.")
 


def menuDecode():
    #picture = str(input("Enter the image with extension (ex: example.png): "))
    print("This is the current path: ", os.getcwd())
    #imgPath = str(input("Enter the path to the image: "))
    #facialFeature = str(input("Enter the facial feature (eyes, mouth, nose): "))
    #we are passing 1 in to the facial_feature_recog function to tell that function to decode
    picture = '1.png'
    imgPath = '/Users/Michael/Documents/Facial-Feature-Based-Image-Steganography//facial_recog/dataset/1.png'
    toGetPoints = '/Users/Michael/Documents/Facial-Feature-Based-Image-Steganography//facial_recog/original_dataset/1.png'
    facialFeature = 'nose'
    pointsList = facial_features.do_facial_feature_recog(picture, toGetPoints, 1, facialFeature)
    pointsList = pointsList[1]
    try:
        print("Decoded: {}".format(LSB.decode(picture,imgPath, pointsList)))
        #shutil will copy the original file and replace the encoded image with the original copy of the image
        shutil.copyfile(toGetPoints, imgPath)  
    except StopIteration:
        print("Exception")
        shutil.copyfile(toGetPoints, imgPath)

main()