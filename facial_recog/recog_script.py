import cv2
import os
import numpy as np

def main():
    face_cascade = cv2.CascadeClassifier('~/Multi-Facial-Steganography/facial_recog/haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('~/Multi-Facial-Steganography/facial_recog/haarcascades/haarcascade_eye.xml')
    imgpath = '~/Multi-Facial-Steganography/facial_recog/dataset/s0/0.jpg'
    img = cv2.imread(imgpath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("img", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

main()