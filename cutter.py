# ffmpeg -i input.mp4 -metadata comment="compressed" -c copy output.mp4

import glob
import os
import sys
from tinytag import TinyTag 
import argparse
import signal
import platform


# GESTIONE ARGOMENTI
WORKING = ""
parser = argparse.ArgumentParser()
parser.add_argument("foldername", help="video file name (or full file path) to classify")
parser.add_argument("--teams", default=False,action="store_true", help="crops the video")

args = parser.parse_args()

# print text at center of screen
def print_centered(text):
	print("\033[1;37;40m")
	print(text.center(os.get_terminal_size().columns))
	print("\033[0;37;40m")
 
 
 # print full line of "="
def print_line():
    print("─"*os.get_terminal_size().columns)

# GESTIONE CHIUSURA IMPROVVISA
def signal_handler(sig, frame):
    print_line()
    print_centered("Rilevata chiusura forzata")
    print_centered("In corso: " + WORKING)
    print("\n\n")
    
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
	
    print_line()
    print("\n\n\n")
    sys.exit(0)
    
# handler di CTRL+C
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


# verifica che sia un file non ancora elaborato
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


# taglia il file
def cut(__file__):
	filename, file_extension = os.path.splitext(__file__)		# recupero il filename ed estensione
	name = os.path.basename(filename)							# recupero il nome del file con estensione
	output = f"{filename}[JUNK]{file_extension}"				# creo il nome del file di output
	scriptname = "./Remsi/remsi.py"								# recupero il nome dello script di remsi
	tempfile = "temp"											# nome del file temporaneo
 
	# creo un file .bat su windows
	p = platform.platform()+""
	if "Windows" in p:
		tempfile += ".bat"

	# eseguo remsi per la rilevazione dei silenzi
	command = f'ffmpeg -i "{__file__}" -hide_banner -af silencedetect=n=-40dB:d=0.75 -f null - 2>&1 | python {scriptname} > {tempfile}'
	print_line()
	print_centered("Generando il comando")
	print(command)
	print_line()
	print("\n")
	os.system(command)
 
	
	# eseguo il comando di taglio
	print_line()
	print_centered("Eseguendo il taglio")
	print_line()
	print("\n")
	os.system(tempfile)
 
	# restituisci il nome del file di output
	return output



# =================== MAIN ===================
if __name__ == "__main__":
	folder = args.foldername				# recupero il nome della cartella
	location = os.path.abspath(folder)		# recupero la posizione della cartella
	
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
	
	# per ogni video esaminato
	for i in z:		
		print("===> " + i)
			
		# se il video non è già stato elaborato
		if(checkCut(i)):
			continue

		
		WORKING = i				# setto il file che sto elaborando
		filename = cut(i) 		# eseguo il taglio

		# verifico se è un video di teams
		if (args.teams):
			filename = crop(filename, 62, 0, 1796, 972)
	
		# altrimenti aggiungo solo i metadata
		else:
			filename = crop(filename)

		# rimuovo i file inutili
		try:
			print("\n")
			print_line()
			print_centered(i+" completato")
			print_line()
			print("\n")
   
			# sposto in cut il file elaborato
			pos = os.path.abspath(location + "/cut/" + os.path.basename(filename))
			os.rename(filename, pos)

			# sposto in fatti il file originale
			pos = os.path.abspath(location + "/fatti/" + os.path.basename(i))
			os.rename(i, pos)

			# elimino il file junk senza crop e metadata
			os.remove(filename.replace("[CUT]","[JUNK]"))
   
		except:
			print("Errore con il file: " + i)
		
		
