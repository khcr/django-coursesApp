==================
AngularJS
==================

#############
Introduction
#############

AngularJS est un framework JavaScript crée et maintenu depuis 2009 par Google, l'entreprise a l'origine du populaire moteur de recherche, du client Gmail mais aussi de beaucoup d'outils pour les développeurs. Outre le fait de créer des outils de programmation comme AngularJS, Google propose des outils d'analyse (`Google Analytics <http://google.com/analytics>`_ [#f1]_), des outils de stockage (`Google Cloud <https://cloud.google.com>`_ [#f2]_) ou encore des serveurs pour héberger des applications. Une entreprise non seulement très présente dans le domaine public mais également dans le soutien et la recherche des technologies informatiques. Pour revenir au sujet qui nous intéresse, l'équipe de Google a donc développé le framework AngularJS. Un framework est un ensemble de structures et d'outils programmés dans un langage et réutilisables qui permettent de faciliter la construction d'applications. On trouve par exemple chez PHP le framework `Symfony <http://symfony.com>`_ [#f3]_, chez Ruby `Ruby on Rails <http://rubyonrails.com>`_ [#f4]_, chez Python Django que nous utilisons pour notre site web. Finalement chez JavaScript on trouve AngularJS, mais encore comme concurrent `Ember <http://emberjs.com>`_ [#f5]_ ou `React <http://facebook.github.io/react/>`_ [#f6]_.

AngularJS permet de développer une application web complète. C'est-à-dire qu'il offre plusieurs outils indispensables. D'abord un système de routes qui permet de lier des URL avec des pages différentes. En clair, on peut dire à notre application que quand l'utilisateur entre ``monsite.com/contact`` dans son navigateur, le fichier contact.html soit affiché. Il y a aussi la prise en charge des formulaires avec la possibilité de récupérer les informations entrées par l'utilisateur ou de faire une validation du formulaire, c'est-à-dire de vérifier les informations entrées. Par contre AngularJS ne sait pas comment communiquer directement avec une base de données - une base de données est l'endroit où sont stockées les données persistantes -, il est simplement capable d'utiliser les données d'une base de données fournie par un serveur intermédiaire. Les bases de donnée sont souvent indispensables car elles permettent donc de concevoir des sites web dynamiques. Il est donc nécessaire d'utiliser un autre langage avec AngularJS. Django jouera ce rôle mais nous éclaircirons ce concept plus tard quand nous étudierons son intégration avec Angular.

Pour bien comprendre la documentation du projet, il faut savoir ce qu'est Django. Comme mentionné précédemment, il s'agit d'un framework Python. Il est spécialisé dans la création de site web et est le leader face à ces concurrents comme `Turbo Gears <http://www.turbogears.org/>`_ [#f7]_. Django est ce que nous utilisons principalement pour créer notre application web. Créer un site web avec Python seulement est difficile et peu pratique, un framework est pratiquement indispensable. Effectivement Django fournit les outils nécessaires pour créer des pages HTML, communiquer avec une base de données, gérer les URLs, etc. Pour comprendre les exemples Django qui apparaitront, sachez simplement qu'il utilise le modèle MVC - modèle, vue, contrôleur - qui est expliqué dans la section suivante. La particularité est que Django a changé les termes: *modèle* reste *modèle*, *vue* est égale à *template* et *contrôleur* est égale à *vue*.

=========== =============
MVC         MVT (Django)
=========== =============
Modèle      Modèle
Vue         Template
Contrôleur  Vue
=========== =============

#########################
Spécificités et avantages
#########################

Qu'est-ce qui démarque AngularJS de ses concurrents ? En bref, quelles sont ses fonctionnalités qui facilitent tant la vie des développeurs ? La première chose à connaitre sur AngularJS est qu'il encourage le modèle MVC - modèle, vue, contrôleur. Il s'agit en fait de séparer dans notre application ces trois composants. Grossièrement, le modèle est la partie qui gère les données de l'application, la vue s'occupe de ce qui sera affiché à l'utilisateur et le contrôleur est la partie qui relie le modèle et à la vue. Il va chercher les données dans les modèles pour les donner à la vue qui les affiche et, vice-versa, il reçoit les données de la vue, par un formulaire par exemple, pour mettre à jour le modèle. Un principe très important dans ce motif de programmation est que le minimum de code logique doit se trouver dans les vues. Elles doivent se contenter d'afficher car toutes les opérations se font idéalement dans les contrôleurs ou les modèles. L'avantage est de cette organisation est une compréhension plus aisé et une modularité du code. 

Dans la suite de cette section nous allons nous intéresser à quelques fonctionnalités clés d'AngularJS

*****************
Du HTML expressif
*****************

Abordons d'abord les vues. Le premier "miracle" du framework est de transformer le HTML statique en un langage expressif et dynamique. A la base le HTML est un syntaxe qui permet de structurer une page web à l'aide de balises qui définissent leur contenu comme par exemple les balises qui délimitent les paragraphes, les titres, les images, etc. Traditionnellement on utilise un autre langage comme Python pour transformer la page et y insérer notre contenu dynamique qui provient de la base de données. Concrètement il pourrait s'agir d'afficher une liste d'articles dans une page. Si on travaille avec Django, on assignerait à une variable ``articles`` tous les articles avec une requête SQL - SQL est le langage pour communiquer avec une base de données relationnelle - on ferait ensuite une boucle dans la page HTML et on afficherait le titre ainsi que le contenu de chaque article.

.. code-block:: html
    
    <html>
        <head></head>
        <body>
            <div id="articles">
                {% for article in articles %}
                    <h1>{{ article.titre }}</h1>
                    <p>{{ article.contenu }}</p>
                {% endfor %}
            </div>
        <body>
    <html>

Les balises ``{% %}`` et ``{{ }}`` signifie simplement que ce n'est plus du HTML mais que du code Django est à l'intérieur et doit être exécuté par le serveur.

Avec AngularJS, le modèle est légèrement différent. En effet on trouve dans le framework ce qu'on appelle des directives, un concept spécifique à Angular. Ce sont des balises ou des attributs HTML supplémentaires que fournit AngularJS. On peut les ajouter à notre page et elles effectueront différentes actions selon leur rôle. Par exemple pour reprendre l'exemple des articles, pour faire une boucle, on utilise la directive ``ng-repeat``. On l'utilise comme un simple attribut HTML:

.. code-block:: html

    <html>
        <head></head>
        <body>
            <div id="articles" ng-repeat="article in articles">
                <h1>{{ article.titre }}</h1>
                <p>{{ article.contenu }}</p>
            </div>
        <body>
    <html>

A l'instar de Django, les doubles accolades signifient qu'on veut exécuter du code Angular/JavaScript à l'intérieur. Ici on affiche simplement une variable, mais on pourrait également faire un calcul et afficher le résultat: ``{{ 1 + 2 }}``. Par contre AngularJS est exécuté côté client contrairement à Django qui est côté serveur.

Comme précédemment, on a assigné une variable avec tous les articles. Par contre cette fois la boucle se fait directement en utilisant la directive ``ng-repeat`` qui se confond avec la syntaxe HTML. A l'intérieur de l'attribut, il faut utiliser la syntaxe Angular pour faire la boucle: ``article in articles``. On lui demande de parcourir la variable ``articles`` et d'utiliser comme variable temporaire ``article`` pour chaque article parcouru. Il existe beaucoup d'autre directives dans AngularJS pour par exemple réagir au clique d'une souris sur un élément ou pour afficher ou cacher des sections. Il est aussi possible de créer ses directives personnalisées avec le comportement désiré. Créer ses propres directives permet soit d'avoir un code plus clair ou d'éviter la répétition. Dans les deux cas, cette fonctionnalité est très utile et puissante. 

A cause de ces directives on parle d'HTML expressif. En effet, avec celles-ci le HTML ne décrit pas seulement le contenu, mais aussi le comportement de l'application web et sa manière de fonctionner. On sait ainsi clairement et rapidement en regardant notre page HTML les fonctionnalités qu'on a implémenter sur celle-ci et c'est plus facile d'avoir une vue d'ensemble de son application.

**********************
Two-way data binding
**********************

La deuxième fonctionnalité majeur d'AngularJS est ce qu'on appelle *two-way data binding* ou en français *la liaison des données à double sens*. Derrière cette mystérieuse expression se cache la manière qu'utilise le framework pour relier le modèle et la vue. Le système habituel est comme suit. On génère les vues en fonction de ce qui se trouve dans le modèle, comme dans l'exemple précédent où ou on cherche des articles dans la *BD* pour ensuite générer une page. Quand le modèle change, un article est ajouté par exemple, la vue ne se met pas à jour. On doit la générer à nouveau pour voir le nouvel article. De plus, si l'utilisateur remplit un formulaire pour ajouter un nouvel article, le modèle ne pas change pas tant que le formulaire n'a pas été traité. On appelle ce système logiquement *one-way data binding*. Le schéma qui suit illustre ce principe. Pour générer une vue pour l'utilisateur, le template et le modèle doivent être fusionné et chaque fois qu'un changement est fait, on doit refaire le même processus.

.. figure:: images/One_Way_Data_Binding.png
    :scale: 100%
    :align: center

    One-way data binding 

    source [#f8]_

Avec Angular le principe est plus intelligent. Les vues se génèrent effectivement en fonction des modèles, par contre si le modèle change, la vue se mettra automatiquement à jour sans d'avoir effectuer un nouveau rendu de la page. Si un utilisateur fait un changement dans la vue, le modèle se changera également. Les deux entités sont donc toujours synchronisé grâce a ce mécanisme du framework. Le vue met à jour le modèle et le modèle met à jour la vue continuellement.

.. figure:: images/Two_Way_Data_Binding.png
    :scale: 100%
    :align: center

    Two-way data binding 

    source [#f8]_

Cette fonctionnalité facilite énormément la vie du développeur. Imaginons un système de commentaire. Il y a une liste de commentaires et un formulaire pour en ajouter un. Pour le développeur il suffit de relier le formulaire au modèle. Ensuite au fur et à mesure que l'utilisateur tape son commentaire, le modèle est mis à jour et contient le nouveau commentaire. Il peut déjà s'afficher dans la liste des commentaires. Voici un exemple de code qui permet de cacher ou afficher une portion de page à l'aide d'un bouton.

.. code-block:: html
    
    # index.html
    <html ng-app="DemoApp">
        <head></head>
        <body ng-controller="IndexController">
            <!-- section affichée selon la variable affiche grâce à la directive ng-show -->
            <div ng-show="affiche">
               <h1>Je suis une section cachée !</h1>
               <p>Mais je ne cache rien d'intéressant...<p>
            </div>
            <!-- bouton qui affiche/cache la section. Appelle la fonction toggle() grâce à la directive ng-click -->
            <button type="button" ng-click="toggle()">Afficher/Cacher</button>
        <body>
    <html>

.. code-block:: javascript
    
    # index_controller.js
    // On crée une application Angular
    var app = angular.module("DemoApp");

    // On crée un contrôleur Angular
    app.controller("IndexController", function($scope) {

        // variable utilisé dans ng-show="affiche"
        $scope.affiche = false;

        // fonction appelée lorsqu'on clique sur le bouton
        $scope.toggle = function() {
            $scope.affiche = !$scope.affiche
        };

    });


D'abord on affiche une section selon une variable booléenne ``affiche`` et on assigne à la variable ``false`` par défaut. Puis on ajoute au bouton qui exécute une fonction qui change la valeur de notre variable ``affiche`` de ``false`` à ``true`` et vice-versa. La section s'affichera ou se cachera selon. Plusieurs directives sont utilisées dans l'exemple. ``ng-app`` signale à AngularJS qu'il faut analyser et compiler cette page. ``ng-controller`` signale qu'il faut utiliser le contrôleur ``IndexController`` qui est défini dans le fichier JavaScript et d'exécuter le code à l'intérieur. ``ng-show`` montre ou non la section selon la contenu de la variable booléenne ``affiche`` et ``ng-click`` exécute la fonction ``toggle()`` lorsque qu'on clique sur le bouton.

******************
Et plus encore...
******************

Il y a évidemment encore d'autres avantages à utiliser ce framework, notamment les injections de dépendances et l'extensibilité d'AngularJS, mais nous avons vu les deux principales différences dans le monde des frameworks JavaScript.

.. rubric:: Notes

.. [#f1] http://google.com/analytics
.. [#f2] https://cloud.google.com
.. [#f3] http://symfony.com
.. [#f4] http://rubyonrails.com
.. [#f5] http://emberjs.com
.. [#f6] http://facebook.github.io/react
.. [#f7] http://www.turbogears.org
.. [#f8] https://docs.angularjs.org/guide/databinding