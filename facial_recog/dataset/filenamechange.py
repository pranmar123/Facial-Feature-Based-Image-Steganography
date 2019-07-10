import os

count=0
listt = ["s0","s1","s2","s3","s4","s5","s6","s7","s8","s9","s10","s11","s12","s13","s14"]
       
for filename in os.listdir("/home/pranmar123/Multi-Facial-Steganography/facial_recog/dataset"):
    print(filename)
    if os.path.isdir("/home/pranmar123/Multi-Facial-Steganography/facial_recog/dataset/"+filename) == True:
        if count > 14:
            count = 0
        dst=listt[count]
        count+=1
        
        while True:
            try:
                os.rename(filename,dst)
                break
            except OSError:
                if count > 14:
                    count = 0
                dst = listt[count]
                count+=1
                continue

