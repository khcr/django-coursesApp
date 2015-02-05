========
MathJax
========

`MathJax <http://mathjax.org>`_ est un plugin JavaScript pour afficher des mathématiques dans le navigateur. Il utilise HTML et CSS pour afficher les expressions de maths dans un style LaTeX. Le rédacteur peut par conséquent aisément utiliser la notation LaTeX pour définir des fonctions, faire des fractions, des racines carrées, des puissances, écrire les symboles spéciaux, etc, en balisant le contenu et ensuite celui-ci sera correctement affiché grâce au moteur de rendu MathJax. Une section d'aide est disponible pour la syntaxe à utiliser.

#############
Installation
#############

L'installation de MathJax est très facile sur n'import quelle site web. Il suffit de télécharger le dossier sur le `site officel <http://mathjax.org>`_, de le mettre dans le projet et d'inclure le lien du fichier JavaScript ``MathJax.js`` à la racine du dossier. Il est possible de charger une configuration différente de celle par défaut, pour changer la mise en forme, la notation et d'autres subtilités. On peut passer le nom de la configuration dans un paramètre ``config`` dans le lien qui inclut MathJax. Toutes ces fichiers se trouvent dans le dossier ``config`` de MathJax ou alors il est possible de créer sa configuration personnalisée. Les informations détaillées des configurations disponibles se trouvent dans `leur documentation <http://docs.mathjax.org/en/latest/config-files.html>`_. Actuellement nous utilisons la configuration ``TeX-AMS_HTML`` qui utilise la notation Tex (LaTeX) et qui génère du HTML. Il est aussi possible d'utiliser le CDN, et dans le lien on peut églamement spécifier le fichier de configuration.

Une fois le plugin MathJax installé, il va automatiquement scanner les pages HTML et detecter les balises qui délimitent du contenu mathématique - par défaut ``$$`` - pour après le transformer. Ci-dessous un exemple de l'intégration du plugin et du résultat.

.. code-block:: html
    
    <html>
        <head>
            <!-- Fichiers locals -->
            <script src="/MathJax/MathJax.js?config=TeX-AMS_HTML"></script>

            <!-- CDN -->
            <script src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML"></script>
        </head>
        <body>
            $$ f(x) = 5x + 4 $$
        </body>
    </html>

.. figure:: images/mathjax.png
    :align: center

    Résultat

#################
Personnalisation
#################

Dans le cadre du projet, quelques modifications ont été faites par rapport à l'utilisation basique de MathJax. Pour pouvoir personnaliser MathJax, on utilise un fichier spécial pour modifier des options que MathJax met à disposition. Ce fichier est déjà créé, se trouve dans le dossier ``config/local`` et se nomme ``local.js``. Ensuite il suffit quand on inclut MathJax dans notre page de modifier l'URL comme suit: ``config=TeX-AMS_HTML,local=local``. On a ajouté dans le paramètre ``config`` de l'URL ``,local/local``.

Etudions ce fichier qui a été modifié pour les besoins du projet.

.. code-block:: javascript

    MathJax.Hub.Config({

        skipStartupTypeset: true,

        // Apparence
        showProcessingMessages: false,
        messageStyle: "none",
        showMathMenu: false,
        showMathMenuMSIE: false,

        styles: {
            ".MathJax_Display": {
              clear: "both"
            }
        }

    });

    MathJax.Ajax.loadComplete("[MathJax]/config/local/local.js");

Premièrement, les options commentées ``Apparence`` servent à supprimer les messages superficiels de MathJax, c'est-à-dire les messages de chargements et autres. On a également supprimé le menu MathJax qu'il ajoute aux expressions qu'il transforme et qu'on affiche avec un clique-droit. Ce menu a été jugé inutile et surchargeant. Ensuite le dictionnaire ``styles`` permet d'ajouter du CSS en plus de ce fait MathJax. Ici on ajoute à la classe "MathJax_Display" - classe utilisé sur toutes les expressions qu'il transforme - l'expression ``clear: "both"``. Il s'agit d'une correction d'un bug du plugin car par défaut MathJax pouvait interférer avec le style déjà en place sur le site web et créait des problèmes génants pour l'interface. Finalement la dernière configuration faite n'est pas la plus simple. Nous avons vu que MathJax analysait toute la page HTML pour transformer le contenu balisé. Nous avons modifié ce comportement par défaut de MathJax. D'une part pour des questions de performance, car nous n'avons pas envie que des pages qui n'ont pas de contenu mathématique soient analysées par le lourd code JavaScript de MathJax, d'autre part pour des questions de contrôle, en effet on veut que savoir exactement où MathJax agit. L'option ``skipStartupTypeset`` permet donc de désactiver l'exécution automatique du processus MathJax. Le prochaine défi est de trouver un moyen facilemenent utilisable d'indiquer quelle partie doit être analysée ou non. Pour ce faire AngularJS a un outils très pratique pour accomplir ce genre de tâches et nous avons déjà eu l'occasion de le découvrir dans le premier chapitre: :doc:`les directives <angularjs>`. Ce sont ces attributs ou éléments HTML d'AngularJS qui exécute des actions spécifiques, comme ``ng-repeat`` ou ``ng-show``.

Nous allons donc créer une directive Angular ``mathjax``.

.. code-block:: javascript

    app.directive('mathjax', function() {
        // Le code vient ici
    }]);

Le but de cette directive est de pouvoir baliser les parties de notre page HTML qui contiennent des maths avec un élément HTML. Par exemple de la façon suivante quand on affiche le cours: ``<mathjax>{{ cours.contenu }}</mathjax>``.
Pour définir notre directive et son comportement, il faut returner un dictionnaire contenant les options de notre directive. Voici la directive complète que nous allons analyser ensemble.

.. code-block:: javascript

    app.directive('mathjax', function($timeout) {
        restrict: 'AE',
        template: '<div class="ng-hide" ng-transclude></div>',
        transclude: true,
        link: function(scope, element, attrs) {
            $timeout(function () {
                MathJax.Hub.Queue(["Typeset", MathJax.Hub, element[0]]);
                MathJax.Hub.Queue(function() {
                    element.children().removeClass("ng-hide");
                })
            });
        }
    }]);

* **restrict**: 'AE' signifie que notre directive peut être un attribut (A = Attribut), c'est à dire ``<directive></directive>`` ou alors un élément (E = Element), c'est à dire ``<div directive></div>``. On peut encore l'utiliser en tant que classe avec l'option C (C = Class), c'est-à-dire ``<div class="directive"></div>``.
* **template**: Le contenu HTML dans notre directive.
* **tranclude**: Cette option permet de récupérer le contenu qui est dans la directive et de l'injecter dans le template. En fait, si on n'utilise pas transclude, qu'importe ce qu'on écrira dans notre directive sur notre page HTML, par exemple lorsqu'on fait ``<mathjax>{{ cours.contenu }}</mathjax>``, le contenu du cours sera remplacé par la chaine de caractère de l'option ``template``. Par contre quand on utilise ``transclude``, Angular récupère le contenu de la directive et l'injecte dans notre template à l'endroit où on spécifie ``ng-tranclude``, c'est pour cela qu'on trouve dans ``template`` le code ``<div ng-transclude></div>``, le contenu sera donc dans la ``div``.
* **link**: c'est la fonction qui sera exécuté une fois que le code sera compilé, en clair quand Angular a transformé la page HTML et ses directives, le code HTML est donc totalement généré et il reste à ajouter la couche JavaScript. Par conséquent avec la fonction qu'on passe à ``link`` on peut manipuler le contenu de notre directive. La fonction prend trois arguments: ``scope``, basiquement l'objet qui contient des données du modèle, ``element``, l'élément HTML lui-même et ``attrs``, les attributs HTML de notre directive.

Il y a encore beaucoup d'autres options disponibles pour personnaliser la directive, voir `la documentation <https://docs.angularjs.org/guide/directive>`_.

Intéressons nous maintenant au code qui se trouve à l'intérieur de la fonction ``link``. La difficulté se trouve surtout dans le code spécifique à MathJax, ``MathJax.Hub.Queue``. En fait cette expression permet d'exécuter des fonctions en lien avec MathJax au bon moment. Elle permet tout simplement d'assurer que les fonctions qu'on passe à ``Queue`` s'exécute une fois que MathJax est complétement chargé et qu'il est prêt à être utilisé. La première expression MathJax, le ``Typeset`` - une fonction fournie par MathJax -, sert à analyser et transformer le contenu de la directive pour mettre en forme les mathématiques, remarquez qu'on passe l'élément en dernier argument, ``element[0]``. Ensuite la deuxième expression, on enlève la classe ``ng-hide`` de notre élément. Par défaut on cache le contenu de la directive, comme on peut l'observer dans l'option ``template`` qui contient la classe ``ng-hide``, et cette expression sert à l'afficher une fois que les expressions mathématiques on été tranformées, ainsi l'utilisateur ne voit pas du contenu qui n'a pas encore été formaté par MathJax. Pour plus d'informations sur la Queue MathJax, voir `la documentation MathJax <http://docs.mathjax.org/en/latest/typeset.html>`_. Finalement le tout est enveloppé dans une fonction ``$timeout`` qui permet simplement d'assurer, lorsque notre directive est utilisé dans une boucle, que le contenu est présent avant que nous exécutions nos transformations.

Voilà, notre directive est prête à être utilisée ! Maintenant il suffit de l'utiliser pour formater notre contenu mathématique à l'endroit où on le désire.

