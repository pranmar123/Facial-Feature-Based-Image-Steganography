    with open('key.txt', 'w+') as file:
        file.write(picture + '\n')
        file.write(imgPath + '\n')
        file.write(repr(pointsList) + '\n')
            #store the facial feature



    


def menuDecode():
    print("This is the current path: ", os.getcwd())
    picture = str(input("Enter the image:"))
    pathToKey = str(input("Enter the path to the key file: "))

    f = open(pathToKey)
    picture = f.readline().split('\n')
    imgPath = f.readline().split('\n')
    pointsList = f.readline().split('\n')
    f.close()
    #strip syntax
    picture = picture[0]
    imgPath = imgPath[0]
    pointsList = pointsList[0]
    #pointsList is a string so we must convert it back to a list
    pointsList = ast.literal_eval(pointsList)

    print("Decoded: {}".format(LSB.decode(picture,imgPath, pointsList)))

