# Cutter
Utility per la compressione e ritaglio dei silenzi all'interno delle lezioni. 

Basato sul lavoro svolto da [Remsi](https://github.com/bambax/Remsi), prende in input il path di una cartelle ed esegue il taglio di tutti i video indicati.

Per riconoscere un silenzio sono stati usati i seguenti parametri:

|Parametro| valore|
|----|-----|
|Durata| 0.75 secondi|
| Tolleranza| -40db |

## Parametri
```text
--teams 	# esegue il crop del video eliminando le bande nere di teams (versione 2021)
```

## Installazione

Clona la questa repo in una cartella comoda:
```bash
https://github.com/Guray00/squeeze
```

Entra nella cartella:
```bash
cd squeeze
```

Installa le dipendenze
```bash
pip install -r .\requirements.txt
```
Sei pronto per l'utilizzo!

## Utilizzo
Per eseguire il programma è sufficiente:
```bash
python3 cutter.py "path-to-folder"
```

Tutti i file mp4 o mkv della cartella verranno elaborati. Con il parametro `--teams` si esegue anche un crop per ritagliare i file di teams.

I file originali verranno spostati in `fatti` mentre le versioni tagliate in `cut`