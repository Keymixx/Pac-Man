PAC-MAN (42 project)
====================

LANCER LE JEU
-------------
Extraire l'archive, puis dans le dossier extrait :
    ./pacman
(Linux x86_64. Le dossier doit rester en ecriture : le highscore y est sauvegarde.)

CONTROLES
---------
Menu principal :
    ESPACE      lancer une partie
    F11         plein ecran on/off
    ECHAP       quitter

En jeu :
    Fleches     diriger Pac-Man (haut / bas / gauche / droite)
    ECHAP       pause
    F11         plein ecran on/off

Menu pause :
    HAUT / BAS  choisir une option
    ENTREE      valider (reprendre la partie / retour au menu principal)
    ECHAP       reprendre la partie

Fin de partie (saisie du nom pour le highscore) :
    Lettres     saisir le nom
    RETOUR ARRIERE  effacer
    ENTREE      valider
    ECHAP       quitter l'ecran

MODE CHEAT
----------
    F1          active / desactive le mode cheat
    Puis (cheat actif) :
    N           niveau suivant
    L           +1 vie
    I           invincibilite on/off
    F           fantomes geles on/off

CONFIGURATION
-------------
Le fichier config.json (a cote de l'executable) peut etre modifie :
    highscore_filename        fichier de sauvegarde des scores
    percent_pacgum            densite de pac-gommes
    points_per_pacgum         points par pac-gomme
    points_per_super_pacgum   points par super pac-gomme
    points_per_ghost          points par fantome mange
    levels                    liste des niveaux : name, width, height,
                              level_max_time (secondes)
Les lignes commencant par # sont ignorees.
En cas d'erreur de configuration, le jeu affiche un message et s'arrete.

HIGHSCORE
---------
Les 10 meilleurs scores sont sauvegardes dans highscore.json
(cree automatiquement a cote de l'executable).
