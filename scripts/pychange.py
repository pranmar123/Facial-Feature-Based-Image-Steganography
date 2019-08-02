import shutil

imgPath = '/home/pranmar123/Multi-Facial-Steganography/facial_recog/dataset/key.txt'
#toGetPoints is there so that we get THE ORIGINAL points of the PNG instead of the modified points.
toGetPoints = '/home/pranmar123/Multi-Facial-Steganography/facial_recog/original_dataset/key.txt'

shutil.move(toGetPoints, imgPath)
