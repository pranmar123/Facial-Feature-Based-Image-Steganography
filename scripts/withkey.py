import facial_features
import time
import os
from PIL import Image
import numpy as np 
import matplotlib.pyplot as plt
import scipy
import LSB
import ast

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
    time.sleep(2)
    facial_features.kill_example_pictures()
    LSB.encode(picture,imgPath,pointsList,pixelsList)
    with open('key.txt', 'w+') as file:
        file.write(picture + '\n')
        file.write(imgPath + '\n')
        file.write(repr(pointsList) + '\n')


def menuDecode():
    #picture = str(input("Enter the image with extension (ex: example.png): "))
    print("This is the current path: ", os.getcwd())
    #imgPath = str(input("Enter the path to the image: "))
    #facialFeature = str(input("Enter the facial feature (eyes, mouth, nose): "))
    #we are passing 1 in to the facial_feature_recog function to tell that function to decode
    picture = '8.png'
    imgPath = '/home/pranmar123/Multi-Facial-Steganography/facial_recog/dataset/8.png'
    pathToKey = '/home/pranmar123/Multi-Facial-Steganography/facial_recog/dataset/key.txt'
    facialFeature = 'mouth'
    #pointsList = facial_features.do_facial_feature_recog(picture, imgPath, 1, facialFeature)
    f = open(pathToKey)
    picture = f.readline().split('\n')
    imgPath = f.readline().split('\n')
    pointsList = f.readline().split('\n')
    f.close()
    #strip syntax
    picture = picture[0]
    imgPath = imgPath[0]
    pointsList = pointsList[0]
    #pointsList is a string so we must convert it back to a list
    pointsList = ast.literal_eval(pointsList)

    print("Decoded: {}".format(LSB.decode(picture,imgPath, pointsList)))


if __name__ == '__main__':
    main()
