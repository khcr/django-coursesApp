====================
Guide du développeur
====================

#########
Fichiers
#########

Cette page permet de se retrouver dans la multitude de fichiers du projets et de pouvoir comprendre certain processus.

* courses/
    * **admin.py**: permet de rajouter les modèles qu'on veut voir apparaitre et modifier dans la zone d'administration Django. `Documentation officielle <https://docs.djangoproject.com/fr/1.7/ref/contrib/admin/>`__ [#f1]_
    * **api.py**: regroupe toutes les vues génériques RestLess qui servent à construire l'API JSON nécessaire à l'application AngularJS. Les classés déclarées sont ensuite utilisées dans le fichier `urls.py`.
    * **forms.py**: déclare les formulaires Django nécessaire pour enregistrer les données d'une requête dans la base de données. Ils sont utilisé principalement dans le fichier `api.py`. `Documentation officielle <https://docs.djangoproject.com/fr/1.7/topics/forms/>`__ [#f2]_
    * **models.py**: déclare les modèles de notre application. Contient également des méthodes d'instance pour certains modèles. `Documentation officielle <https://docs.djangoproject.com/fr/1.7/topics/db/models/>`__ [#f3]_
    * **urls.py**: contient les urls spécifiques à l'application. Elles sont ensuite ajoutée dans le fichier principal `webmath/urls.py`. La première url, de nom `index`, est la point de départ de notre application AngularJS. Le reste des routes est défini directement par AngularJS dans le fichier `courses/static/courses/javascripts/config/routes.js`. Dans `urls.py` la deuxième url, de nom `pdf`, est celle qui génère le pdf d'un cours. Les routes qui suivent sont celle de l'API JSON qui utilisent les vues génériques du fichier `api.py`. `Documentation officielle <https://docs.djangoproject.com/fr/1.7/topics/http/urls/>`__ [#f4]_
    * **utils.py**: regroupe une série de fonctions utiles utilisées à travers l'application.
    * **views.py**: contient les vues Django. A l'instar des urls, il n'y a que deux fonctions, une qui est le point de départ de l'application et l'autre qui génère le pdf d'un cours. `Documentation officielle <https://docs.djangoproject.com/fr/1.7/topics/http/views/>`__ [#f5]_

* **courses/templates/courses/**: contient le layout de base `courses.html` de notre application et le fichier markdown `pdf.md` servant à générer le pdf d'un cours.

* courses/static/courses/
    * **html/**: contient tous les fichiers html utilisés par AngularJS. Les pages html sont relié à une route dans le ficher `courses/static/courses/javascripts/config/routes.js` d'AngularJS qui s'occupe d'associer une route à un fichier html.

    * **images/**: contient les images utilisées dans le design de l'application.

    * **stylesheets/**: contient les feuilles de styles.

* courses/static/courses/javascripts/:
    * **config/routes.js**: déclare les routes principales de notre application avec AngularJS. `Documentation officielle <https://docs.angularjs.org/tutorial/step_07>`__ [#f6]_
    * **controllers/**: déclare les controlleurs AngularJS. Un fichier correspond à une route et son controlleur. Ils sont utilisé dans le fichier `courses/static/courses/javascripts/config/routes.js`.
    * **directives/**: déclare des directives AngularJS. `Documentation officielle <https://docs.angularjs.org/guide/directive>`__ [#f7]_
    * **factories/resources.js**: déclare des objets resources qui permettent de communiquer facilement avec l'API. `Documentation officielle <https://docs.angularjs.org/api/ngResource/service/$resource>`__ [#f8]_
    * **filters/**: déclare des filtres AngularJS. `Documentation officielle <https://docs.angularjs.org/guide/filter>`__ [#f9]_
    * **app.js**: point de départ, déclare l'application AngularJS et les modules avec leurs dépendances. C'est dans ces modules qu'on déclare ensuite les filtres, controlleurs, etc.
    * **extensions.js**: permet de personnaliser Showdown.js, la bibliothèque qui transforme le markdown en HTML. `Documentation officielle <https://github.com/showdownjs/showdown>`__ [#f10]_

* **spec/conf.js**: fichier de configuration de Protractor, le moteur de test.

* **spec/**: contient les fichiers de tests end-to-end Protractor. Chaque fichier correspond à une route de l'application.

* management/commands/
    * `Documentation officielle <https://docs.djangoproject.com/fr/1.7/howto/custom-management-commands/>`__ [#f11]_
    * **seed.py**: commande qui crée des données de démonstration dans la base de données afin d'avoir une application fonctionnelle.
    * **tests.py**: commande qui lance les tests Protractor.

* **webmath/test_router.py**: Le routeur permet d'utiliser plusieurs bases de données avec Django. En l'occurence, le routeur permet d'utiliser une base de données différente lorsqu'on lance les tests de notre application. `Documentation officielle <https://docs.djangoproject.com/fr/1.7/topics/db/multi-db/>`__ [#f12]_


########
Concepts
########

************************************
Intégration d'AngularJS avec Django
************************************

En dehors de l'API et des pdfs, Django ne fournit qu'une seule route dans l'application. En effet à partir de cette route Angular s'occupe de gérer les routes et les templates. Concrétement quand on charge une une page de notre application, la requête va d'abord passer par la vue Django `index` déclaré dans le fichier `views.py`. Cette vue s'occupe simplement d'afficher le template `courses.html`. Ce fichier HTML est un layout pour notre application, son contenu sera sur toutes les pages. Il contient le menu, l'inclusion des fichiers javascripts et des feuilles de syles ainsi que le pied de page. Dans la balise `body` on a ajouté la directive Angular `ng-app=Courses` pour déclarer qu'à l'intérieur de cette balise se trouve une application AngularJS nommée `CoursesApp`. Ainsi une fois que Django a affiché le template `courses.html`, Angular, grâce aux routes écrites dans le fichier `routes.js`, va insérer le contenu du bon fichier HTML dans la balise `body` selon l'URL. La page final est maintenant visible pour l'utilisateur. L'avantage de ce sytème est que lorsqu'on change de page, la vue Django ne sera pas rappelée mais seul le contenu de `body` sera mis à jour avec le contenu HTML approrié à l'URL. AngularJS rend notre site web plus rapide.

.. rubric:: Notes

.. [#f1] https://docs.djangoproject.com/fr/1.7/ref/contrib/admin
.. [#f2] https://docs.djangoproject.com/fr/1.7/topics/forms/
.. [#f3] https://docs.djangoproject.com/fr/1.7/topics/db/models/
.. [#f4] https://docs.djangoproject.com/fr/1.7/topics/http/urls/
.. [#f5] https://docs.djangoproject.com/fr/1.7/topics/http/views/
.. [#f6] https://docs.angularjs.org/tutorial/step_07
.. [#f7] https://docs.angularjs.org/guide/directive
.. [#f8] https://docs.angularjs.org/api/ngResource/service/$resource
.. [#f9] https://docs.angularjs.org/guide/filter
.. [#f10] https://github.com/showdownjs/showdown
.. [#f11] https://docs.djangoproject.com/fr/1.7/howto/custom-management-commands/
.. [#f12] https://docs.djangoproject.com/fr/1.7/topics/db/multi-db/