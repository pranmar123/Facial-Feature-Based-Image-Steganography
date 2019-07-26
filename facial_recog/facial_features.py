from PIL import Image, ImageDraw
import os
import face_recognition
import time
import random

def select_image():
    path = "/home/pranmar123/Multi-Facial-Steganography/facial_recog/dataset"
    pictures_list = os.listdir(path)

    #randomly selecting a element from our picture list to perform facial feature recognition 
    picture = random.choice(pictures_list)
    os.chdir(path)
    img_path = "/home/pranmar123/Multi-Facial-Steganography/facial_recog/dataset/"+picture
    print("The file that was chosen was: ", picture)
    return picture, img_path


def do_facial_feature_recog(img,path):
    image = face_recognition.load_image_file(img)

    face_landmarks_list = face_recognition.face_landmarks(image)


    #If the machine did not find any landmarks then delete the image
    if len(face_landmarks_list) == 0:
        print("Removing: " + img + " at " + path)        
        os.remove(path)
        return False

    pil_image = Image.fromarray(image)
    d = ImageDraw.Draw(pil_image)

    for face_landmarks in face_landmarks_list:
        #combining bottom lip, top lip, and chin into mouth
        #combining left_eye, left_eyebrow, right_eye, right_eyebrow into eyes
        #combing nose_bridge, nose_tip into nose.
        #This will give us 3 features to randomly choose from to hide information
        face_landmarks['mouth'] = face_landmarks['bottom_lip'] + face_landmarks['top_lip'] + face_landmarks['chin']
        face_landmarks['eyes'] = face_landmarks['left_eye'] + face_landmarks['right_eye'] + face_landmarks['left_eyebrow'] + face_landmarks['right_eyebrow']
        face_landmarks['nose'] = face_landmarks['nose_bridge'] + face_landmarks['nose_tip']
        #cleaning up the leftover points
        toRemove = ["bottom_lip","top_lip","chin","left_eye","right_eye","left_eyebrow","right_eyebrow","nose_bridge","nose_tip"]
        for each in toRemove:
            face_landmarks.pop(each)
        facial_feature = random.choice(list(face_landmarks.keys()))

        d.line(face_landmarks[facial_feature], width=5)
    pil_image.show()
    time.sleep(.1)
    return facial_feature, face_landmarks[facial_feature]


    
def kill_example_pictures():
    myCmd = "ps aux | pkill -f PNG"
    os.system(myCmd)


