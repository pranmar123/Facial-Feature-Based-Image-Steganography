from PIL import Image, ImageDraw
import os
import face_recognition
import time
import random
from pathlib import Path

def select_image():

    #script_location will generate an absolute path of the current file. This is the fix for hardcoding location paths and overall improves the experience of the person trying to use the software 
    # so they no longer have to manually change the location paths on each machine this is run. 

    script_location = Path(__file__).absolute().parent
    path = str(script_location) +"/dataset"
    
    pictures_list = os.listdir(path)
    picture = str(input("Enter the name of the file you want to use for encoding: "))
    flag=True
    os.chdir(path)
    img_path = path+"/"+picture
 
 
    if os.path.isfile(img_path)==False:
        while flag:
            picture = str(input("The file doesn't exist, please enter a correct file name: "))
            img_path = path+"/"+picture
            if os.path.isfile(img_path)==True:
                flag=False
       

    return picture, img_path



def do_facial_feature_recog(img,path, decode = 0, facialFeature = None):
        image = face_recognition.load_image_file(path)
        face_landmarks_list = face_recognition.face_landmarks(image)
        face_location = face_recognition.face_locations(image)
        pil_image = Image.fromarray(image)
        d = ImageDraw.Draw(pil_image)


        print("I found {} face(s) in this photograph".format(len(face_location)))

        for face_landmarks in face_landmarks_list:
            #combining bottom lip, top lip, and chin into mouth
            #combining left_eye, left_eyebrow, right_eye, right_eyebrow into eyes
            #combing nose_bridge, nose_tip into nose.
            face_landmarks['mouth'] = face_landmarks['bottom_lip'] + face_landmarks['top_lip'] + face_landmarks['chin']
            face_landmarks['eyes'] = face_landmarks['left_eye'] + face_landmarks['right_eye'] + face_landmarks['left_eyebrow'] + face_landmarks['right_eyebrow']
            face_landmarks['nose'] = face_landmarks['nose_bridge'] + face_landmarks['nose_tip']
            face_landmarks['face'] = face_landmarks['bottom_lip'] + face_landmarks['top_lip'] + face_landmarks['chin'] + face_landmarks['left_eye'] + face_landmarks['right_eye']+ face_landmarks['left_eyebrow'] + face_landmarks['right_eyebrow'] + face_landmarks['nose_bridge'] + face_landmarks['nose_tip']
             
            #cleaning up the leftover points
            toRemove = ["bottom_lip","top_lip","chin","left_eye","right_eye","left_eyebrow","right_eyebrow","nose_bridge","nose_tip"]
            for each in toRemove:
                face_landmarks.pop(each)

            if decode == 1:
                facial_feature = facialFeature
            else: 
                #facial_feature = random.choice(list(face_landmarks.keys())) #if we want to allow the user to randomize their pick
                facial_feature = str(input("Enter the facial feature that you want to use for encoding (mouth, nose, eyes, face): ")).lower()
                while facial_feature != 'nose' and facial_feature != 'mouth' and facial_feature != 'eyes' and facial_feature != 'face':
                    facial_feature = str(input("Please Enter a correct facial feature: ")).lower()
                    

            points = face_landmarks[facial_feature]
            fullFacePoints = face_landmarks["face"]
            i = 0
            lengthPointsFace = len(fullFacePoints)
            lengthOfPoints = len(points)
            
            while i < lengthOfPoints:
                x, y = points[i][0], points[i][1]
                #adding surrounding points to the total list of points (in diagonals)
                for j in range(-10, 10):
                    points.append((x+j, y+j))
                i+= 1
            i = 0
            while i < lengthPointsFace: 
                x, y = fullFacePoints[i][0], fullFacePoints[i][1]
                for j in range(-10, 10): 
                    fullFacePoints.append((x+j, y+j))
                i += 1
            #removing duplicates
            fullFacePoints = list(dict.fromkeys(fullFacePoints))
            points = list(dict.fromkeys(points))
            print(f"This is len of points: {len(points)}") #test



            #Extracting pixel values
            pixels = pil_image.load()
            pixel_list = []
            for pair in points:
                x,y = pair[0], pair[1]
                pixel_list.append(pixels[x,y])
        d.line(points, width=0) #test
        pil_image.show() #test
        return facial_feature,points,pixel_list,fullFacePoints
