from PIL import Image, ImageDraw
import os
import face_recognition
import time

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
            d.line(face_landmarks[facial_feature], width=5)


    pil_image.show()
    time.sleep(.5)

    #now rename the images into correct order and figure out how to pass into DCT (PUT ALL IMGS IN ARRAY AND RANDOMIZE)
    #kill all png  ps aux | pkill -f PNG

    return True
    




def main():
    path = "facial_recog/dataset/"
    for filename in os.listdir("/home/pranmar123/Multi-Facial-Steganography/facial_recog/dataset"):
        path = "/home/pranmar123/Multi-Facial-Steganography/facial_recog/dataset/"+filename
        if os.path.isdir(path) == True:
            os.chdir(path)
            for each in os.listdir():
                img_path = path + "/" + each
                do_facial_feature_recog(each, img_path)








main()