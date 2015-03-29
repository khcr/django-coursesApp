# TM 2014-15 Keran Kocher

Application de gestion de cours.
Pour les commandes qui concernent l'application, veiller à les lancer à la racine du projet.

**Prérequis**

* Python 3 et pip installés

**Installer Django et les dépendances**

``pip3 install -r requirements.txt``

De plus, il faut encore installer ces paquets sur la machine:

* pandoc
* pdflatex

**Lancer les migrations**

``python3 manage.py migrate``

**Créer un super utilisateur**

S'il y a besoin de se connecter à la zone d'administration (``/admin``)

``python3 manage.py createsuperuser`` et suivre les instructions

**Lancer le serveur Django**

``python3 manage.py runserver``

**Données**

* Créer les données nécessaires: ``python3 manage.py seed``
* Finalement, vous pouvez vous rendre sur l'URL ``/courses`` et profitez des fonctionnalités.
* Identifiant pour se connecter en tant qu'enseignant: ``smith.john`` et ``12341``
* Identifiant pour se connecter en tant qu'étudiant: ``dupont.alfred`` et ``12341``

**Tests**

Pour lancer les tests, installer d'abord Protractor (ne pas lancer le serveur webdriver): http://angular.github.io/protractor/#/tutorial

Ensuite, lancer la commande ``python3 manage.py tests``.