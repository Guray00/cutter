# Cutter
Utility per la compressione e ritaglio dei silenzi all'interno delle lezioni. 

Basato sul lavoro svolto da [Remsi](https://github.com/bambax/Remsi), prende in input il path di una cartelle ed esegue il taglio di tutti i video indicati.

Per riconoscere un silenzio sono stati usati, di default, i seguenti parametri:

|Parametro| valore|
|----|-----|
|Durata| 0.8 secondi|
| Tolleranza| -40db |

_Nota: più è basso in modulo la tolleranza più è semplice il taglio, esempio: -40db taglia maggiormente di -50db_

## Parametri
```text
--teams 	# esegue il crop del video eliminando le bande nere di teams (versione 2021)
```

## Installazione

Clona questa repo in una cartella comoda:
```bash
https://github.com/Guray00/squeeze
```

Entra nella cartella:
```bash
cd squeeze
```

Installa le dipendenze:
```bash
pip install -r ./requirements.txt
```
Sei pronto per l'utilizzo!

## Utilizzo
Per eseguire il programma è sufficiente:
```bash
python3 cutter.py "path-to-folder"
```
Mentre le opzioni possiibili sono:
```text
usage: cutter.py [-h] [--teams] [-d D] [-n N] foldername

positional arguments:
  foldername  video file name (or full file path) to classify

options:
  -h, --help  show this help message and exit
  --teams     crops the video
  -d D        duration of silence in seconds
  -n N        noise level in dB
```

Tutti i file `.mp4` o `.mkv` della cartella verranno elaborati. Con il parametro `--teams` si esegue anche un crop per ritagliare i file di teams.

I file originali verranno spostati in `fatti` mentre le versioni tagliate in `cut`.