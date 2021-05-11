from playsound import playsound
import glob
import sys
import os
#playsound('myfile.wav')

import pygame

pygame.init()
pygame.mixer.init()
  

folder = "training_data/"+sys.argv[1]
path = os.path.abspath(folder)

print(path)

x = glob.glob(folder+"/*.wav")

for i in x:

    if not os.path.exists(path+"/ehm"):
        os.makedirs(path+"/ehm")

    if not os.path.exists(path+"/silent"):
        os.makedirs(path+"/silent")
	
    if not os.path.exists(path+"/false"):
        os.makedirs(path+"/false")

    #playsound(i)
    sound = pygame.mixer.Sound(i)
    sound.set_volume(2)   # Now plays at 90% of full volume.
    sound.play()


    answer = ""
    while(answer != "e" and answer != "p" and answer != "s" and answer != "f"):
        if (answer == "r"):
            print("RIPETO")
            sound = pygame.mixer.Sound(i)
            sound.set_volume(2)   # Now plays at 90% of full volume.
            sound.play()
		
        elif (answer == "SKIP"):
            break
		
        elif (answer != ""):
            print("Hai scritto male. Cosa volevi dire?\t")
    	
        answer = input("is [e]hm  / [s]ilent /[f]alse? or [r]epeat\t")
		
    if (answer == "e"):
        pos = os.path.abspath(path + "/ehm/" + os.path.basename(i))
        os.rename(i, pos) 
	
    elif (answer == "s"): 
        pos = os.path.abspath(path + "/silent/" + os.path.basename(i))
        os.rename(i, pos) 

    elif (answer == "f"):
        pos = os.path.abspath(path + "/false/" + os.path.basename(i))
        os.rename(i, pos) 


	