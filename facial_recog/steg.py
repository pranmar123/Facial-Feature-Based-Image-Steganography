import facial_features
import time
import os
from PIL import Image
import numpy as np 
import scipy
import LSB
import shutil
from pathlib import Path
import time

def main():
    choice = 0
    while choice != '1' and choice != '2' and choice != '3':
        choice = input("Please select an option: \n 1. Encode Message \n 2. Decode Message \n 3. Exit \n Your Selection: ")
        if choice == '1':
            menuEncode()
            choice=0
        elif choice == '2':
            menuDecode()
            choice=0
        elif choice == '3':
            print("Thank You. Exiting.")
            exit()


def menuEncode():
    picture, imgPath = facial_features.select_image()
    chosenFeature, pointsList, pixelsList = facial_features.do_facial_feature_recog(picture, imgPath)
    print("The important information: \n Picture chosen: {} \n Chosen feature: {} ".format(picture, chosenFeature))
    try:
        LSB.encode(picture,imgPath,pointsList,pixelsList)
    except ValueError:
        print("The message is too large to be encoded.")
   

 


def menuDecode():

    script_location = Path(__file__).absolute().parent
    picture = str(input("Enter the image with extension (ex: example.png): "))
    flag=True
    imgPath = str(script_location) +"/dataset/" + picture
    if os.path.isfile(imgPath)==False:
        while flag:
            picture = str(input("This image doesn't exist, please Enter a correct image name: "))
            imgPath = str(script_location) +"/dataset/" + picture
            if os.path.isfile(imgPath)==True:
                flag=False
                
    print("This is the current path: ", os.getcwd())
    #imgPath = str(input("Enter the path to the image: "))
    facialFeature = str(input("Enter the facial feature (eyes, mouth, nose, face): "))
    facialFeature=facialFeature.lower()
    while facialFeature != 'nose' and facialFeature != 'mouth' and facialFeature != 'eyes' and facialFeature != 'face':
        facialFeature = str(input("Please Enter a correct facial feature: "))
        facialFeature=facialFeature.lower()
    #we are passing 1 in to the facial_feature_recog function to tell that function to decode
    #picture = '1.png'
    toGetPoints = str(script_location) +"/original_dataset/" + picture
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
