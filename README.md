# Task Track

## Prezentare generală

Task Track este un program care faciliteaza gestionarea de sarcini in cadrul academic. Acesta permite utilizatorului sa isi introduca si gestioneze sarcinile pe care le are. Sarcinile disponibile sunt prestabilite: 'lucrare de laborator', 'lucrare practica' si lucrare individuala. Sarcinile au 3 etape iar fiecare etapa are propriul sau statut: 'not started', 'unfinished', 'finished', 'not presented' si 'presented'. Datele despre sarcini sunt salvate in o baza de date numta 'tasks.db' cu care programul opereaza direct. Programul are un GUI interactiv pentru a usura utilizarea acestuia.

## Funcționalități

- **Gestionarea unei baze de date:** Suport deplin pentru a opera cu baze de date.
- **Gestionare de sarcini:** Afisarea si modificarea sarcinilor in GUI.
- **Implementare serviciul Dropbox:** Utilizatorul are posibilitatea sa salveze baza de date utilizand serviciile de cloud storage ale Dropbox.
- ~~**Colectare automata a datelor:**~~ Programul poate colecta automat, dupa autentificarea manuala, date despre sarcini de pe website-ul oficial ELSE si cheia de API proprie oferita de Dropbox de pe website-ul lor. 

## Dependențe

- `bs4`
- `selenium`
- `dropbox`

## Instalare

1. **Clonează Repositoriul:**
```bash
git clone https://github.com/MariusC-UTM/Task-Track.git
```

2. **Instalează Bibliotecile Necesare:**
```bash
pip install -r requirements.txt
```

3. **Rulează Programul:**
```bash
python TaskTrack.py
```
sau
```bash
python3 TaskTrack.py
```

## Utilizare

1. **Rularea programului Task Track:**
    - .

2. **Easter Egg:**
    - .

3. **:**
    - .

## Structura Proiectului

- **TaskTrack.py:** .
- **gui.py:** .
- **database.py:** .
- **api.py** .
- **scraper.py** .
