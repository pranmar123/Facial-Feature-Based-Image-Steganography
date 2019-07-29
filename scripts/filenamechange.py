import os


listt = ["s0","s1","s2","s3","s4","s5","s6","s7","s8","s9","s10","s11","s12","s13","s14"]
list2 = ["0","1","2","3","4"]
for filename in os.listdir("/home/pranmar123/Multi-Facial-Steganography/facial_recog/dataset"):
    count=0
    print(filename)
    path = "/home/pranmar123/Multi-Facial-Steganography/facial_recog/dataset/"+filename
    if os.path.isdir("/home/pranmar123/Multi-Facial-Steganography/facial_recog/dataset/"+filename) == True:
        os.chdir(path)
        for each in os.listdir(path):
            dst=list2[count] + ".jpg"
            count+=1
            os.rename(each, dst)

        
