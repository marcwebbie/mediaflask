### Installer MediaFlask

```
# creer un environment virtuel
virtualenv -p /usr/bin/python3 env_mediaflask

# rentrer dans l'environment virtuel
cd env_mediaflask

# cloner le code source du projet
git clone https://bitbucket.org/marcwebbie/mediaflask

# activer l'environment virtuel
source bin/activate

# rentrer dans le dossier avec le code source
cd mediaflask

# installer les requirement
pip install -U requeriments.txt

# installer pydub
pip install -U https://github.com/marcwebbie/pydub/tarball/master
```

### Mètre-a-jour MediaFlask

```
# rentrer dans l'environment virtuel
cd env_mediaflask

# activer l'environment virtuel
source bin/activate

# rentrer dans le dossier avec le code source
cd mediaflask

# mètre-à-jour pydub
pip install -U https://github.com/marcwebbie/pydub/tarball/master

# mètre-à-jour youtube-dl
pip install -U youtube_dl

# PULLER les dernièrs modifications
git pull origin master
```


### Executer MediaFlask

```
# rentrer dans l'environment virtuel
cd env_mediaflask

# activer l'environment virtuel
source bin/activate

# rentrer dans le dossier avec le code source
cd mediaflask

# demarrer la version desktop
python3 desktop/app.py

# demarrer la version web local
python3 app.py
```


### Autres infos

Mediaflask web démarre sur la porte '5000'. Pour acceder à l'application il faudra aller sur 127.0.0.1:5000

```
# pour trouver votre addresse ip local:
ip addr | grep inet

# pour trouver votre addresse ip externe
curl -s icanhazip.com
```