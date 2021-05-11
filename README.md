# Squeeze
Software di compressione video ed editor automatizzato per le lezione online.
Al momento è implementato mediante due differenti script:
- cutter: si occupa di ritagliare (crop) i video in modo da eliminare la fastidiosa banda nera sotto i file di teams
- squeeze: comprime con alta fedeltà in h265 i file

## Utilizzo
Semplice invocazione
```bash
python3 cutter.py "path-to-folder"
```

Tutti i file mp4 o mkv della cartella verranno elaborati. Con il parametro `--teams` si esegue anche un crop per ritagliare i file di teams, mentre con `--generate-training-data` vengono memorizzati i file di training per la rete neurale in modo da identificare i falsi positivi e segnalarli.
