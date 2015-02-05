# TM2014 Keran Kocher

Application de gestion de cours.

## Démarrage

**Pré-requis**

* Python 3 installé et pip

**Installer Django et les dépendences**

``pip3 install -r requirement.txt``

**Lancer les migrations**

``python3 manage.py migrate``

**Créer un super utilisateur**

``python3 manage.py createsuperuser`` et suivre les instructions

**Lancer le serveur Django**

``python3 manage.py runserver``

**Données**

Se connecter à la zone admin - ``/admin`` - et ajouter au moins un thème (Themes) et un chapitre (Chapters) dans la base de données. Ensuite créer un professeur (dans la section Teachers sous le nom Users). Finalement vous pouvez vous rendre sur l'URL ``/courses`` et profiter des des fonctionnalités.