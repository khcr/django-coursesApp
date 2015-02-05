==================
Modèle relationnel
==================

############
Introduction
############

Une base de données est un outil permettant, comme son nom l'indique, de stocker des données persistantes pour ensuite les réutiliser ou les conserver. Dans le domaine du web, on utilise des base de données relationnelles. Traditionnelement elle se découpe en plusieurs tableaux, ou plutôt tables dans le jargon, contenant des colonnes et des lignes. On crée des tables pour représenter des objets, des cours par exemple, qui ont des attributs représentés par des colonnes et chaque ligne est un enregistrement, c'est-à-dire une entité, un objet, 1 cours dans notre exemple. Une table a pratiquement toujours une colonne ID qui est un nombre, un identifiant unique qui permet de trouver un enregistrement parmi les autres de la table. On l'appelle *clé primaire*. Ils servent aussi à créer des relations entre les tables, un lier un enregistrement à un autre, d'une table différente ou non, comme nous le verrons ensuite dans la construction du module de cours. Pour communiquer avec la base de données relationnelles, notamment chercher tous les enregistrements d'une table ou seulement 1, créer ou mettre à jour un enregistrement, etc, on utilse le language SQL, Structured Query Language.

.. figure:: images/bd.png
    :scale: 70%
    :align: center

    Schéma résumant une base de données relationnelle

Le modèle relationnel est une modélisation de la base de données du site. Attardons-nous donc sur le modèle qui se cache derrière les fonctionnalités évoquées précédemment. Nous commencerons par le point centrale de la base données: les tables et relations qui concernent les cours et qui forment la majeur partie du modèle et ensuite nous verrons les tables additionelles qui complètent le modèle relationnel et ajoutent les fonctionnalités auxiliaires.

Il est important de savoir que Django fourni en tant que framework plusieurs outils facilitant le travail avec une base de données. Chaque table de notre BD est représenté par ce qu'on appelle un modèle, c'est un simple fichier Python qui contient les informations de notre table. Ces fichiers permettent ensuite à Django de générer lui-même les tables et ensuite de fournir une série de méthodes qui permettent de communiquer avec la BD sans utiliser directement SQL qui est le seul language que comprend la BD. Django nous évite donc d'apprendre un nouveau language. Nous verrons ces méthodes plus tard dans les exemples d'utilisation.

##########
Les cours
##########

************
La structure
************

.. figure:: images/uml_courses.png
    :scale: 90%
    :align: center

    Le schema de toutes les tables du modèle relationnel

Le fait que la structure des tables relationnelles reflètent la structure que perçoit le rédacteur facilitent grandement la compréhension. Nous avons vu qu'un cours de compose de plusieurs pages, qui elles-mêmes contiennent plusieurs sections avec un titre et un contenu et que l'auteur pouvait ajouter ou retirer des éléments à sa guise. C'est exactement la même chose dans le modèle. Tout d'abord on trouve une tables ``courses`` qui contient les informations de base qu'entre le professeur au début du processus et qui sont les colonnes suivantes: ``name``, ``description``, ``difficulty``, il reste le champs ``chaptitre`` que nous verrons plus tard. Ensuite il y a la table ``pages`` avec les colonnes ``name`` qui est le titre de la page, ``order`` qui est un nombre qui permet de trier les pages d'un cours entre elles et de permettre de rérganiser l'ordre et ``course_id`` qui signale la relation avec le cours. En effet chaque page appartient à un cours et vice-versa un cours possède donc plusieurs page, grâce à la clé étrangère - champs qui contient l'ID, l'identifiant d'un enregistrement d'une autre table - ``course_id`` qui relie les deux tables. L'utilisation plus précise de la relation est expliqué dans la partie suivante. Finalement pour terminer l'ensemble il reste la table ``sections`` qui a les colonnes ``name``, ``content``, ``order`` et ``page_id``, un titre, un contenu, et à l'instar des pages un order et une clé étrangère qui la relie à une page. Donc une section appartient à une page et une page a plusieurs sections. A noter que ces trois tables possèdent également les champs ``created_at`` et ``updated_at`` qui enregistrent la date et l'heure de la création et la dernière mise à jour de l'entité. Pour résumé les relations, un cours a plusieurs pages et chacune de ses pages a plusieurs sections. Comme dit précédement on comprend facilement les relations en observant comment les tables sont implémentés dans l'interface de rédaction d'un cours.

.. figure:: images/schema_cours.png
    :scale: 80%
    :align: center

    Schema qui résume les relations des tables courses, pages et sections


***********
Utilisation
***********

Tous les examples d'opérations sur la base de données sont d'abord écrit avec les méthodes de Django puis en SQL pur. Une des particularités de Django quant il s'agit de sauvegarder des objets dans la base de données est qu'il fait appelle à des formulaires, nommé dans le code sous forme de ....Form, comme CourseForm par exemple. On utilise ces mêmes formulaires dans les vues pour générer les formulaires HTML que complètent les utilisateurs, comme pour s'inscrire sur le site. Ils permettent en fait de simplement relier les données soumises par les utilisateurs à nos modèles Django (je rappelle que les modèles sont dans Django la représentation de nos tables de la BD) et par conséquent de créer ou mettre à jour des enregistrements via des formulaires HTML. Pour bien se représenter le concept, lorsqu'un utilisateur soumet un formulaire, le navigateur envoie les données au serveur sous la forme d'un dictionnaire qui ressemble à cela: {"titre" : "La géométrie", "description" : "Bla bla"}. On récupère ensuite dans le code ce dictionnaire et on enregistre les données dans la BD.

Récupère tous les cours afin de créer une liste avec un lien pour pouvoir se rendre sur le page de lecture d'un cours.

.. code-block:: python

    Course.objects.all()

.. code-block:: sql

    SELECT * FROM courses

Créer un nouveau cours. On crée d'abord le cours, puis une page associée contenant une section.

.. code-block:: python
    
    # on utilise un formulaire
    # request.data est un dictionnaire contenant les données soumise par un utilisateur: ici les informations du cours
    course_form = CourseForm(request.data)
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
    INSERT INTO courses (name, description, difficulty, author_id, chapter_id, created_at, updated_at) VALUES ("L'algèbre", "Lorem ipsum...", 1, 1, 1, *, *)
    -- => ID du cours = 1
    -- On crée la page associée
    INSERT INTO pages (name, order, course_id, created_at, updated_at) VALUES ("Première page", 1, 1, *, *)
    -- => ID de la page = 1
    -- on crée une section associée à la page
    INSERT INTO sections (name, content, order, course_id, created_at, updated_at) VALUES ("Première section", "", 1, 1, *, *)

Mettre à jour le contenu d'une page d'un cours. Le titre de la page, le titre et le contenu des sections vont être sauvegardé. Pour accomplir cela on commence par simplement enregistrer la page avec les nouvelles données par la même procédure que pour la création d'un cours. Remarquez simplement dans ``page_form = PageForm(request.data, instance=page)`` qu'on passe en paramètre la page provenant de la base de données pour signaler à Django que l'enregistrement existe déjà et que par conséquent il faut non pas le créer mais le mettre à jour. Pour les sections, on itère le dictionnaire qui contient les données de toutes les sections de la page et ensuite pour chaque section on accomplit la même procédure que pour une page.

.. code-block:: python
    
    # Récupère la page à editer
    page = Page.objects.get(id=page_id)
    # On utilise un formulaire
    # request.data est un dictionnaire contenant les données soumise par un utilisateur: ici le contenu de la page
    page_form = PageForm(request.data, instance=page)
    if page_form.is_valid():
        # On enregistre la page - sauvegarde le titre
        page_form.save()
    # On récupère le dictionnaire contenant seulement les sections
    sections_params = request.data['sections']
    # On fait une boucle pour chaque section
    for section_params in sections_params:
        # On récupère la section
        section = Section.objects.get(id=section_params['id'])
        # On utilise un formulaire
        # section_params est un dictionnaire contenant le titre et le contenu de la section
        section_form = SectionForm(section_params, instance=section)
        if section_form.is_valid():
            # On enregistre la section
            section_form.save()

.. code-block:: sql
    
    -- Récupère la page à editer
    SELECT * FROM pages WHERE id = page_id
    -- On enregistre la page
    UPDATE pages SET name = "Nouveau titre" WHERE id = 1
    -- On enregistre la section
    UPDATE sections SET name = "Nouveau titre", "content" = "Lorem ispum" WHERE id = 1

##############
Les chapitres
##############

Pour pouvoir organiser le contenu du site, cours, exercices, quiz, est toujours associé à un chapitre. Deux tables servent à cette objectif. Tout d'abord la table ``themes`` avec un champs ``name`` et la table ``chapters`` avec un champs ``name`` et ``theme_id`` qui associe chaque thème à un chapitre. Ensuite les tables comme ``courses`` ont un champs ``chapter_id`` qui les relient à un chapitre et donc à un thème aussi. On peut légitement se demander pourquoi ces deux niveaux, ces deux tables ? Cela laisse une plus grande souplesse et liberté pour organiser le contenu et l'afficher. En effet imaginons qu'il y ait 10, 20, 30 ou plus chapitres, comment s'y retrouver ? On les regroupe sous une idée plus générale, et c'est là le rôle de la table ``themes``.    

#################
Les commentaires
#################

###############
La progression
###############

############
Les favoris
############

#############
Les demandes
#############
