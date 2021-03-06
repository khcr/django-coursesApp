===========
RestLess
===========

#############
Présentation
#############

`RestLess <https://github.com/dobarkod/django-restless>`_ [#f1]_ est un set d'outils permettant de faciliter l'implémentation d'une API JSON dans Django. Il a l'avantage d'être léger et facile à utiliser comme nous le verrons par la suite. Une API, Application Programming Interface, est basiquement une application qui offre des services accessibles par une autre application. Le JSON est un format de données dans le style d'un dictionnaire ``{"nom" : "Keran", "prenom" : "Kocher"}``. On appelle donc une API JSON une application qui fournit des données en format JSON. Concrètement, il s'agit d'une série d'URL qui fournissent le contenu de différentes tables de la BD en format JSON. Quand on se rend sur une de ces URL, on ne voit pas une page HTML, mais simplement un dictionnaire de données. Sur notre site web rendez-vous sur ``http://webmath.com/courses/api/themes`` pour voir à quoi ressemble la page.

Dans la présentation d'AngularJS, nous avons vu que le framework n'est pas capable de communiquer directement avec une base de données. C'est une limitation de JavaScript, qui s'exécute du côté du client dans notre cas. Pour palier à ce problème, on utilise un langage intermédiaire qui est capable de communiquer avec une BD et qui s'exécute côté serveur, c'est le cas de Python et son framework Django. On va donc construire une API avec Django. API à laquelle notre application AngularJS va pouvoir accéder. Dans les fait, Django va chercher les données dans la base de données, les transforme en format JSON puis les sert. Il suffit ensuite avec AngularJS d'accéder à l'URL correspondante et l'on dispose ensuite des données que l'on peut utiliser à sa guise dans nos vues AngularJS.

###################
Les vues génériques
###################

Lorsqu'on développe une application web, cela donne souvent un code redondant, répétitif. En effet, quand on crée des fonctionnalités, il s'agit généralement d'une table dans la base de données, avec laquelle on communique pour ajouter ou modifier des données. Et ces interactions se ressemblent dans la plupart des cas. On parle généralement du CRUD: create, read, update and delete, en français créer, lire, mettre à jour et supprimer. On a une table et on veut accomplir les opérations CRUD dessus. Pour ce faire, l'on a une série d'URL qui exécutent différentes actions. Prenons l'exemple de la création d'un blog tout à fait typique. On va créer une table ``articles``, et implémenter les actions suivantes: on veut pouvoir afficher tous les articles, ou n'en afficher qu'un seul, ajouter un nouvel article, le mettre à jour ou le supprimer. Ainsi, avec ces quatre opérations, l'on peut disposer d'un blog complet et fonctionnel. Pour beaucoup de fonctionnalités, il s'agit d'effectuer toujours ces mêmes opérations classiques; un autre exemple serait un système de commentaires. Pour programmer ces outils basiques et conventionnels, deux moyens sont à notre disposition dans Django. D'abord, l'on peut programmer les opérations de A à Z. Avec Django, il s'agit basiquement de créer une URL et de lui assigner une fonction qui s'occupe de communiquer avec la base de données, et qui retourne une page HTML. Si l'on utilise cette méthode, on risque de devoir programmer souvent le même code au fil du développement et de perdre du temps. Ci-dessous le code pour afficher tous les articles avec la première méthode.

.. code-block:: python
    
    # urls.py - fichier qui gère les URL du site

    from django.conf.urls import patterns, url, include

    from courses import views

    # On crée une URL /articles qui utilise la fonction index - voir fichier views.py
    urlpatterns = patterns('',
        url(r'^articles$', views.index),
    )

    # views.py - fichier qui contient les fonctions liées aux URL
    # = vue ou contrôleur

    from django.shortcuts import render

    # Fonction reliée à /articles
    def index(request):
        # Récupère tous les articles de la BD (fait appelle au modèle Article)
        articles = Article.objects.all()
        # Retourne le code HTML en utilisant le ficher courses.html
        return render(request, "courses/courses.html", locals())


La deuxième méthode consiste à utiliser les vues génériques. Ce sont des classes dans Django contenant les opérations conventionnelles déjà écrites. Il nous suffit donc de créer notre propre classe qui hérite d'une vue générique Django et d'ensuite la relier à notre URL, comme on le faisait précédemment avec la fonction. Pourquoi créer une classe et ne pas utiliser directement les classes Django ? On agit ainsi tout simplement pour pouvoir personnaliser la classe. Il faut déjà obligatoirement spécifier le modèle que doit utiliser la classe, par exemple pour savoir quels enregistrements elle doit aller récupérer. Regardons la même fonctionnalité qu'avant, mais écrite avec les vues génériques.

.. code-block:: python
    
    # urls.py - fichier qui gère les URL du site

    from django.conf.urls import patterns, url, include

    from courses.views import ArticlesList

    # On crée une URL /articles qui utilise la vue générique ArticlesList - voir fichier views.py
    urlpatterns = patterns('',
        url(r'^articles$', ArticlesList.as_view()),
    )

    # views.py - fichier qui contient les fonctions liées aux URL
    # = vue ou contrôleur

    from django.views.generic import ListView

    # La classe générique reliée à /articles
    # Hérite de ListView, classe provenant de Django
    class ArticlesList(ListView):

        # On spécifie le modèle à utiliser
        model = Article

Avec la seconde méthode, le code est plus concis. L'exemple montre comment générer la liste des articles, mais il existe une vue générique pour chaque opération CRUD. Il est encore possible de personnaliser notre classe ``ArticlesList`` avec des options ou en surchargeant les méthodes. En revanche, si notre fonctionnalité a des besoins spécifiques qui s'éloignent trop de la convention, les vues génériques ne sont plus adaptées, car leur personnalisation a évidemment des limites. Dans ces cas-ci, on retourne à la première méthode. Toutes les explications et options des vues génériques se trouvent dans la `documentation Django <https://docs.djangoproject.com/fr/1.7/topics/class-based-views/generic-display/>`_  [#f2]_.

##########################
Fonctionnement de RestLess
##########################

Nous avons étudié ce qu'étaient les vues génériques dans Django, parce que RestLess se base exclusivement sur ce concept pour construire une API JSON. En fait, RestLess fournit également des vues génériques qui sont des dérivées des classes Django. Les classes de RestLess font en effet exactement le même travail que celle de Django, à la différence qu'elles travaillent avec le format JSON. Ainsi, on peut construire facilement et rapidement notre API, en économisant du code et du temps. En revanche, Django possède beaucoup de vues génériques et RestLess n'offre que les plus utiles. Avant de nous intéresser aux classes que nous pouvons utiliser avec RestLess, il nous faut d'abord voir les différents types de requêtes qui existent dans le monde du web.

*****
HTTP
*****

HTTP est l'abréviation de *HyperText Transfer Protocol* qui veut dire *protocole de transfert hypertexte*. Ce protocole est utilisé sur internet pour la communication entre un client et un serveur. Le serveur est un ordinateur dont le rôle est de fournir le contenu désiré d'un site web. Le client est un navigateur utilisé par une personne qui navigue sur un site web. Lorsqu'un utilisateur visite une page, le navigateur demande au serveur la page HTML correspondante et ensuite il l'affiche à l'utilisateur. Pour établir le transfert de données, on utilise donc HTTP. Quand le client demande une information au serveur, on appelle cela une requête HTTP. Il y a plusieurs types de requêtes HTTP. Nous avons vu que le serveur envoie des données au client, mais le contraire est aussi vrai. Le client peut envoyer des données au serveur, quand il soumet un formulaire HTML par exemple. Ces différentes requêtes, formulées par un navigateur qui est le client, servent en général à agir sur une ressource en permettant notamment les opérations CRUD. On appelle une ressource une entité modifiable, souvent un enregistrement provenant d'une *BD*. La liste qui suit présente les différentes requêtes les plus importantes dans notre cas.

* GET: requête la plus courante, le serveur envoie les données au client, une page HTML par exemple. Aucune ressource modifiée.
* POST: le client envoie des données au serveur, souvent via un formulaire HTML. Le résultat est la création d'une ressource.
* PUT: le client envoie des données au serveur. Le résultat est la modification d'une ressource.
* DELETE: supprime une ressource.

.. figure:: images/http.png
    :scale: 100%
    :align: center

    Schéma de la communication avec HTTP entre un client et un serveur

Nous devons utiliser ces requêtes lorsqu'il s'agit de modifier nos ressources, c'est-à-dire les enregistrements de notre base de données. Par exemple on crée un cours, on le modifie ou on le supprime. Le travail de RestLess est de supporter ces requêtes. En clair, il doit fournir une URL et une fonction qui s'occupent de traiter les différents types de requêtes. Attention à ne pas confondre, une requête n'agit pas directement sur une ressource, c'est le serveur qui s'en occupe. La requête consiste juste en un transfert de données entre le client et le serveur et ainsi elle déclenche des actions.

********************
Les classes RestLess
********************

Maintenant que les bases sont en place, nous pouvons enfin nous intéresser à la liste des classes RestLess utilisées dans le projet avec les requêtes supportées et leur utilité.

* ListEndpoint
    
    * get: retourne toutes les ressources
    * post: crée une nouvelle ressource

* DetailEndpoint
    
    * get: retourne une ressource
    * put: met à jour la ressource
    * delete: supprime la ressource

* Endpoint

    * pour créer des actions spécifiques

La liste ci-dessus regroupe les trois vues génériques dont nos classes peuvent hériter. Elles permettent de réaliser les quatre opérations sur nos ressources ainsi que des actions personnalisées. La différence entre la classe ``DetailEndpoint`` et ``ListEndpoint`` est que la première agit sur une ressource particulière. Elle a donc besoin d'un identifiant dans l'URL pour savoir quelle ressource elle doit modifier, dans le style ``/courses/:id``. Notons qu'évidemment toutes les actions, le code qui s'exécute derrière une URL, retournent du JSON. En effet, il s'agit de la particularité et de l'utilité de RestLess. Comment concrètement utiliser ces classes dans le projet ? On fait comme précédemment dans l'exemple sur les vues génériques Django. La première étape consiste à créer une classe qui hérite soit de ``ListEndpoint``, de ``DetailEndpoint`` ou de ``Endpoint``. La seconde étape consiste à spécifier le modèle. Ensuite il faut créer une URL dans laquelle l'on spécifie qu'il faut utiliser notre classe précédemment déclarée. Ainsi. quand on fait une requête sur cette URL, suivant le type de requête, Django fait appel aux méthodes provenant des vues génériques RestLess. Par exemple, on crée une classe ``CoursesList`` dans laquelle on spécifie le modèle ``Course``. Ensuite on rattache cette classe à l'url ``/courses``. Si l'on fait une requête de type POST sur ``/courses``, Django va chercher la méthode ``post``, même nom que le type de requête, dans la classe ``CoursesList``. Comme il ne la trouve pas dans notre classe, il la cherche dans la classe parente ``ListEndpoint`` et l'exécute. On appelle ce principe l'héritage. Le résultat est qu'une ressource est créée dans la table ``courses`` avec les paramètres du client. Une réponse en JSON contenant la ressource créée est retournée. On peut également faire une requête GET sur ``/courses`` et le serveur retourne tous les cours en format JSON également. Rien n'est plus nécessaire pour avoir notre API JSON fonctionnelle.

.. figure:: images/requetes.png
    :scale: 90%
    :align: center

    Schéma du traitement d'une requête à l'aide des vues génériques RestLess

Dans le cas de notre projet, il a fallu personnaliser les vues génériques pour répondre aux besoins spécifiques des ressources. Pour ce faire, il faut surcharger les méthodes héritées des classes RestLess. Comme mentionné précédemment, les méthodes ont le nom de la requête à laquelle elles correspondent. Si l'on fait une requête PUT, la méthode ``put`` est appelée et ainsi de suite. C'est un principe des vues génériques Django. En ce qui concerne les vues génériques, si notre classe ne contient pas le méthode appelée par une requête, le framework va automatiquement chercher la méthode dans la classe parente. Celle-ci est la classe RestLess qui contient les méthodes classiques et conventionnelles qui nous évitent un code redondant. En revanche, si l'on ne veut plus utiliser ces méthodes classiques car elles ne sont plus adaptées, l'on crée alors une méthode de même nom dans la classe fille. Cette méthode est desormais appelée à la place de celle de la classe mère. On appelle cela surcharger une méthode. Dans le projet, toutes les vues génériques sont écrites dans le fichier ``api.py``. On peut y observer que plusieurs méthodes de tous types ont été surchargées. Il faut s'inspirer des méthodes RestLess que l'on surcharge pour que la nouvelle méthode accepte les bons arguments et retourne une réponse valide. On retrouve le fichier source sur `la documentation RestLess <https://django-restless.readthedocs.org/en/latest/_modules/restless/modelviews.html>`_ [#f3]_.

.. figure:: images/surcharge.png
    :scale: 90%
    :align: center

    Surcharge d'une méthode

On doit parfois retourner des objets JSON personnalisés, c'est-à-dire pouvoir choisir les paires clé/valeur de notre dictionnaire. Par défaut RestLess retourne simplement tous les attributs de l'enregistrement en question. On accomplit cette personnalisation généralement dans le but de choisir certains attributs, d'en créer des nouveaux qui ne sont pas des champs de la table ou de joindre des enregistrements associés. RestLess fournit la méthode ``serialize`` pour résoudre ce problème. Par exemple, pour un cours nous avons besoin de joindre les pages associées et leur contenu ainsi que le nombre total de pages. On peut se rendre sur `la documentation <https://django-restless.readthedocs.org/en/latest/#>`_ [#f4]_ pour plus d'informations et sur le fichier ``api.py`` pour des exemples d'utilisation.

*************************
Communication avec l'API
*************************

Nous avons construit une API JSON afin qu'AngularJS puisse communiquer avec une base de données. Pour effectuer les requêtes sur l'API, on trouve deux méthodes utilisées dans le projet. La première consiste à utiliser l'objet Angular ``$http``. Celui-ci permet de construire une requête et de récupérer la réponse ainsi que les éventuelles erreurs. On trouve toutes les spécifications sur la `documentation AngularJS <https://docs.angularjs.org/api/ng/service/$http>`_ [#f5]_. La seconde méthode est d'utiliser l'objet ``$resource``. Si l'on possède une table sur laquelle on veut effectuer les opérations CRUD, ``$resource`` nous évite d'écrire toutes les requêtes avec ``$http``. En effet, ``$resource`` est un objet qui fournit directement les méthodes pour effectuer les différents types de requêtes sur l'API. Pour générer les URL, on fournit d'abord à l'objet une URL de base. Puis, en se basant sur les conventions du web, l'objet est capable d'effectuer les requêtes servant à agir sur la table. Ci-dessous se trouve un exemple d'un objet ``$resource`` et de son utilisation partielle.

.. code-block:: javascript
        
    var Section = $resource(
        "api/sections/:sectionId"    
    );

    Section.query();
    // => GET /api/sections
    var section = Section.get({sectionId: 1});
    // => GET /api/sections/1
    card.$save;
    // => POST /api/sections/1

Dans notre application, tous les objets ``$resource`` sont définis dans le fichier ``/courses/static/courses/javascripts/factories/resources.js``. La `documentation <https://docs.angularjs.org/api/ngResource/service/$resource>`_ [#f5]_ fournit toutes les explications concernant ``$resource``.

.. [#f1] https://github.com/dobarkod/django-restless. Consulté le 4 janvier 15.
.. [#f2] https://docs.djangoproject.com/fr/1.7/topics/class-based-views/generic-display. Consulté le 4 janvier 15.
.. [#f3] https://django-restless.readthedocs.org/en/latest/_modules/restless/modelviews.html. Consulté le 4 janvier 15.
.. [#f4] https://django-restless.readthedocs.org/en/latest. Consulté le 4 janvier 15.
.. [#f5] https://docs.angularjs.org/api/ng/service/$http. Consulté le 21 mars 15.