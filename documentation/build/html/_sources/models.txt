==================
Modèle relationnel
==================

############
Introduction
############

Une base de données est un outil permettant de stocker des données persistantes pour ensuite les réutiliser ou les conserver. Dans le domaine du web, on utilise principalement les bases de données relationnelles. Traditionnellement, elles se découpent en plusieurs tableaux que l'on appelle tables, contenant des colonnes et des lignes. On crée des tables pour représenter des entités, des cours par exemple, qui ont des attributs représentés par des colonnes. Ensuite, chaque ligne correspond à un enregistrement, c'est-à-dire une entité, un cours dans notre exemple. Une table a pratiquement toujours une colonne ``id`` qui est un nombre, un identifiant unique qui permet d'identifier un enregistrement parmi les autres de la table. On l'appelle *clé primaire*. Ils servent aussi à créer des relations entre les tables, à lier un enregistrement à un autre. Nous verrons ces relations dans la construction du module de cours. Pour communiquer avec une base de données relationnelles, notamment chercher des enregistrements dans une table, créer ou mettre à jour un enregistrement, etc. l'on utilise le langage *SQL*, *Structured Query Language*.

.. figure:: images/bd.png
    :scale: 80%
    :align: center

    Schéma résumant une base de données relationnelle

Le modèle relationnel est une modélisation de la base de données du site. Attardons-nous donc sur le modèle qui se cache derrière les fonctionnalités que nous voulons développer. Nous commencerons par le point central de la base de données: les tables et les relations qui concernent les cours et qui forment la majeure partie du modèle. Ensuite nous verrons les tables additionnelles qui complètent le modèle relationnel et ajoutent les fonctionnalités auxiliaires.

Il est important de savoir que Django fournit en tant que framework plusieurs outils facilitant le travail avec une base de données. Chaque table de notre *BD* est représentée par ce que l'on appelle un modèle. C'est un simple fichier Python qui contient les informations pour construire la table. Dans le projet, les modèles sont regroupés dans le fichier ``models.py``. Ce fichier permet à Django de générer les tables et ensuite de fournir une série de méthodes qui permettent de communiquer avec la *BD* sans utiliser le langage SQL, qui est le seul langage que comprend une *BD*. Django nous évite par conséquent d'apprendre un nouveau langage. Nous verrons ces méthodes plus tard dans les exemples d'utilisation.

##########
Les cours
##########

************
La structure
************

.. figure:: images/uml_courses.png
    :scale: 90%
    :align: center

    Schéma de toutes les tables du modèle relationnel

La structure des tables relationnelles reflète la structure que perçoit le rédacteur et cela facilite grandement la compréhension. Nous avons vu qu'un cours se compose de plusieurs pages. Elles-mêmes contiennent plusieurs sections, avec un titre et un contenu, que l'auteur peut éditer ou retirer à sa guise. C'est exactement la même chose dans la structure du modèle. Tout d'abord on trouve une tables ``courses`` qui contient les informations de base que entre le professeur à la création du cours. Elle contient les colonnes suivantes: ``name``, ``description``, ``difficulty``. Il reste le champs ``chapter`` que nous verrons plus tard. Ensuite, il y a la table ``pages`` avec la colonne ``name``, ``order`` et ``course_id``. ``name`` est le titre de la page. ``order`` est un nombre qui permet de trier les pages d'un cours entre elles et de les réorganiser par la suite. ``course_id`` indique la relation avec un cours. Elle contient l'``id`` du cours auquel appartient la page. En effet, chaque page appartient à un cours et, vice-versa, un cours possède donc plusieurs pages. L'utilisation plus précise de cette relation est expliquée dans la partie suivante. Finalement, pour compléter l'ensemble, il reste la table ``sections``. Elle possède les colonnes ``name``, ``content``, ``order`` et ``page_id``. On retrouve un titre et un contenu. Il y également l'ordre qui fonctionne comme pour les pages. ``page_id`` indique la relation avec une page. Elle contient l'``id`` de la page à laquelle appartient la section. Par conséquent, une section appartient à une page et une page possède plusieurs sections. A noter que ces trois tables ont également les champs ``created_at`` et ``updated_at``. Elles enregistrent la date et l'heure de la création et la dernière mise à jour de l'entité. Pour résumer les relations qui lient les tables, un cours a plusieurs pages, et chacune des pages a plusieurs sections. Comme dit précédemment, l'on comprend facilement les relations en observant l'implémentation de l'interface de rédaction d'un cours.

.. figure:: images/schema_cours.png
    :scale: 80%
    :align: center

    Schéma qui résume les relations des tables courses, pages et sections


***********
Utilisation
***********

Tous les exemples d'opérations sur la base de données sont d'abord écrits avec les méthodes de Django puis en SQL pur. Une des particularités de Django pour sauvegarder des objets dans la base de données est qu'il fait appel à des formulaires. Ils sont nommés dans le code sous la forme de ....Form, comme ``CourseForm`` par exemple. On utilise aussi ces formulaires dans les vues pour générer les formulaires HTML que complètent les utilisateurs. Concrètement, ils permettent simplement de relier les données soumises par un utilisateur à nos modèles Django. Rappelons que dans Django les modèles sont la représentation des tables de la *BD*. Par conséquent les formulaires Django servent à créer et à mettre à jour des enregistrements de la base de données via des formulaires HTML. Prenons un exemple pour bien se représenter le processus. Lorsqu'un utilisateur soumet un formulaire, le navigateur envoie les données au serveur sous la forme d'un dictionnaire: ``{"titre" : "La géométrie", "description" : "Bla bla"}``. Ensuite, côté serveur, l'on récupère le dictionnaire et on enregistre les données dans la *BD* en utilisant un formulaire Django. Pour approfondir le concept des formulaires, il faut se rendre sur la `documentation Django <https://docs.djangoproject.com/fr/1.7/topics/forms/>`_ [#f1]_.

Récupère tous les cours.

.. code-block:: python

    # api.py - TeacherCourseList

    Course.objects.all()

.. code-block:: sql

    SELECT * FROM courses

Récupère tous les cours publiés ayant un thème particulier.

.. code-block:: python

    # api.py - CourseList

    Course.objects.filter(chapter__theme__name=request.GET['theme'], published=True)

.. code-block:: sql

    SELECT * FROM "courses_course" INNER JOIN "teachers_chapter" ON ( "courses_course"."chapter_id" = "teachers_chapter"."id" ) 
    INNER JOIN "teachers_theme" ON ( "teachers_chapter"."theme_id" = "teachers_theme"."id" ) 
    WHERE ("teachers_theme"."name" = "Gémotrie" AND "courses_course"."published" = True)

Créer un nouveau cours. On crée d'abord le cours, puis une page associée contenant une section vierge.

.. code-block:: python

    # api.py - CourseList
    
    # on utilise un formulaire (CourseForm)
    # request.data est un dictionnaire contenant les données soumises par l'utilisateur 
    # ici les informations du cours
    course_form = CourseForm(request.data)
    # on vérifie si les informations sont présentes et valides
    if course_form.is_valid():
        # on crée le cours
        course = course_form.save()
        # on crée la page associée
        page = Page(name="Première page", order=1, course_id=course.id)
        page.save()
        # on crée une section associée à la page
        page.sections.create(name="Première section", order=1)

.. code-block:: sql
    
    -- on crée le cours
    INSERT INTO courses (name, description, difficulty, author_id, chapter_id, created_at, updated_at) 
    VALUES ("L'algèbre", "Lorem ipsum...", 3, 1, 1, *, *)
    -- => ID du cours = 1
    -- On crée la page associée
    INSERT INTO pages (name, order, course_id, created_at, updated_at) 
    VALUES ("Première page", 1, 1, *, *)
    -- => ID de la page = 1
    -- on crée une section associée à la page
    INSERT INTO sections (name, content, order, page_id, created_at, updated_at) 
    VALUES ("Première section", "bla bla", 1, 1, *, *)

Mettre à jour le contenu d'une page d'un cours. Le titre de la page, le titre et le contenu des sections vont être sauvegardés. Pour accomplir cette action, on commence par simplement enregistrer la page avec les nouvelles données. On utilise la même procédure que pour la création d'un cours. Remarquez simplement que dans ``page_form = PageForm(request.data, instance=page)``, on passe en paramètre la page provenant de la base de données pour signaler à Django que l'enregistrement existe déjà. Ainsi Django ne crée pas une nouvelle page mais met la nôtre à jour. Pour les sections, on itère d'abord sur le dictionnaire qui contient les données de toutes les sections de la page. Puis, pour chaque section, on accomplit la même procédure que pour une page.

.. code-block:: python

    # api.py - PageCourseDetail
    
    # Récupère la page à éditer
    page = Page.objects.get(id=page_id)
    # On utilise un formulaire (PageForm)
    # request.data est un dictionnaire contenant les données soumises par l'utilisateur
    # ici le contenu de la page
    page_form = PageForm(request.data, instance=page)
    # On vérifie si les informations sont présentes et valides
    if page_form.is_valid():
        # On enregistre la page - sauvegarde le titre
        page_form.save()
    # On récupère le dictionnaire contenant les données des sections
    sections_params = request.data['sections']
    # On fait une boucle pour chaque section
    for section_params in sections_params:
        # On récupère la section
        section = Section.objects.get(id=section_params['id'])
        # On utilise un formulaire (SectionForm)
        # section_params est un dictionnaire contenant le titre et le contenu de la section
        section_form = SectionForm(section_params, instance=section)
        # On vérifie si les informations sont présentes et valides
        if section_form.is_valid():
            # On enregistre la section
            section_form.save()

.. code-block:: sql
    
    -- Récupère la page à éditer
    SELECT * FROM pages WHERE id = 1
    -- On enregistre la page
    UPDATE pages SET name = "Nouveau titre" WHERE id = 1
    -- On enregistre la section
    UPDATE sections SET name = "Nouveau titre", "content" = "Lorem ispum" WHERE id = 1

##############
Les chapitres
##############

Pour pouvoir organiser le contenu du site, chaque cours est associé à un chapitre. Deux tables servent cet objectif. Tout d'abord il y a la table ``themes`` avec un champs ``name``. Il y a également la table ``chapters`` avec un champ ``name`` et ``theme_id``. ``theme_id`` associe chaque chapitre à un thème. Ensuite la table ``courses`` a un champ ``chapter_id``. Celui-ci contient l'``id`` d'un chapitre. Il relie chaque cours à un chapitre et par conséquent à un thème. Par exemple, il peut y avoir un cours sur les tangentes. On le placerait dans le chapitre "les cercles" et le chapitre se trouverait lui-même dans le thème "Géométrie". On peut légitiment se demander pourquoi ces deux niveaux et ces deux tables ? Le système est construit afin de laisser une plus grande souplesse et liberté pour organiser le contenu. En effet, imaginons qu'il y ait 10, 20, 30 ou plus chapitres, comment s'y retrouver ? La solution des de les regrouper sous une idée plus générale et c'est précisément le rôle de la table ``themes``.    

#################
Les commentaires
#################

La table ``course_comments`` permet aux lecteurs du site de poster un commentaire sur un cours. La table contient un champ ``content``, ``user_id`` et ``course_id``. Chaque commentaire appartient donc à un utilisateur et à un cours.


###############
La progression
###############

L'utilisateur a la possibilité de marquer sa progression quand il lit un cours. Voyons comment cette fonctionnalité se traduit au niveau du modèle relationnel. ``progressions`` est la table principale. Elle contient les colonnes ``page_id``, ``user_id`` et ``status_id``. En somme, elle ne contient que des relations. L'idée principale est la suivante. Lorsqu'un utilisateur a lu une page d'un cours, on lui propose de choisir s'il a compris ou souhaite relire la page. Le champ ``user_id`` enregistre quel utilisateur indique sa progression et le champ ``page_id`` indique quelle page est concernée. Finalement, l'attribut ``status_id`` associe la progression à une table ``statuses``. Celle-ci contient le nom que peut avoir une progression. Il y a deux statuts: "Compris" et "A relire". Pour résumer, lorsque que l'on crée une progression dans notre base de données, l'on sait qu'un certain utilisateur a "compris" ou souhaite "relire" une page particulière. L'exemple qui suit montre comment l'on enregistre une progression concrètement.

.. code-block:: python

    # api.py - CoursePageProgress
    
    # On récupère l'utilisateur connecté au site
    user = request.user
    # On récupère la page concernée
    page = Page.objects.get(id=pk)

    # request.data est un dictionnaire contenant les données soumises par l'utilisateur
    # ici, si l'utilisateur a compris ou non la page
    # On choisit le status en fonction
    if request.data['is_done'] == True:
        status = Status.objects.get(name="Compris")
    else:
        status = Status.objects.get(name="Relire")

    # Si l'utilisateur n'a pas encore marqué sa progression sur cette page
    if not page.state(user):
        # On crée une progression avec la page, le statut et l'utilisateur
        page.progression_set.create(status=status, user=user)
    # si l'utilisateur a déjà marqué sa progression sur cette page
    else:
        # On récupère sa progression
        progression = page.progression_set.get(user=user)
        # On met à jour avec le nouveau statut
        progression.status = status
        progression.save()

.. code-block:: sql
    
    -- Récupère la page à éditer
    SELECT * FROM pages WHERE id = 1
    -- => ID de la page = 1
    -- Récupère le statut
    SELECT * FROM statuses WHERE name = "Compris"
    -- => ID du statut = 1
    -- Crée une progression
    INSERT INTO "progressions" ("page_id", "status_id", "user_id", "created_at", "updated_at") 
    VALUES (1, 1, 1, *, *)
    -- Met à jour une progression
    UPDATE "progressions" SET status_id = 1 WHERE id = 1

.. [#f1] https://docs.djangoproject.com/fr/1.7/topics/forms
