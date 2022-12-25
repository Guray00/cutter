import glob
import os
import sys
from tinytag import TinyTag 
import argparse
import signal
import platform
import ffmpeg
import tempfile
import shutil
import remsi


# costanti di default
NOISE	 = -40
DURATION = 0.80
WORKING  = ""
ORIGINAL_FILES_DESTINATION_FOLDER = "originals"
EDITED_FILES_DESTINATION_FOLDER   = "edited"

EDITED_FILE_MARK = "[EDIT]"
TMP_FILE_MARK    = "[TMP]"

# necessario per l'export di windows
try:
	if (os.environ["EXPORT"] == "win"):
		base_path = sys._MEIPASS
		FFMPEG_CMD = base_path + "\\ffmpeg.exe"

	elif (os.environ["EXPORT"] == "linux"):
		base_path = sys._MEIPASS
		FFMPEG_CMD = base_path + "/ffmpeg"
   
except:
	FFMPEG_CMD = "ffmpeg"
# ==================================    


# calculate difference between two video duration
def durationDiff(original, edited):
	try:
		video1 = TinyTag.get(original) 
		video2 = TinyTag.get(edited) 

		minutes = str(int((abs(video1.duration - video2.duration))/60))
		seconds = f"{int((abs(video1.duration - video2.duration))%60):02d}"
  
		return minutes + ":" + seconds

	except Exception as e:
		print(f"errore: {e}")
		return -1

# argomenti
parser = argparse.ArgumentParser()
parser.add_argument("path", help="the path of the video or the folder (for many videos) to cut")
# parser.add_argument("--teams", default=False,action="store_true", help="crops the video")
parser.add_argument('-d', type=int, required=False, default=DURATION, help='duration of silence in seconds')
parser.add_argument('-n', type=int, required=False, default=NOISE, help='noise level in dB')
parser.add_argument('-fr', type=int, required=False, help='output video frame rate')
parser.add_argument('-x', type=float, default=-1, required=False, help='Speed of the video')
parser.add_argument('-vfr', default=False, required=False, action="store_true", help='variable frame rate on output (if -fr is given, it indicates the max number of duplicates frames per second)')
parser.add_argument('--keep-cfr', default=False, required=False, action="store_true", help='keeps Constant Frame Rate version of the file for future editing.')
parser.add_argument('--preview', default=False, required=False, action="store_true", help='makes a preview of 180 seconds')
args = parser.parse_args()

# print text at center of screen
def print_centered(text):
	print("\033[1;37;40m")
	print(text.center(os.get_terminal_size().columns))
	print("\033[0;37;40m")
 
 
 # print full line of "="
def print_line():
    print("─"*os.get_terminal_size().columns)
    
# stampa le informazioni sui comandi eseguiti
def fancy_print(arg1, arg2=""):
	print_line()
	print_centered(arg1)
	# print("\x1B[3m"+arg2+"\x1B[0m")
	print_line()
	print("\n")

# GESTIONE CHIUSURA IMPROVVISA
def signal_handler(sig, frame):
	print()
	print_line()
	print_centered("⛔️ Rilevata \033[91mchiusura\033[0m forzata ⛔️")
	print_centered("Era in corso: " + WORKING)
    
	if (WORKING != ""):
		filename, file_extension = os.path.splitext(WORKING)
		
		# elimino i file non completati
		try:
			os.remove(f'{filename}[JUNK]{file_extension}')
		except:
			pass
			
		try:
			os.remove(f'{filename}[CUT]{file_extension}')
      
		except:
			pass

		try:
        		os.remove(f'{filename}[TMP]{file_extension}')
		except:
			pass

	print_line()
	print("\n\n")
	sys.exit(0)
    
# handler di CTRL+C
signal.signal(signal.SIGINT, signal_handler)

# controlla se un video è a framerate variabile
def check_variable_framerate(media_file):
    
	try:
		denom = int(ffmpeg.probe(media_file)["streams"][0]["avg_frame_rate"].split("/")[1])
	
		# se il denominatore è 1, allora il framerate è statico
		if(denom == 1):
			return False

		# altrimenti è variabile
		return True

	# se si verifica qualche problema continuo ipotizzando
	# che il file sia cfr
	except:
		return False


"""
# DEPRECATO
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
"""

# converte un video a framerate variabile in un video a framerate statico
def convert_to_cfr(_input_file, _output_file):
    
    # se è già stato correttamente processato
	if ( os.path.exists(_output_file) and TinyTag.get(_output_file).comment == "cfr version"):
		return

	filename, file_extension = os.path.splitext(_input_file)
	name = os.path.basename(filename)
	tmp_path= tempfile.gettempdir()

	_tmp_file = f"{tmp_path}/{name}{TMP_FILE_MARK}{file_extension}"
 
	#_tmp_output = f"{tmp_path}/{name}{file_extension}"			# creo il nome del file di output temporaneo
 
	# decode delle opzioni
	_fr  = f"-r {args.fr}" if (args.fr) else ""	# framerate
	_t 	 = f"-t 180" if (args.preview) else ""
 
	# effettua la conversione
	command = f"{FFMPEG_CMD} -y -ignore_chapters 1 -i \"{_input_file}\" {_t} -hide_banner -loglevel info -vsync cfr -metadata comment=\"cfr version\" {_fr} -preset ultrafast \"{_tmp_file}\""
	fancy_print(f"🔧 Sto \033[35mConvertendo\033[0m il file in CFR ({_input_file})", command)

	os.system(command)
	shutil.move(_tmp_file, _output_file)

 
def speed(_input_file):
	filename, file_extension = os.path.splitext(_input_file)	# recupero il filename ed estensione
	name = os.path.basename(filename)
	tmp_path= tempfile.gettempdir()
 
	_tmp_output = f"{tmp_path}/{name}{file_extension}"			# creo il nome del file di output temporaneo

	# decode
	_t 	 = f"-t 180" if (args.preview)  else "" 				# modalità preview
	
	pts = 1/args.x
	command = f'{FFMPEG_CMD} -y -ignore_chapters 1 -i "{_input_file}" {_t} -hide_banner -filter:v "setpts=PTS*{pts}" -filter:a "atempo={args.x}"  -preset ultrafast {_tmp_output}'
	fancy_print(f"🚀 Sto \033[33mvelocizzando\033[0m il video ({_input_file})", command)
	os.system(command)
	# os.replace(_tmp_output, _input_file)
	shutil.move(_tmp_output, _input_file)



# taglia il file
def cut(__file__):
	filename, file_extension = os.path.splitext(__file__)		# recupero il filename ed estensione	
	output = f"{filename}{TMP_FILE_MARK}{file_extension}"		# creo il nome del file di output
	input_file = __file__
 
	if(check_variable_framerate(__file__)):
		input_file = f"{filename}[CFR]{file_extension}"
		convert_to_cfr(__file__, input_file)
  
	# decoding delle impostazioni per ffmpeg	
	_fr  = f"-r {args.fr}" if (args.fr) else ""	# framerate
	_vfr = f"-vsync vfr" if (args.vfr)  else ""	# framerate
	_t 	 = f"-t 180" if (args.preview)  else "" # modalità preview
 

	# eseguo remsi per la rilevazione dei silenzi
	fancy_print(f"💡 Sto \033[93mgenerando\033[0m il comando di taglio ({__file__})")
	remsi.elaborate(input_file, FFMPEG_CMD, args.n, args.d)
 
	name 		= os.path.basename(filename)
	tmp_path	= tempfile.gettempdir()
	_tmp_output = f"{tmp_path}/{name}{TMP_FILE_MARK}{file_extension}"
 
	# eseguo il comando di taglio
	command = f'{FFMPEG_CMD} -y -ignore_chapters 1 -i "{input_file}" {_t} -hide_banner -filter_script:v "{tmp_path}/vfilter.txt" -filter_script:a "{tmp_path}/afilter.txt" {_vfr} {_fr} -metadata comment="edited" "{_tmp_output}"'
	fancy_print(f"✂️ Sto \033[94mtagliando\033[0m il file ({__file__})", command)
	os.system(command)
	shutil.move(_tmp_output, output)
 
	if(not args.keep_cfr and os.path.exists(f"{filename}[CFR]{file_extension}")):
		os.remove(f"{filename}[CFR]{file_extension}")
	elif (args.preview):
		os.remove(f"{filename}[CFR]{file_extension}")
     
  
	# restituisci il nome del file di output
	return output

def sort(lst):
    lst = [str(i) for i in lst]
    lst.sort()
    lst = [int(i) if i.isdigit() else i for i in lst ]
    return lst

# =================== MAIN ===================
if __name__ == "__main__":
	path = args.path						# recupero il nome della cartella
	location = os.path.abspath(path)		# recupero la posizione della cartella
 
	if os.path.isdir(location):
		folder = location
  
	elif os.path.isfile(location):
		folder = os.path.dirname(location)
	
	# creo la cartella fatti se non presente
	if not os.path.exists(folder+f"/{ORIGINAL_FILES_DESTINATION_FOLDER}"):
        	os.makedirs(folder+f"/{ORIGINAL_FILES_DESTINATION_FOLDER}")

	# creo la cartella cut se non presente
	if not os.path.exists(folder+f"/{EDITED_FILES_DESTINATION_FOLDER}"):
        	os.makedirs(folder+f"/{EDITED_FILES_DESTINATION_FOLDER}")


	y = [] 
 
	# scansiono tutti i file della cartella
	if os.path.isdir(location):
		for path in os.scandir(location):
			filename, file_extension = os.path.splitext(path)
	
			if not path.is_file():
				continue

			if file_extension not in [".mp4", ",mkv"]:
				continue

			if TinyTag.get(path).comment == "cfr version":
				continue

			if TinyTag.get(path).comment == "edited":
				continue
			
			y.append(f"{filename}{file_extension}")
   
	elif os.path.isfile(location):
		y.append(location)

	z = sort(y)
 
	# per ogni video esaminato
	for i in z:		
		WORKING = i				# setto il file che sto elaborando
		filename = cut(i) 		# eseguo il taglio

		# verifico se è un video di teams
		# if (args.teams):
		#	filename = crop(filename, 62, 0, 1796, 972)
	
		# altrimenti aggiungo solo i metadata
		#else:
		#	filename = crop(filename)
  
		if(args.x != -1):
			speed(filename)

		# rimuovo i file inutili
		try:
			# calcolo i secondi risparmiati
			elapsed = durationDiff(i, filename)

			print("\n")
			fancy_print(f"✅ {i} \033[92mCompletato!\033[0m Sono stati risparmiati {elapsed} minuti")
   
			if(not args.preview):
				edited_file = filename.replace(TMP_FILE_MARK, EDITED_FILE_MARK)
			else:
				edited_file = filename.replace(TMP_FILE_MARK, "[PREVIEW]")
   
			# elimino il file junk senza crop e metadata
			os.replace(filename, edited_file)
			tmp_path= tempfile.gettempdir()
			os.remove(f"{tmp_path}/afilter.txt")
			os.remove(f"{tmp_path}/vfilter.txt")
   
			if (not args.preview):
				# sposto in cut il file elaborato
				pos = os.path.abspath(location + f"/{EDITED_FILES_DESTINATION_FOLDER}/" + os.path.basename(edited_file))
				os.replace(edited_file, pos)

				# sposto il file originale
				pos = os.path.abspath(location + f"/{ORIGINAL_FILES_DESTINATION_FOLDER}/" + os.path.basename(i))
				os.rename(i, pos)
    
   
		except Exception as e:
			print(f"errore: {e}")
			print("⚠️ Non ho spostato il file " + i+ " perchè già presente nella cartella degli originali.")