from PIL import Image
import face_recognition
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


def encode(picture,imgPath,points_list,pixels_list):
    image = Image.open(imgPath,'r')
    maxLen = len(points_list) // 3
    print("This is the maximum number of bytes that can be encoded: ", maxLen)
    message = str(input("Enter the message you wish to encode: "))
    if (len(message) == 0):
        raise ValueError("Message is empty") 
    
    newImage = image.copy()
    encodeMessage(newImage, message, points_list, pixels_list)

    #newImage.save("/home/pranmar123/Multi-Facial-Steganography/facial_recog/dataset/"+picture)
    newImage.save("/home/pranmar123/Facial-Feature-Based-Image-Steganography//facial_recog/dataset/1.png")


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



