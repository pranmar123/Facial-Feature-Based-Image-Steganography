import os
from time import sleep

def main():

    for filename in os.listdir("/home/pranmar123/Downloads/dataset"):
        newdir = "/home/pranmar123/Downloads/dataset/"+filename
        #going into the folders
        if os.path.isdir(newdir) == True:
            os.chdir(newdir)
            test = os.listdir(newdir)           
            #removing .txt
            for i in test:
                if i.endswith(".txt"):
                    os.remove(os.path.join(newdir, i))
            #removing every files
            test = os.listdir(newdir)
            for i in test[::444]:
                os.remove(i)
                print("Removed file: ",i)
            #renaming the leftover files
            test = os.listdir(newdir)
            count = 0
            for i in test:
                dst = str(count) + ".jpg" 
                os.rename(i,dst)
                count += 1
                

main()
