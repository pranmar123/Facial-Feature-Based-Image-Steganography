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
    picture, imgPath = facial_features.select_image() #select_image() function is called
    chosenFeature, pointsList, pixelsList = facial_features.do_facial_feature_recog(picture, imgPath) #do_facial_feature_recog() function
    print("The important information: \n Picture chosen: {} \n Chosen feature: {} ".format(picture, chosenFeature))
    try:
        LSB.encode(picture,imgPath,pointsList,pixelsList, chosenFeature)
    except ValueError:
        print("Function menuEncode(): There was an error while ")
   

 


def menuDecode():

    script_location = Path(__file__).absolute().parent
    picture = str(input("Enter the image with extension (ex: example.png): "))
    flag=True
    imgPath = str(script_location) +"/dataset/" + picture
    facialFeature = None
    facialFeature1 = []
    facialFeature2 = []
    #this list is so the program will check the first feature, and remove it form the list, and then apply the list to the formatted string
    #when it asks for a secondary feature. So the user doesn't have an option to type nose and nose
    facialFeaturesList = ['nose', 'eyes', 'mouth']
    if os.path.isfile(imgPath)==False:
        while flag:
            picture = str(input("This image doesn't exist, please Enter a correct image name: "))
            imgPath = str(script_location) +"/dataset/" + picture
            if os.path.isfile(imgPath)==True:
                flag=False
    howManyFeatures = str(input("How many facial features to be decoded? (1 or 2): "))
    while howManyFeatures != '1' and howManyFeatures != '2': 
        howManyFeatures = str(input("Error: How many facial features to be decoded? (1 or 2): "))
    print("This is the current path: ", os.getcwd())
    #imgPath = str(input("Enter the path to the image: "))
    if(howManyFeatures == "1"):
        #if one feature
        facialFeature = str(input("Enter the facial feature (eyes, mouth, nose, face): ")).lower()
        while facialFeature != 'nose' and facialFeature != 'mouth' and facialFeature != 'eyes' and facialFeature != 'face': 
            facialFeature = str(input("Please enter a correct facial feature (eyes, mouth, nose, face): ")).lower()
    else: 
        #if two features
        facialFeature1 = str(input("Enter the first facial feature (eyes, mouth, nose): ")).lower()
        while facialFeature1 != 'nose' and facialFeature1 != 'mouth' and facialFeature1 != 'eyes':
            facialFeature1 = str(input("Please enter a correct facial feature (eyes, mouth, nose): ")).lower()
        facialFeaturesList.remove(facialFeature1) #remove from list, to show user which options remain.
        facialFeature2 = str(input("Enter the second facial feature ({}, {}): ".format(*facialFeaturesList)))
        while facialFeature2 != facialFeaturesList[0] and facialFeature2 != facialFeaturesList[1]: 
            facialFeature2 = str(input("Please enter a correct secondary facial feature ({}, {}): ".formar(*facialFeaturesList))).lower()

    pointsList = []
    
    
    toGetPoints = str(script_location) +"/original_dataset/" + picture
    if howManyFeatures == "1": 
        xx, pointsList, pixel_list = facial_features.do_facial_feature_recog(picture, toGetPoints, 1, facialFeature)
    else: 
        zzz, pointsListFeature1, xxx = facial_features.do_facial_feature_recog(picture, toGetPoints, 1, facialFeature1)
        zzzz, pointsListFeature2, xxxx = facial_features.do_facial_feature_recog(picture, toGetPoints, 1, facialFeature2)
        pointsList = pointsListFeature1 + pointsListFeature2
    #pointsList = pointsList[1]
    try:
        print("Decoded: {}".format(LSB.decode(picture,imgPath, pointsList)))
        #shutil will copy the original file and replace the encoded image with the original copy of the image
        shutil.copyfile(toGetPoints, imgPath)  
    except StopIteration:
        print("Error: Could not decode message.")
        shutil.copyfile(toGetPoints, imgPath)


main()
