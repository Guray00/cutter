# MARCHIO IL FILE
# ffmpeg -i input.mp4 -vcodec libx265 -crf 28 -metadata comment="compressed" output.mp4

# NO
# ffmpeg -i video.mkv -metadata comment="compressed" -c copy output.mp4


# VERIFICO SE HA IL MARCHIO
# rm -f .ck.txt && ffmpeg -i output.mp4 -f ffmetadata .ck.txt
# rm -f /tmp/squeeze/.ck.txt && ffmpeg -i output.mp4 -f ffmetadata /tmp/squeeze/.ck.txt && a = grep "comment=compressed"


# RECUPERIAMO L'ELENCO DEI VIDEO
# mkdir -p /tmp/squeeze/
# sudo find /var/www/html/nextcloud/data/Gray/files/Anno\ 2/ -regex  '.*\(mkv\|mp4\)$' > /tmp/squeeze/.titles.txt

import glob
import os
from tinytag import TinyTag 
import platform

def elaborate(type):
	command = "ffmpeg -i \"{}\" -vcodec libx265 -crf 28 -metadata comment=\"compressed\" \"{}\"".format(i, "./lite/"+i.replace(type, "[lite]."+type).replace("./", ""))
	print(command)
	os.system(command)
	os.system("mv \"{}\" \"{}\"".format(i, i.replace("./", "./fatti/")))

def win_elaborate(type):
	command = "ffmpeg -i \"{}\" -vcodec libx265 -crf 28 -metadata comment=\"compressed\" \"{}\"".format(i, ".\\lite\\"+i.replace(type, "[lite]."+type).replace(".\\", ""))
	print(command)
	os.system(command)
	os.system("move \"{}\" \"{}\"".format(i, i.replace(".\\", ".\\fatti\\")))



if __name__ == "__main__":
	# os.system("mkdir -p /tmp/squeeze/")
	x = glob.glob("./*.mp4")
	y = glob.glob("./*.mkv")

	p = platform.platform()+""
	
	for i in x:
		video = TinyTag.get(i) 
		if(video.comment != "compressed"): # se il video non è già compresso lo elabora		
			if "Windows" not in p:
				elaborate("mp4")
			else:
				win_elaborate("mp4")


	for i in y:
		try:
			video = TinyTag.get(i)
				 
			if(video.comment != "compressed"): # se il video non è già compresso lo elabora
				if "Windows" not in p:
					elaborate("mkv")
				else:
					win_elaborate("mkv")

		except:
			print("errore con "+ i)
			if "Windows" not in p:
				elaborate("mkv")
			else:
				win_elaborate("mkv")
		
