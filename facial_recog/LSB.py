from PIL import Image, ImageDraw
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
    try: 
        for pixel in modifyPixels(newImage.getdata(), pixels_list, message):
            #putting the modified pixels in the new image
            x,y = points_list[counter]
            counter+=1
            newImage.putpixel((x,y), pixel)
    except StopIteration: 
        print("StopIteration encodeMessage()")

        


def encode(picture,imgPath,points_list,pixels_list,chosen_facial, full_face):
    image = Image.open(imgPath,'r')
    maxSingleFeature = len(points_list) // 3
    absoluteMaxSize = len(full_face) // 3

    print("This is the maximum number of bytes that can be encoded: ", maxSingleFeature)
    message = str(input("Enter the message you wish to encode: "))

    flag=True
    largeMessageFlag = True
    extendFlag=True
    pointsListOriginal = points_list
    pixelListOriginal = pixels_list
    while flag:
        
        extend = None #instantiate out of scope variable
        if (len(message)> maxSingleFeature): #check if the message is too large to encode
            print("ERROR: The message length is greater than ", maxSingleFeature," bytes")
            while largeMessageFlag: #loop for error correction 
                if(chosen_facial == 'face'): #if the 'face' feature is selected there are no additonal features to pick. 
                    print("ERROR: The message as typed is too large. There are no aditional features to encode to.")
                    message = str(input("Please enter a smaller message: ")) #give the option to encode a smaller message, loop if large again
                    if(len(message) < maxSingleFeature): #If the message is less than max byte length, message is good to encode, close flags
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
                    if(len(message) > absoluteMaxSize): 
                        print("Error: The message is still too large. Exiting.")
                        break
                    else: 
                        expandedPointsList, expandedPixelsList = calculate_expanded_feature_points(picture, imgPath, extended_feature)
                        #add both together for more message space.
                        pixels_list = pixelListOriginal + expandedPixelsList
                        points_list = pointsListOriginal + expandedPointsList
                    
                    
                elif(extend == 'n'): 
                    message = str(input("Please enter the message you wish to encode: "))
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


#function that will take the message, and break it up into another string. 
#message is the message
#n is the length to cut at. 
def split_message(message, n): 
    for x in range(0, len(message), n): 
        yield message[x:x+n]
    

def calculate_expanded_feature_points(img,path, facialFeature = None): 
        image = face_recognition.load_image_file(path)
        face_landmarks_list = face_recognition.face_landmarks(image)
        face_location = face_recognition.face_locations(image)
        pil_image = Image.fromarray(image)
        d = ImageDraw.Draw(pil_image)
        for face_landmarks in face_landmarks_list:
            face_landmarks['mouth'] = face_landmarks['bottom_lip'] + face_landmarks['top_lip'] + face_landmarks['chin']
            face_landmarks['eyes'] = face_landmarks['left_eye'] + face_landmarks['right_eye'] + face_landmarks['left_eyebrow'] + face_landmarks['right_eyebrow']
            face_landmarks['nose'] = face_landmarks['nose_bridge'] + face_landmarks['nose_tip']
            face_landmarks['face'] = face_landmarks['bottom_lip'] + face_landmarks['top_lip'] + face_landmarks['chin'] + face_landmarks['left_eye'] + face_landmarks['right_eye']+ face_landmarks['left_eyebrow'] + face_landmarks['right_eyebrow'] + face_landmarks['nose_bridge'] + face_landmarks['nose_tip']
            #cleaning up the leftover points
            toRemove = ["bottom_lip","top_lip","chin","left_eye","right_eye","left_eyebrow","right_eyebrow","nose_bridge","nose_tip"]
            for each in toRemove:
                face_landmarks.pop(each)
        points = face_landmarks[facialFeature]
        i = 0
        lengthOfPoints = len(points)
            
        while i < lengthOfPoints:
            x, y = points[i][0], points[i][1]
            #adding surrounding points to the total list of points (in diagonals)
            for j in range(-10, 10):
                points.append((x+j, y+j))
            i+= 1

        #removing duplicates
        points = list(dict.fromkeys(points))
        print(f"This is len of points: {len(points)}") #test        


        pixels = pil_image.load()
        pixel_list = []
        for pair in points:
            x,y = pair[0], pair[1]
            pixel_list.append(pixels[x,y])
        d.line(points, width=0) #test
        pil_image.show() #test
        return points,pixel_list





