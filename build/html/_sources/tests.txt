======
Tests
======

Une série de tests à été écrite afin de pouvoir garantir l'utilisation des fonctionnalités et faciliter les futurs apports au projet. Dans notre cas il s'agit de test système, end to end en anglais. Ce type de tests signifie qu'on teste l'application dans son ensemble et d'un point de vue utilisateur. On ne vas pas tester juste une partie du code comme dans des tests unitaires, mais on va simuler un utilisateur et naviguer sur notre site afin de s'assurer que les fonctionnalités sont opérationnelles.

AngularJS fournit un outil adapté pour tester ses applications qui se nomme `Protractor <http://angular.github.io/protractor/#/>`__ [#f1]_. Ce programme nous permettra d'écrire des tests adaptés à AngularJS. En fait Protractor fournit des outils spécifiques au framework. Par exemple il permet de séléctionner des éléments par leur modèle Angular - `ng-model="password"`. Ou encore Protractor attend automatiquement qu'Angular ait fini de préparer la page et que les requêtes AJAX soient terminées avant de faire les tests. Basiquement, un test consiste tout simplement à se rendre sur une page, un cliquer sur un bouton et à vérifier un résultat. On simule un utilisateur. Dans le projet, les tests se trouve dans le dossier `courses/spec`. Il y a un fichier `conf.js` qui est le fichier pour configurer Protractor et les autres fichiers se terminant par `_spec.js` contiennent nos tests. Chaque fichier correspond à une route de notre site. Prenons un exemple dans lequel on test si l'utilisateur peut changer de page sur un cours.

.. code-block:: javascript

    it("allows to switch pages", function() {
        // On se rend sur la page
        browser.get("http://localhost:3333/courses/#/1/view/1");
        // On clique sur le lien
        element(by.id("next-page")).click();
        // On s'attend à ce que le titre ait changé
        expect(element.all(by.binding("page.name")).getText()).toEqual("Les équations");
    });

Notre test commence par la fonction `it`, qui décrit ce qu'on teste, par exemple dans ce code on déclare que "Cela permet de changer de pages". Cette description est utile car elle nous permet de savoir rapidement ce qui est testé et aussi, lorsqu'un test ne fonctionne pas, de savoir tout de suite quelle fonctionnalité ne marche plus. Ensuite dans la fonction `it` on décrit une série d'étape. On se rend sur la page `courses/#/1/view/1`, on trouve lien avec l'id `next-page` et on clique dessus. A la fin du test, on écrit une "attente", c'est ce qui determine si le test passe ou non. Dans notre cas, on s'attend à ce que le nouveau titre de la page soit "Les équations", car on a changé de page en cliquant sur le bouton.

Pour lancer les tests écrit pour notre application, on lance la commande `python3 manage.py tests`. La commande se charge principalement de créer une base de données propre avec des données spécifiques et de lancer les serveurs. Une fois la commande lancée, une fenêtre de navigateur s'ouvrira et les tests défileront dedans comme si un utilisateur agissait. A la fin des tests, il suffit de revenir dans la console pour avoir le compte-rendu, les résultats.

La commande exécutera par défaut tous les tests se trouvant dans le dossier `courses/spec`. Pour changer ce comportement, on peut spécifier le fichier en argument: `python3 manage.py tests home_spec.js`. Pour changer le dossier, par défaut `courses`, il faut le spécifier avec l'option `--app`. Par exemple: `python3 manage.py tests --app teachers`.

.. rubric:: Notes

.. [#f1] http://angular.github.io/protractor/#/