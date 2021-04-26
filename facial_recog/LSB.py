from PIL import Image
import face_recognition
from pathlib import Path
##from facial_recog.facial_features import expand_points
#convert the secret message binary form based on ASCII value
def generateData(data):
    newData = []

    for i in data:
        newData.append(format(ord(i), '08b'))
    
    return newData

#modify pixels based on the 8-bit binary data and return the pixels
def modifyPixels(pixels, pixels_list, data):
    dataList = generateData(data)
    lengthOfData = len(dataList)
    if lengthOfData > len(pixels_list):
        raise ValueError
    imageData = iter(pixels_list)

    for i in range(lengthOfData):
        pixels = [value for value in imageData.__next__()[:3] + imageData.__next__()[:3] + imageData.__next__()[:3]]
        #Pixel value should be 1 for odd and 0 for even
        for j in range(0, 8):
            if (dataList[i][j]=='0') and (pixels[j]%2 != 0):

                if (pixels[j]% 2 != 0):
                    pixels[j] -= 1
            
            elif (dataList[i][j] == '1') and (pixels[j] % 2 == 0):
                pixels[j] -= 1
        #If the 8th pixel is 0 then it means keep reading; 1 means the msg is over
        if (i == lengthOfData - 1):
            if (pixels[-1]%2 == 0):
                pixels[-1] -= 1
        else:
            if (pixels[-1] % 2 != 0):
                pixels[-1] -= 1
        
        pixels = tuple(pixels)
        yield pixels[0:3]
        yield pixels[3:6]
        yield pixels[6:9]


def encodeMessage(newImage, message, points_list,pixels_list):
    counter = 0
    for pixel in modifyPixels(newImage.getdata(), pixels_list, message):
        #putting the modified pixels in the new image
        x,y = points_list[counter]
        counter+=1
        newImage.putpixel((x,y), pixel)


def encode(picture,imgPath,points_list,pixels_list,chosen_facial):
    image = Image.open(imgPath,'r')
    maxLen = len(points_list) // 3
    print("This is the maximum number of bytes that can be encoded: ", maxLen)
    message = str(input("Enter the message you wish to encode: "))

    flag=True
    largeMessageFlag = True
    extendFlag=True
    pointsListOriginal = points_list
    while flag:
        
        extend = "temp" #instantiate out of scope variable
        if (len(message)> maxLen): #check if the message is too large to encode
            print("ERROR: The message length is greater than ", maxLen," bytes")
            while largeMessageFlag: #loop for error correction 
                if(chosen_facial == 'face'): #if the 'face' feature is selected there are no additonal features to pick. 
                    print("ERROR: The message as typed is too large. There are no aditional features to encode to.")
                    message = str(input("Please enter a smaller message: ")) #give the option to encode a smaller message, loop if large again
                    if(len(message) < maxLen): #If the message is less than max byte length, message is good to encode, close flags
                        largeMessageFlag = False
                        extendFlag = False
                elif extendFlag == True: #Check if 
                    extend = str(input("Would you like to add an additional facial feature? (y/n): ")).lower()
                    largeMessageFlag = False

            #extend facial feature
            while extendFlag: 
                if (extend == 'y'): 
                    extended_feature = None
                    feature_list = ['eyes', 'mouth', 'nose']
                    feature_list.remove(str(chosen_facial)) #remove the feature that has already been selected
                    while extended_feature != feature_list[0] and extended_feature != feature_list[1]:
                        extended_feature = str(input("Enter the facial feature that you want to extend for encoding ({}, {}): ".format(*feature_list))).lower()
                    extendFlag = False
                    flag = False

                    ##THINGS TO FINISH
                    ## BREAK FACIAL_FEATURES DO_FACIAL_FEATURES_RECOG INTO MULTIPLE FUNCTIONS
                    ## THIS WILL THEN ALLOW YOU TO RUN PIECES OF IT TO THEN GET THE POINTS OF THE NEXT FACIAL FEATURE
                    ## ONCE YOU HAVE THE POINTS YOU CAN APPEND THAT TO THE MASTER POINTS LIST AND THEN WRITE IT
                    ## HAVE IT CHECK WHAT FACIAL FEATURE HAS BEEN SELECTED SO YOU DONT ENCODE THE MESSAGE INTO THE SAME FEATURE
                    ## TO THE IMAGE. I THINK THAT SHOULD MAKE SENSE???

                    

                    ##CODE expand pixel and then figure out how to find where the message ends
                elif(extend == 'n'): 
                    message = str(input("Please enter the message you wish to encode. "))
                    extendFlag = False
                    flag = False
                else:
                    extend = str(input("Please enter (y/n) if you would like to add an aditional facial feature: "))
                    extendFlag = True

            
        elif (len(message)==0):
            print("ERROR: The message is empty ")
            message = str(input("Please Enter a message again: "))
        else:
            flag=False


    newImage = image.copy()
    encodeMessage(newImage, message, points_list, pixels_list)
    print("The message Encoded successfully")

    #newImage.save("/home/pranmar123/Multi-Facial-Steganography/facial_recog/dataset/"+picture)
    script_location = Path(__file__).absolute().parent
    newImage.save(str(script_location) + "/dataset/" + picture)



def decode(picture, imgPath, points_list):
    image = face_recognition.load_image_file(imgPath)
    message = ''
    #get modified pixels
    pil_image = Image.fromarray(image)
    pix_map = pil_image.load()
    modified_pixels_list = []
    for pair in points_list:
        x,y = pair[0], pair[1]
        modified_pixels_list.append(pix_map[x,y])
 
    image_data = iter(modified_pixels_list) #we dont want the original pixels here we want the modified pixels here. 
    while True:
        pixels = [value for value in image_data.__next__()[:3] + image_data.__next__()[:3] + image_data.__next__()[:3]]
        binstr = ''
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        message += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return message



