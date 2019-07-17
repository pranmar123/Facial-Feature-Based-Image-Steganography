from PIL import Image, ImageDraw
import os
import face_recognition
import time
import random

def select_image():
    path = "/home/pranmar123/Multi-Facial-Steganography/facial_recog/dataset"
    pictures_list = os.listdir(path)
    #remove any non pictures from pictures_list
    for each in pictures_list:
        if ".jpg" not in each:
            pictures_list.remove(each)

    #randomly selecting a element from our picture list to perform facial feature recognition 
    picture = random.choice(pictures_list)
    os.chdir(path)
    img_path = "/home/pranmar123/Multi-Facial-Steganography/facial_recog/dataset/"+picture
    print("The file that was chosen was: ", picture)
    return picture, img_path


def do_facial_feature_recog(img,path):
    image = face_recognition.load_image_file(img)

    face_landmarks_list = face_recognition.face_landmarks(image)

    print("I found {} face(s) in the photo".format(len(face_landmarks_list)))

    #If the machine did not find any landmarks then delete the image
    if len(face_landmarks_list) == 0:
        print("Removing: " + img + " at " + path)        
        os.remove(path)
        return False

    pil_image = Image.fromarray(image)
    d = ImageDraw.Draw(pil_image)


    for face_landmarks in face_landmarks_list:

        for facial_feature in face_landmarks.keys():
            print("The {} in this face has the following points: {}".format(facial_feature, face_landmarks[facial_feature]))

        for facial_feature in face_landmarks.keys():
            #drawing line on each of the facial features
            d.line(face_landmarks[facial_feature], width=5)

##pick random picture and random facial feature and send coordinates to either other module or to do DCT on. 
    pil_image.show()
    time.sleep(.1)


    return True
    
def kill_example_pictures():
    myCmd = "ps aux | pkill -f PNG"
    os.system(myCmd)




def main():

    picture, img_path = select_image()
    do_facial_feature_recog(picture, img_path)
    time.sleep(5)
    kill_example_pictures()







main()