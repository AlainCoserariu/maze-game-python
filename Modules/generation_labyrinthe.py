###############################################################################
#                            Module de Project X                              #
#                           génération_labyrinthe                             #
#                     Valentin Bernier - Alain Coserariu                      #
###############################################################################


import random
import fltk
from Modules import utilitaire as util


###############################################################################
#                         Affichage écran de chargement                       #
###############################################################################


def afficher(labyrinthe, intersections, position, coin_sup_gauche_x,
             coin_sup_gauche_y, taille_carres, passer):
    """
    Affiche à chaque étape de génération du labyrinthe l'état de celui ci.
    Les carrés rouges représentent les cases accessible par le joueur.
    Les carrés noirs représentent les murs.
    Les carrés jaune représentent les intersections.
    Le corrés vert représente la sortie.
    Le carrés bleu représente le départ.

    :param labyrinthe: Schéma en cours de construction du labyrinthe
    :param intersections: Autre chemins possible qui n'a pas été pris par le
    curseur
    :param position: Position du curseur
    :param coin_sup_gauche_x: Coordonnées du coin supérieur gauche en x
    :param coin_sup_gauche_y: Coordonnées du coin supérieur gauche en y
    :param taille_carres: Tailles des carrés représentants les parties du
        labyrinthe
    :param passer: Booléen indiquant si l'affichage a lieu
    """
    if not passer:
        case_adjacente_position = [(position[0], position[1]),
                                   (position[0] - 1, position[1]),
                                   (position[0] + 1, position[1]),
                                   (position[0], position[1] + 1),
                                   (position[0], position[1] - 1)]

        for e in case_adjacente_position:
            affichage_couleurs(labyrinthe, e[0], e[1], coin_sup_gauche_x,
                               coin_sup_gauche_y, taille_carres, intersections)
        fltk.mise_a_jour()


def afficher_case(case, coin_sup_gauche_x, coin_sup_gauche_y, taille_carres,
                  couleur, remplissage):
    """
    Affiche les cases représentatif du labyrinthe

    :param case: Case à verifier
    :param coin_sup_gauche_x: Position en x coin du supérieur gauche labyrinthe
    :param coin_sup_gauche_y: Position en y coin du supérieur gauche labyrinthe
    :param taille_carres: taille d'une case
    :param couleur: Couleur de la case
    :param remplissage: Couleur interieur de la case
    """
    fltk.rectangle(coin_sup_gauche_x + case[0] * taille_carres,
                   coin_sup_gauche_y + case[1] * taille_carres,
                   coin_sup_gauche_x + case[0] * taille_carres + taille_carres,
                   coin_sup_gauche_y + case[1] * taille_carres + taille_carres,
                   remplissage=couleur, couleur=remplissage)


def regeneration_labyrinthe(labyrinthe, largeur, hauteur, intersection,
                            taille_carres, passer):
    """
    Affiche tous les éléments du labyrinthe

    :param labyrinthe: Schéma du labyrinthe en construction
    :param largeur: Largeur du labyrinthe
    :param hauteur: Hauteur du labyrinthe
    :param intersection: Autre chemins possible qui n'a pas été pris par le
        curseur
    :param taille_carres: Tailles des carrés représentants les parties du
        labyrinthe
    :param passer: Booléen indiquant si l'affichage a lieu
    """
    if not passer:
        fltk.efface_tout()

        coin_sup_gauche_x = util.TAILLE_FENETRE[
                                0] / 2 - largeur * taille_carres / 2
        coin_sup_gauche_y = util.TAILLE_FENETRE[
                                1] / 2 - hauteur * taille_carres / 2

        contour_ecran_chargement(largeur, hauteur, taille_carres)

        for y in range(len(labyrinthe)):
            for x in range(len(labyrinthe[y])):
                affichage_couleurs(labyrinthe, x, y, coin_sup_gauche_x,
                                   coin_sup_gauche_y, taille_carres,
                                   intersection)


def affichage_couleurs(labyrinthe, x, y, coin_sup_gauche_x, coin_sup_gauche_y,
                       taille_carres, intersection):
    """
    Affiche les cases colorées représentant le labyrinthe

    :param labyrinthe: Liste de listes représentant le labyrinthe
    :param x: Abscisse de la case dans le labyrinthe
    :param y: Ordonnée de la case dans le labyrinthe
    :param coin_sup_gauche_x: Abscisse du coin supérieur gauche
    :param coin_sup_gauche_y: Ordonnée du coin supérieur gauche
    :param taille_carres: Taille des carrés
    :param intersection: Liste des intersections
    """
    # Mur
    if labyrinthe[y][x] == "*":
        afficher_case((x, y), coin_sup_gauche_x, coin_sup_gauche_y,
                      taille_carres, 'black', 'black')
    # Sortie
    elif labyrinthe[y][x] == "x":
        afficher_case((x, y), coin_sup_gauche_x, coin_sup_gauche_y,
                      taille_carres, 'green', 'green')
    # Chemin
    elif labyrinthe[y][x] == ".":
        afficher_case((x, y), coin_sup_gauche_x, coin_sup_gauche_y,
                      taille_carres, 'red', 'red')
    # Emplacement de départ
    elif labyrinthe[y][x] == '@':
        afficher_case((x, y), coin_sup_gauche_x, coin_sup_gauche_y,
                      taille_carres, 'blue', 'blue')
    # Intersection
    elif (x, y) in intersection:
        afficher_case((x, y), coin_sup_gauche_x, coin_sup_gauche_y,
                      taille_carres, 'yellow', 'yellow')


def contour_ecran_chargement(largeur, hauteur, taille_carres):
    """
    Affiche des bords noirs autour de l'écran de chargement et les textes
    """
    coin_sup_gauche_x\
        = util.TAILLE_FENETRE[0] / 2 - largeur * taille_carres / 2
    coin_sup_gauche_y\
        = util.TAILLE_FENETRE[1] / 2 - hauteur * taille_carres / 2
    coin_inf_droit_x\
        = util.TAILLE_FENETRE[0] / 2 + largeur * taille_carres / 2
    coin_inf_droit_y\
        = util.TAILLE_FENETRE[1] / 2 + hauteur * taille_carres / 2

    # Bords noirs
    fltk.rectangle(0, 0, util.TAILLE_FENETRE[0], coin_sup_gauche_y,
                   remplissage="black")
    fltk.rectangle(0, 0, coin_sup_gauche_x, util.TAILLE_FENETRE[1],
                   remplissage='black')
    fltk.rectangle(coin_inf_droit_x, 0, util.TAILLE_FENETRE[0],
                   util.TAILLE_FENETRE[1],
                   remplissage='black')
    fltk.rectangle(0, coin_inf_droit_y, util.TAILLE_FENETRE[0],
                   util.TAILLE_FENETRE[1],
                   remplissage='black')

    # Textes
    fltk.texte(util.TAILLE_FENETRE[0] - 10, util.TAILLE_FENETRE[1] - 25,
               'Chargement du labyrinthe en cours...', 'white', ancrage="se",
               taille=20)
    fltk.texte(util.TAILLE_FENETRE[0] - 140, util.TAILLE_FENETRE[1] - 10,
               'Appuyez sur un bouton pour passer.', 'white', ancrage="se",
               taille=10)


###############################################################################
#                            Génération labyrinthe                            #
###############################################################################


def murs_exterieur_labyrinthe(labyrinthe, largeur):
    """
    Génére la couche de mur extérieur d'un labyrinthe

    :param labyrinthe: labyrinthe vide de tout schéma
    :param largeur: Largeur du labyrinthe
    """
    i = [0, 1, -1, -2]
    for e in i:
        labyrinthe[e] = ["*"] * largeur
    for k in labyrinthe:
        for e in i:
            k[e] = '*'


def generer_murs(labyrinthe, position_possible, intersection):
    """
    Génére les murs du labyrinthe à chaque nouvelle étape dans une direction
    possible prise aléatoirement

    :param labyrinthe: Schéma en construction du labyrinthe
    :param position_possible: position à laquelle peut se déplacer le curseur
    :param intersection: Autre chemins possible qui n'a pas été pris par le
        curseur
    """
    if len(position_possible) >= 2:
        placement_mur = random.choice(position_possible)
        labyrinthe[placement_mur[1]][placement_mur[0]] = '*'

        # On supprime la coordonnée du mur des positions possible et de la
        # liste des intersections
        if placement_mur in intersection:
            intersection.remove(placement_mur)
        position_possible.remove(placement_mur)


def remplir_vides(labyrinthe):
    """
    Remplace les vides restants (v) par des murs (*)

    :param labyrinthe: Liste de listes représentant le labyrinthe
    """
    for y in range(len(labyrinthe)):
        for x in range(len(labyrinthe[y])):
            if labyrinthe[y][x] == 'v':
                labyrinthe[y][x] = '*'


def tirage_taille():
    """
    Génère une taille d'un coté de labyrinthe aléatoire entre 6 et 100

    :return: La taille
    """
    while True:
        taille = random.randint(6, 100)
        if taille <= 50:
            if random.randint(0, int(0.08 * (taille - 25) ** 2)) == 0:
                return taille
        else:
            if random.randint(0, int(0.38 * (taille - 50) ** 2 + 50)) == 0:
                return taille


def generation():
    """
    Génére un schéma de labyrinthe composé de couloirs et de murs.

    :return: labyrinthe, largeur, hauteur
    """
    fltk.efface_tout()
    passer = False

    # Tirage de la taille
    largeur, hauteur = tirage_taille(), tirage_taille()

    # Génération d'un labyrinthe vide (que des v)
    labyrinthe = [["v" for i in range(largeur)] for j in range(hauteur)]

    # Génération aléatoire de l'emplacement de départ de la génération
    position_depart = [random.randint(2, largeur - 3),
                       random.randint(2, hauteur - 3)]
    position = position_depart[:]

    # Initialisation de la taille des carrés de l'affichage
    taille_carres = 5
    coin_sup_gauche_x\
        = util.TAILLE_FENETRE[0] / 2 - largeur * taille_carres / 2
    coin_sup_gauche_y\
        = util.TAILLE_FENETRE[1] / 2 - hauteur * taille_carres / 2

    murs_exterieur_labyrinthe(labyrinthe, largeur)

    regeneration_labyrinthe(labyrinthe, largeur, hauteur, [], taille_carres,
                            passer)

    # Initialisations de variables nécessaires à la génération
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    intersection = []
    derniere_position = None

    while True:

        # Détection d'événement fltk
        evenement = fltk.donne_ev()
        type_evenement = fltk.type_ev(evenement)

        # Passer si un evenement quelconque se produit
        if type_evenement is not None:
            passer = True

        position_possible = []
        labyrinthe[position[1]][position[0]] = "."

        # Pour chaque direction, on regarde si la case est vide
        for e in directions:
            if labyrinthe[position[1] + e[1]][position[0] + e[0]] == 'v':
                position_possible.append((position[0] + e[0],
                                          position[1] + e[1]))

        if position_possible:
            # Créé un mur si il y a au moins deux positions possibles
            generer_murs(labyrinthe, position_possible, intersection)

            # Deplace le curseur sur une postion possible aléatoire
            position = random.choice(position_possible)
            derniere_position = position
            position_possible.remove(position)

            # Mémorise les positions possibles restantes en tant
            # qu'intersection
            for e in position_possible:
                intersection.append(e)

        else:
            # Si pas de position possible mais si il y a des intersections,
            # déplace le curseur sur l'une des intersections
            if intersection:
                position = random.choice(intersection)
                intersection.remove(position)

                # Actualise l'affichage (si il n'a pas été passé)
                if random.randint(1, max(largeur // 2, hauteur // 2)) == 1:
                    regeneration_labyrinthe(labyrinthe, largeur, hauteur,
                                            intersection, taille_carres,
                                            passer)

            # Si plus de possibilités, termine la génération
            else:
                labyrinthe[position_depart[1]][position_depart[0]] = '@'
                labyrinthe[derniere_position[1]][derniere_position[0]] = "x"

                # Remplace les vides restants par des murs
                remplir_vides(labyrinthe)

                # Actualise l'affichage
                regeneration_labyrinthe(labyrinthe, largeur, hauteur,
                                        intersection, taille_carres, passer)

                return labyrinthe, largeur, hauteur

        # Affiche les éléments autour du curseur
        afficher(labyrinthe, intersection, position, coin_sup_gauche_x,
                 coin_sup_gauche_y, taille_carres, passer)
