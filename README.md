# TM2014 Keran Kocher

Application de gestion de cours.

## Démarrage

**Pré-requis**

* Python 3 installé et pip

**Installer Django et les dépendences**

``pip3 install -r requirement.txt``

De plus, il faut encore installer ces paquets sur la machine:
* cairo
* pango
* GDK-PixBuf
* Plus d'info: http://weasyprint.org/docs/install/

**Lancer les migrations**

``python3 manage.py migrate``

**Créer un super utilisateur**

``python3 manage.py createsuperuser`` et suivre les instructions

**Lancer le serveur Django**

``python3 manage.py runserver``

**Données**

* Se connecter à la zone admin - ``/admin`` 
* Ajouter au moins un thème (Themes) et un chapitre (Chapters) dans la base de données. 
* Créer un professeur (dans la section Teachers sous le nom Users).
* Créer deux status (Statuss): un "Relire" et l'autre "Compris"
* Finalement vous pouvez vous rendre sur l'URL ``/courses`` et profiter des des fonctionnalités.