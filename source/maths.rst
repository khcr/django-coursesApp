========
MathJax
========

`MathJax <http://mathjax.org>`_ [#f1]_ est un plugin JavaScript pour afficher des mathématiques dans le navigateur. Il utilise HTML et CSS pour afficher les expressions de mathématique dans le style LaTeX. Le rédacteur peut par conséquent aisément utiliser la notation LaTeX pour définir des fonctions, faire des fractions, des racines carrées, des puissances, écrire les symboles spéciaux, etc. en balisant le contenu et ensuite celui-ci sera correctement affiché grâce au moteur de rendu MathJax. Une section d'aide est disponible pour la syntaxe à utiliser.

#############
Installation
#############

L'installation de MathJax est très facile sur n'importe quelle site web. Il suffit de télécharger le dossier sur le `site officiel <http://mathjax.org>`_ [#f1]_, de le mettre dans le projet et d'inclure le lien du fichier JavaScript ``MathJax.js`` à la racine du dossier. Il est possible de charger une configuration différente de celle par défaut, pour changer la mise en forme, la notation et d'autres subtilités. On peut passer le nom de la configuration dans un paramètre ``config`` dans le lien qui inclut MathJax. Tous ces fichiers se trouvent dans le dossier ``config`` de MathJax. Il est aussi possible de créer sa configuration personnalisée. Les informations détaillées des configurations disponibles se trouvent dans `leur documentation <http://docs.mathjax.org/en/latest/config-files.html>`_ [#f2]_. Actuellement nous utilisons la configuration ``TeX-AMS_HTML`` qui utilise la notation Tex (LaTeX) et qui génère du HTML. Il est aussi possible d'utiliser le CDN. On peut également spécifier dans le lien le fichier de configuration.

Une fois le plugin MathJax installé, il va automatiquement scanner les pages HTML et détecter les balises qui délimitent du contenu mathématique, par défaut ``$$``. Ensuite il va mettre en forme le contenu afin qu'il s'affiche correctement. Ci-dessous se trouve un exemple de l'intégration du plugin et du résultat.

.. code-block:: html
    
    <html>
        <head>
            <!-- Fichiers locaux -->
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
    :scale: 50%

    Résultat de MathJax

#################
Personnalisation
#################

Dans le cadre du projet, quelques modifications ont été faites par rapport à l'utilisation basique de MathJax. Pour pouvoir le personnaliser, on utilise un fichier spécial pour modifier les options que MathJax met à disposition. Ce fichier est déjà présent dans le dossier. Il se trouve dans le sous-dossier ``config/local`` et se nomme ``local.js``. Ensuite, lorsque l'on inclut MathJax dans notre page, il suffit de modifier l'URL comme suit: ``config=TeX-AMS_HTML,local=local``. On a ajouté dans le paramètre ``config`` de l'URL ``,local/local``.

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

Premièrement, le groupe d'options commenté ``Apparence`` sert à supprimer les messages inutiles de MathJax, c'est-à-dire les messages de chargements par exemple. On supprime également le menu MathJax que celui-ci ajoute aux expressions qu'il transforme et que l'on affiche avec un clic droit. Ce menu est jugé inutile et surchargeant. Ensuite le dictionnaire ``styles`` permet d'ajouter du CSS en plus de celui que génère MathJax. On ajoute à la classe ``MathJax_Display``, une classe utilisée sur toutes les expressions qu'il transforme, le style ``clear: "both"``. Il s'agit d'une correction d'un bug du plugin, car par défaut MathJax pouvait interférer avec le style déjà en place sur le site web. Ce problème créait des problèmes gênants pour l'interface. Finalement, la dernière configuration faite n'est pas la plus simple. Nous avons vu que MathJax analysait automatiquement toute la page HTML pour transformer le contenu balisé. Nous avons modifié ce comportement par défaut de MathJax. Il s'agit d'une part d'une question de performance. En effet, nous n'avons pas envie que des pages qui n'ont pas de contenu mathématique soient analysées par le lourd code JavaScript de MathJax. D'autre part, pour des questions de contrôle, l'on veut savoir exactement où il agit. L'option ``skipStartupTypeset`` permet donc de désactiver l'exécution automatique du processus MathJax. Le prochain défi est de trouver un moyen facilement utilisable pour indiquer quelle partie du code HTML doit être analysée. AngularJS a un outil très pratique pour accomplir ce genre de tâches. Nous avons déjà eu l'occasion de le découvrir dans le premier chapitre: :doc:`les directives <angularjs>`. Ce sont des attributs ou éléments HTML qui exécutent des actions spécifiques, comme ``ng-repeat`` ou ``ng-show``.

Nous allons donc créer une directive ``mathjax``. Le code ci-dessous déclare simplement la directive.

.. code-block:: javascript
    
    // on déclare la directive
    app.directive('mathjax', function() {
        // Le code vient ici
    }]);

Le but de cette directive est de pouvoir baliser les parties de notre page HTML qui contiennent des mathématiques. Par exemple, lorsque l'on affiche un cours, on aimerait faire de la façon suivante: ``<mathjax>{{ cours.contenu }}</mathjax>``.
Pour définir la directive et son comportement, il faut retourner un objet JavaScript contenant les options de notre directive. Ci-dessous se trouve la directive complète que nous allons analyser.

.. code-block:: javascript
    :linenos:

    app.directive('mathjax', function($timeout) {
        restrict: 'AE',
        template: '<div class="ng-hide" ng-transclude></div>',
        transclude: true,
        link: function(scope, element, attrs) {
            $timeout(function () {
                MathJax.Hub.Queue(["Typeset", MathJax.Hub, element[0]]);
                MathJax.Hub.Queue(function() {
                    element.children().removeClass("ng-hide");
                });
            });
        }
    });

* **restrict**: 'AE' signifie que notre directive peut être un attribut (A = Attribut), avec le forme ``<directive></directive>`` ou un élément (E = Element), avec la forme ``<div directive></div>``. On peut aussi ajouter l'option C pour utiliser la directive en tant que classe (C = Class), avec la forme ``<div class="directive"></div>``.
* **template**: Le contenu HTML dans notre directive.
* **tranclude**: Cette option permet de récupérer le contenu qui est dans la directive et de le réinjecter dans le template. En fait, par défaut, qu'importe le contenu de la directive sur la page HTML, celui-ci est de toute façon remplacé par la chaine de caractère de l'option ``template``. Par exemple, si on écrit ``<mathjax>{{ cours.contenu }}</mathjax>``, le contenu du cours est supprimé. Par contre, quand on utilise l'option ``transclude``, Angular récupère le contenu de la directive et l'injecte dans notre template, à l'endroit où l'on spécifie ``ng-tranclude``. Ainsi on trouve dans l'option ``template`` le code HTML ``<div ng-transclude></div>``. Le contenu de la directive est donc ajouté dans la ``div``.
* **link**: c'est la fonction qui est exécutée une fois que la page est compilée. En clair, quand AngularJS a transformé la page HTML et ses directives, le DOM est totalement généré. Ensuite seulement JavaScript peut agir sur celui-ci. Par conséquent, avec la fonction que l'on passe à ``link``, on peut manipuler le contenu de notre directive. La fonction prend trois arguments. ``scope`` est basiquement l'objet qui contient les données du modèle. ``element`` est l'élément HTML lui-même et ``attrs`` contient les attributs HTML supplémentaires de notre directive.

Il y a encore beaucoup d'autres options disponibles pour personnaliser une directive, elles sont listées sur `la documentation <https://docs.angularjs.org/guide/directive>`_ [#f3]_.

Intéressons nous maintenant au code qui se trouve à l'intérieur de la fonction ``link``. La difficulté se trouve surtout dans le code spécifique à MathJax, ``MathJax.Hub.Queue``. En fait, cette expression permet d'exécuter des fonctions en lien avec MathJax au bon moment. Elle permet tout simplement d'assurer que les fonctions que l'on passe à ``Queue`` s'exécutent une fois que MathJax est complétement chargé et qu'il est prêt à être utilisé. La première expression MathJax, à la ligne 7, indique qu'il faut analyser et mettre en forme le contenu de l'élément qu'on passe en argument, dans notre cas ``element[0]``. On peut remarquer que l'on utilise ``element[0]`` et pas ``element``. ``element`` est un objet contenant plusieurs informations tandis que ``element[0]`` retourne l'élément du DOM. Ensuite dans la deuxième expression, ligne 8, on enlève simplement la classe ``ng-hide`` de notre élément. Par défaut on cache le contenu de la directive, comme on peut l'observer dans l'option ``template`` qui contient la classe ``ng-hide``. Cette expression sert à afficher la directive seulement une fois que les expressions mathématiques ont été transformées. Ainsi, l'utilisateur ne voit pas du contenu qui n'a pas encore été formaté par MathJax. Pour plus d'informations sur la ``Queue`` MathJax, on peut se rendre sur `la documentation officielle <http://docs.mathjax.org/en/latest/typeset.html>`_ [#f4]_. Finalement, le code est enveloppé dans une fonction ``$timeout`` qui permet simplement d'assurer, lorsque notre directive est utilisée dans une boucle, que la boucle soit terminée avant que nous exécutions les transformations.

Notre directive est prête à être utilisée ! Maintenant, il suffit de l'utiliser pour mettre en forme notre contenu mathématique à l'endroit où on le désire.

.. code-block:: html
    
    <body>
        <mathjax>
            $$ f(x) = 5x + 4 $$
        </mathjax>
    </body>

.. [#f1] http://mathjax.org. Consulté le 27 décembre.
.. [#f2] http://docs.mathjax.org/en/latest/config-files.html.  Consulté le 27 décembre 14.
.. [#f3] https://docs.angularjs.org/guide/directive. Consulté le 28 décembre 14.
.. [#f4] http://docs.mathjax.org/en/latest/typeset.html.  Consulté le 28 décembre 14.