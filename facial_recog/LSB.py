from PIL import Image

#convert the secret message into 8 bit binary form based on ASCII value 
def generateData(data):
    newData = []

    for i in data:
        newData.append(format(ord(i), '08b'))
    
    return newData

#modify pixels based on the 8-bit binary data and return the pixels
def modifyPixels(pixels, pixels_list, data):
    dataList = generateData(data)
    lengthOfData = len(dataList)
    imageData = iter(pixels_list)

    for i in range(lengthOfData):
        #taking 3 pixels at a time
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

#Encoding message into image
def encodeMessage(newImage, message, points_list,pixels_list):
    w = newImage.size[0]
    counter = 0
    for pixel in modifyPixels(newImage.getdata(), pixels_list, message):
        #putting the modified pixels in the new image
        x,y = points_list[counter]
        counter+=1
        newImage.putpixel((x,y), pixel)


def encode(picture,imgPath,chosenFeature,points_list,pixels_list):
    image = Image.open(imgPath,'r')

    message = str(input("Enter the message you wish to encode: "))
    if (len(message) == 0):
        raise ValueError("Message is empty") 
    
    newImage = image.copy()
    encodeMessage(newImage, message, points_list, pixels_list)

    newImage.save("/home/pranmar123/Multi-Facial-Steganography/facial_recog/dataset/save.png","PNG")
    #naybe I could save picture, imgpath, chosenfeature, and points be saved on a txt that the decode function
    #will extract from the text file

def decode(picture, imgPath, chosenFeature, points_list, pixels_list):
    image = Image.open(imgPath,'r')
    message = ''
    pix_map = image.load()
    #get modified pixels
    modified_pixels_list = []
    for pair in points_list:
        x,y = pair[0], pair[1]
        modified_pixels_list.append(pix_map[x,y])

    imageData = iter(modified_pixels_list) #we dont want the original pixels here we want the modified pixels here. 
    while True:
        #THE PROBLEM IS THE VALUE FOR VALUE is returning the original pixels but we need the modified pixels there.
        #one way to do it is get the points of all the places we modified and then get the NEW pixels from that and
        #plug that into imageData. 
        pixels = [value for value in imageData.__next__()[:3] + imageData.__next__()[:3] + imageData.__next__()[:3]]
        #binary data string
        binstr = ''
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        message += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return message



    
