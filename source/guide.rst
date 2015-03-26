====================
Guide du développeur
====================

#########
Fichiers
#########

Cette section permet de s'y retrouver dans la multitude de fichiers du projet et de comprendre certains processus.

* courses/
    * **admin.py**: permet de rajouter les modèles que l'on veut voir apparaitre et modifier dans la zone d'administration Django. `Documentation officielle <https://docs.djangoproject.com/fr/1.7/ref/contrib/admin/>`__ [#f1]_
    * **api.py**: regroupe toutes les vues génériques RestLess qui servent à construire l'API JSON nécessaire à l'application AngularJS. Les classes déclarées sont ensuite utilisées dans le fichier ``urls.py``.
    * **forms.py**: déclare les formulaires Django nécessaires pour enregistrer les données d'une requête dans la base de données. Ils sont utilisés principalement dans le fichier `api.py`. `Documentation officielle <https://docs.djangoproject.com/fr/1.7/topics/forms/>`__ [#f2]_
    * **models.py**: déclare les modèles de notre application. Contient également des méthodes d'instance pour certains modèles. `Documentation officielle <https://docs.djangoproject.com/fr/1.7/topics/db/models/>`__ [#f3]_
    * **urls.py**: contient les URL spécifiques à l'application. Elles sont ensuite ajoutées dans le fichier principal ``webmath/urls.py``. La première url, de nom ``index``, est le point de départ de notre application AngularJS. Le reste des routes est défini directement par AngularJS dans le fichier ``courses/static/courses/javascripts/config/routes.js``. Dans ``urls.py``, la deuxième url, de nom ``pdf``, est celle qui génère le PDF d'un cours. Les routes qui suivent sont celles de l'API JSON qui utilisent les vues génériques du fichier ``api.py``. `Documentation officielle <https://docs.djangoproject.com/fr/1.7/topics/http/urls/>`__ [#f4]_
    * **utils.py**: regroupe une série de fonctions utiles utilisées à travers l'application.
    * **views.py**: contient les vues Django. A l'instar des URL, il n'y a que deux fonctions, une qui est le point de départ de l'application et l'autre qui génère le PDF d'un cours. `Documentation officielle <https://docs.djangoproject.com/fr/1.7/topics/http/views/>`__ [#f5]_

* **courses/templates/courses/**: contient le gabarit de base ``courses.html`` de notre application et le fichier Markdown ``pdf.md`` servant à générer le PDF d'un cours.

* courses/static/courses/
    * **html/**: contient tous les fichiers HTML utilisés par AngularJS. Les pages HTML sont reliées à une route dans le ficher ``courses/static/courses/javascripts/config/routes.js`` d'AngularJS qui s'occupe d'associer une route à un fichier HTML.

    * **images/**: contient les images utilisées pour le design de l'application.

    * **stylesheets/**: contient les feuilles de styles.

* courses/static/courses/javascripts/:
    * **config/routes.js**: déclare les routes principales de notre application avec AngularJS. `Documentation officielle <https://docs.angularjs.org/tutorial/step_07>`__ [#f6]_
    * **controllers/**: déclare les contrôleurs AngularJS. Un fichier correspond à une route et son contrôleur. Ils sont utilisés dans le fichier ``courses/static/courses/javascripts/config/routes.js``.
    * **directives/**: déclare des directives AngularJS. `Documentation officielle <https://docs.angularjs.org/guide/directive>`__ [#f7]_
    * **factories/resources.js**: déclare des objets ressources qui permettent de communiquer facilement avec l'API. `Documentation officielle <https://docs.angularjs.org/api/ngResource/service/$resource>`__ [#f8]_
    * **filters/**: déclare des filtres AngularJS. `Documentation officielle <https://docs.angularjs.org/guide/filter>`__ [#f9]_
    * **app.js**: point de départ, déclare l'application AngularJS principale ainsi que les modules avec leurs dépendances. C'est dans ces modules qu'on ajoute ensuite les filtres, contrôleurs, etc.
    * **extensions.js**: permet de personnaliser Showdown.js, la bibliothèque qui transforme le Markdown en HTML. `Documentation officielle <https://github.com/showdownjs/showdown>`__ [#f10]_

* **spec/conf.js**: fichier de configuration de Protractor, le moteur de test.

* **spec/**: contient les fichiers de tests end-to-end Protractor. Chaque fichier correspond à une route de l'application.

* management/commands/
    * `Documentation officielle <https://docs.djangoproject.com/fr/1.7/howto/custom-management-commands/>`__ [#f11]_
    * **seed.py**: commande qui crée des données de démonstration dans la base de données afin d'avoir une application fonctionnelle.
    * **tests.py**: commande qui lance les tests Protractor.

* **webmath/test_router.py**: Le routeur permet d'utiliser plusieurs bases de données avec Django. En l'occurrence, le routeur permet d'utiliser une base de données différente lorsqu'on lance les tests de notre application. `Documentation officielle <https://docs.djangoproject.com/fr/1.7/topics/db/multi-db/>`__ [#f12]_

####
URL
####

Cette section regroupe une explication de toutes les URL de l'application. Toutes les URL se trouvent dans l'espace de nom ``courses``, par exemple ``/courses/help``. Lorsque un ``#`` se trouve dans l'URL, cela signifie que c'est une URL définie par AngularJS.

*************
Utilisateurs
*************

* **#/**: Page d'accueil de l'application, on y trouve une liste des cours publiés. Ils peuvent être triés par catégories ou favoris.

* **#/new**: Page qui permet aux enseignants de créer un nouveau cours.

* **#/:course_id/edit/:page**: Page d'édition d'un cours. L'enseignant peut y éditer le contenu de son cours, le publier ou le retirer.

* **#/:course_id/preview/:page**: Prévisualise une page d'un cours. Lorsqu'un enseignant rédige un cours, il peut voir le résultat final grâce à cette page.

* **#/teacher/courses:** Liste de tous les cours du site, publiés ou non.

* **#/help**: Page qui fournit une aide aux rédacteurs concernant la syntaxe *Markdown* et *LaTex*.

* **#/:course_id/edit**: Page qui permet de modifier les informations de base d'un cours, telles que le nom, la description ou la difficulté.

* **#/:course_id/show/:page**: Page pour lire un cours. Le cours y est affiché, on peut naviguer à travers les pages, commenter le cours, etc.

* **/pdf/:course_id/*.pdf**: Renvoie un cours au format PDF pour pouvoir être téléchargé.

* **#/about**: Page d'information générale sur l'application.

******
API
******

Les URLs de l'API sont dans l'espace de nom ``api``, par exemple ``/courses/api/themes``.

* **/courses/all**: renvoie une liste de tous les cours, publiés ou non.

* **/courses**

    * GET: renvoie tous les cours publiés.
    * POST: crée un nouveau cours.

* **/courses/:id**

    * PUT: met à jour un cours.

* **/pages/:page_id/courses/:course_id**:

    * GET: renvoie le contenu d'une page d'un cours.
    * PUT: met à jour le contenu d'une page.

* **/themes**: renvoie une liste de tous les thèmes en incluant leurs chapitres respectifs.

* **/pages/:page_id/sections**

    * POST: ajoute une section à une page d'un cours.

* **/courses/:course_id/pages**

    * POST: ajoute une page à un cours.

* **/sections/:id**

    * DELETE: supprime une section.

* **/courses/:course_id/comments**

    * GET: renvoie les commentaires d'un cours.
    * POST: ajoute un commentaire à un cours.

* **/courses/:course_id/menu**: Permet de construire le menu d'un cours en renvoyant le nom de ses pages et de leurs sections.

* **/courses/:course_id/publish**

    * PUT: publie/retire un cours en changeant l'attribut ``published`` de ``True`` à ``False`` et vice-versa.

* **/courses/:course_id/favorite**

    * PUT: ajoute/retire un cours au/des favoris de l'utilisateur.

* **/pages/:page_id/progression**

    * POST: marque une page d'un cours comme comprise ou à relire pour l'utilisateur.

########
Concepts
########

************************************
Intégration d'AngularJS avec Django
************************************

En dehors de l'API et des PDF, Django ne fournit qu'une seule route dans l'application. En effet, à partir de cette route, Angular s'occupe de gérer les autres routes et les templates. Concrètement, lorsqu'on charge une page de notre application, la requête va d'abord passer par la vue Django ``index`` déclarée dans le fichier `views.py`. Cette vue s'occupe simplement d'afficher le template ``courses.html``. Ce fichier HTML est un layout pour notre application, c'est-à-dire que son contenu est sur toutes les pages. Il contient le menu, l'inclusion des fichiers JavaScript et des feuilles de syle, ainsi que le pied de page. Dans la balise ``body``, on a ajouté la directive Angular ``ng-app=Courses``. On déclare qu'à l'intérieur de cette balise se trouve une application AngularJS nommée ``CoursesApp``. Ainsi, une fois que Django a affiché le template ``courses.html``, Angular va insérer le contenu du bon fichier HTML dans la balise ``body`` selon l'URL et les routes écrites dans le fichier ``routes.js``. La page finale est maintenant visible par l'utilisateur. Par exemple, si l'on se rend sur ``courses/help``, Angular s'occupe de chercher le fichier ``help.html`` et d'insérer son contenu dans la balise ``body`` de ``courses.html``. L'avantage de ce système est que lorsqu'on change de page, la vue Django n'est pas rappelée, mais seul le contenu de `body` est mis à jour avec le contenu HTML approprié à l'URL. AngularJS rend ainsi notre site web plus rapide.


.. [#f1] https://docs.djangoproject.com/fr/1.7/ref/contrib/admin. Consulté le 14 mars 15.
.. [#f2] https://docs.djangoproject.com/fr/1.7/topics/forms/. Consulté le 14 mars 15.
.. [#f3] https://docs.djangoproject.com/fr/1.7/topics/db/models/. Consulté le 14 mars 15.
.. [#f4] https://docs.djangoproject.com/fr/1.7/topics/http/urls/. Consulté le 14 mars 15.
.. [#f5] https://docs.djangoproject.com/fr/1.7/topics/http/views/. Consulté le 14 mars 15.
.. [#f6] https://docs.angularjs.org/tutorial/step_07. Consulté le 14 mars 15.
.. [#f7] https://docs.angularjs.org/guide/directive. Consulté le 14 mars 15.
.. [#f8] https://docs.angularjs.org/api/ngResource/service/$resource. Consulté le 14 mars 15.
.. [#f9] https://docs.angularjs.org/guide/filter. Consulté le 14 mars 15.
.. [#f10] https://github.com/showdownjs/showdown. Consulté le 14 mars 15.
.. [#f11] https://docs.djangoproject.com/fr/1.7/howto/custom-management-commands/. Consulté le 14 mars 15.
.. [#f12] https://docs.djangoproject.com/fr/1.7/topics/db/multi-db/. Consulté le 15 mars 15.