from PIL import Image
import math
import os

# Only works with PNG images due to JPG compression issues messing up the message

def encodeMessage(imageName, path, pointsList, pixelsList, msg):
    image = Image.open(path)
    width, height = image.size
    if len(pointsList) < len(msg):
        raise ValueError
    pixels = image.load()
    for i in range(0, len(msg)):
        encodedChar = str(ord(msg[i]))
        #pixel = pixelsList[i] #added (interesting maybe the alternate))
        pixel = pixels[pointsList[i]]
        newPixel = list(pixel)
        newPixel[0] = str(newPixel[0])
        newPixel[1] = str(newPixel[1])
        newPixel[2] = str(newPixel[2])

        if ord(msg[i]) >= 100:
            r = list(newPixel[0])
            r[-1] = encodedChar[0]
            newPixel[0] = ''.join(r)

            r = list(newPixel[1])
            r[-1] = encodedChar[1]
            newPixel[1] = ''.join(r)

            r = list(newPixel[2])
            r[-1] = encodedChar[2]
            newPixel[2] = ''.join(r)

        elif ord(msg[i]) >= 10:
            r = list(newPixel[0])
            r[-1] = '0'
            newPixel[0] = ''.join(r)

            r = list(newPixel[1])
            r[-1] = encodedChar[0]
            newPixel[1] = ''.join(r)

            r = list(newPixel[2])
            r[-1] = encodedChar[1]
            newPixel[2] = ''.join(r)

        else:
            r = list(newPixel[0])
            r[-1] = '0'
            newPixel[0] = ''.join(r)

            r = list(newPixel[1])
            r[-1] = '0'
            newPixel[1] = ''.join(r)

            r = list(newPixel[2])
            r[-1] = encodedChar[0]
            newPixel[2] = ''.join(r)


        newPixel[0] = int(newPixel[0])
        newPixel[1] = int(newPixel[1])
        newPixel[2] = int(newPixel[2])
        image.putpixel((pointsList[i]), tuple(newPixel))
    pixel = pixels[pointsList[i+1]]
    newPixel = list(pixel)
    newPixel[0] = str(newPixel[0])
    newPixel[1] = str(newPixel[1])
    newPixel[2] = str(newPixel[2])

    r = list(newPixel[0])
    r[-1] = '1'
    newPixel[0] = ''.join(r)
    
    r = list(newPixel[1])
    r[-1] = '2'
    newPixel[1] = ''.join(r)

    r = list(newPixel[2])
    r[-1] = '7'
    newPixel[2] = ''.join(r)



    newPixel[0] = int(newPixel[0])
    newPixel[1] = int(newPixel[1])
    newPixel[2] = int(newPixel[2])
    image.putpixel((pointsList[i+1]), tuple(newPixel))
    image.save("/home/pranmar123/Multi-Facial-Steganography/facial_recog/dataset/" + imageName)


def decodeMessage(picture, imgPath, pointsList):
    image = Image.open(imgPath)
    pixels = image.load()
    encodedText = ""
    for each in pointsList:
            pixel = pixels[each]
            encodedChar = int(str(pixel[0])[-1]) * 100 + int(str(pixel[1])[-1]) * 10 + int(str(pixel[2])[-1])
            if(encodedChar == 127):
                return encodedText
            else:
                encodedText+=chr(encodedChar)
    return encodedText