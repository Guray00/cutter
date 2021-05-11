# ffmpeg -i input.mp4 -metadata comment="compressed" -c copy output.mp4

import glob
import os
import sys
from tinytag import TinyTag 
import argparse
import signal


# GESTIONE ARGOMENTI
WORKING = ""
parser = argparse.ArgumentParser()
parser.add_argument("foldername", help="video file name (or full file path) to classify")
parser.add_argument("--teams", default=False,action="store_true", help="crops the video")
parser.add_argument("--generate-training-data", default="", action='store_true', help="export extracted ehm(s) and silences as well to a separate folder. Useful for training on false positives")

args = parser.parse_args()


# GESTIONE CHIUSURA IMPROVVISA
def signal_handler(sig, frame):
    print('\n\n============== DETECTED FORCE CLOSE ==============\n')
    print("current: " + WORKING)

    if (WORKING != ""):
        filename, file_extension = os.path.splitext(WORKING)
		
		# elimino i file non completati
        try:
            #os.remove(f'{filename}.wav')
            #print(f'==> Removed {filename}.wav')
            os.remove(f'{filename}[JUNK]{file_extension}')
            print(f'==> Removed {filename}[JUNK]{file_extension}')
            os.remove(f'{filename}[CUT]{file_extension}')
            print(f'==> Removed {filename}[CUT]{file_extension}')			

        except:
            pass
	
    print("\n\n\n")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


# TAGLIA IL VIDEO E AGGIUNGE IL METADATA
def crop(path, x=-1, y=-1, width=-1, height=-1, meta="cut"):
	filename, file_extension = os.path.splitext(path)
	location = os.path.dirname(os.path.abspath(path))

	filename = filename.replace("[JUNK]", "")

	if (x == -1 or y == -1 or width == -1 or height == -1):
		command= f'ffmpeg -i "{path}" -hide_banner -metadata comment="cut" -c copy "{filename}[CUT]{file_extension}"'
	
	else:
		command= f'ffmpeg -i "{path}" -hide_banner -metadata comment="cut" -filter:v "crop={width}:{height}:{x}:{y}" -threads 0 -preset ultrafast "{filename}[CUT]{file_extension}"'
	
	print(command)

	try:
		os.system(command)
	except:
		raise("Maybe not teams file")

	return f"{filename}[CUT]{file_extension}"


# CONTROLLA CHE NON SIA UN VIDEO GIA' ELABORATO
def checkCut(__file__):
	try:
		video = TinyTag.get(i) 
		if(video.comment != "cut" and "[JUNK]" not in __file__): # se il video non è già compresso lo elabora
			return False
		return True

	except:
        	if ("[JUNK]" not in __file__ ):
            		return False
			
	return False


# TAGLIA IL FILE
def cut(__file__):
	filename, file_extension = os.path.splitext(__file__)
	name = os.path.basename(filename)
	output = f"{name}[JUNK]{file_extension}"
	simple = "simple_ehm-runnable.py"
	#--generate-training-data

	gtd = ""
	if(args.generate_training_data):
		gdt = "--generate-training-data"

	command = f'python3 {simple} "{__file__}" --output "{output}" {gdt}'

	print(command)
	os.system("cd simple-ehm && " + command)

	
	return f'{filename}[JUNK]{file_extension}'


def moveTrainingData(filename):
	if (args.generate_training_data == ""):
		return

	filen, file_extension = os.path.splitext(filename)
	name = os.path.basename(filen)

	x = glob.glob("simple-ehm/training_data/*.wav")

	if not os.path.exists(f'training_data/{name} creato'):
        	os.makedirs(f'training_data/{name}')

	for i in x:
		wav = os.path.basename(i)
		os.rename(i, f'training_data/{name}/{wav}')


if __name__ == "__main__":
	folder = args.foldername	
	location = os.path.abspath(folder)
	
	# creo la cartella fatti se non presente
	if not os.path.exists(location+"/fatti"):
        	os.makedirs(location+"/fatti")

	# creo la cartella cut se non presente
	if not os.path.exists(location+"/cut"):
        	os.makedirs(location+"/cut")

	# cerco tutti i video in mp4 e in mkv
	x = glob.glob(f"{location}/*.mp4")
	y = glob.glob(f"{location}/*.mkv")
	z = x + y
	
	for i in z:		
		print("===> " + i)
			
		if(checkCut(i)):
			continue

		
		WORKING = i
		filename = cut(i)

		if (args.teams):
			filename = crop(filename, 62, 0, 1796, 972)
	
		else:
			filename = crop(filename)

		# REMOVES JUNKS
		try:
			print("===> " + i + " DONE")
			#input("waiting")
			# sposto in cut il file elaborato
			pos = os.path.abspath(location + "/cut/" + os.path.basename(filename))
			os.rename(filename, pos)

			# sposto in fatti il file originale
			pos = os.path.abspath(location + "/fatti/" + os.path.basename(i))
			os.rename(i, pos)

			# elimino il file junk senza crop e metadata
			os.remove(filename.replace("[CUT]","[JUNK]"))
			moveTrainingData(i)
		except:
			pass
		
		