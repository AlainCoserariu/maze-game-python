###############################################################################
#                            Module de Project X                              #
#                                    Jeu                                      #
#                     Valentin Bernier - Alain Coserariu                      #
###############################################################################


import fltk
from Modules import utilitaire as util
from Modules import sauvegarde
from Modules import generation_labyrinthe
from random import randrange
import time


###############################################################################
#                                Affichage                                    #
###############################################################################


def affichage(labyrinthe, position, direction, carte, nb_laby, temps,
              temps_total_restant, temps_restant, score, largeur, hauteur):
    """
    Affiche tous les éléments du jeu

    :param labyrinthe: Liste des éléments du labyrinthe
    :param position: Couple des coordonnées de la position du joueur
    :param direction: Direction du regard du joueur
    :param carte: Liste des éléments de la carte
    :param nb_laby: Nombre de labyrinthe parcouru
    :param temps: Temps de jeu total
    :param temps_total_restant: Temps restant avant la defaite
    :param temps_restant: Temps restant pour finir le labyrinthe
    :param score: Score du joueur
    :param largeur: Largeur du labyrinthe
    :param hauteur: Hauteur du labyrinthe
    """
    fltk.efface_tout()

    # Labyrinthe
    affichage_labyrinthe(labyrinthe, position, direction)

    # Interface
    affichage_interface(direction, nb_laby, temps, temps_total_restant,
                        temps_restant, score, largeur, hauteur)

    # Carte
    affiche_carte(carte, position, direction)

    fltk.mise_a_jour()


def affichage_interface(direction, nb_laby, temps, temps_total_restant,
                        temps_restant, score, largeur, hauteur):
    """
    Affiche les éléments de l'interface

    :param direction: Direction du regard du joueur
    :param nb_laby: Nombre de labyrinthe parcouru
    :param temps: Temps de jeu total
    :param temps_total_restant: Temps restant avant la defaite
    :param temps_restant: Temps restant pour finir le labyrinthe
    :param score: Score du joueur
    :param largeur: Largeur du labyrinthe
    :param hauteur: Hauteur du labyrinthe
    """
    fltk.image(0, 0, "Assets/Interface/interface.png", ancrage="nw")

    affichage_boussole(direction)

    fltk.texte(1450, 350, "{:0>3d}".format(nb_laby), ancrage="center")

    fltk.texte(330, 105, "{:0>2d}:{:0>2d}".format(temps // 60, temps % 60),
               ancrage="center")

    fltk.texte(610, 105, "{:0>2d}:{:0>2d}".format(temps_total_restant // 60,
                                                  temps_total_restant % 60),
               ancrage="center")

    if temps_restant >= 0:
        fltk.texte(890, 105, "{:0>2d}:{:0>2d}".format(temps_restant // 60,
                                                      temps_restant % 60),
                   ancrage="center")
    else:
        fltk.texte(890, 105, "{:0>2d}:{:0>2d}".format(-temps_restant // 60,
                                                      -temps_restant % 60),
                   couleur="red", ancrage="center")

    fltk.texte(1170, 105, "{:0>6d}".format(score), ancrage="center")

    fltk.texte(1450, 475, f"{largeur}x{hauteur}", ancrage="center")


def affichage_labyrinthe(laby, pos, rot, i=0):
    """
    Affiche les éléments au niveau de la case où se trouve le joueur et
    appelle les fonctions d'affichage des autres cases si nécessaire

    :param laby: Liste des éléments du labyrinthe
    :param pos: Couple des coordonnées de la position du joueur
    :param rot: Rotation, direction du regard du joueur
    :param i: Indice indiquant la hauteur de l'affichage des textures
        (pour les animations)
    """
    # Sol et ciel
    affichage_decors("pos_sol", i)

    # Face
    if laby[pos[1] + rot[1]][pos[0] + rot[0]] != "*":
        aff_laby_face(laby, pos, rot, i)
    else:
        # Face Doite
        if laby[pos[1] + rot[0] + rot[1]][pos[0] - rot[1] + rot[0]] != "*":
            aff_laby_droite(laby, [pos[0] + rot[0], pos[1] + rot[1]], rot, i)
        # Face Gauche
        if laby[pos[1] - rot[0] + rot[1]][pos[0] + rot[1] + rot[0]] != "*":
            aff_laby_gauche(laby, [pos[0] + rot[0], pos[1] + rot[1]], rot, i)

        affichage_decors("pos_face", i)

    # Droite
    if laby[pos[1] + rot[0]][pos[0] - rot[1]] == "*":
        affichage_decors("pos_droite", i)
    else:
        affichage_decors("pdr_sol", i)
        if laby[pos[1] + rot[0] + rot[1]][pos[0] - rot[1] + rot[0]] == "*":
            affichage_decors("pdr_face", i)

    # Gauche
    if laby[pos[1] - rot[0]][pos[0] + rot[1]] == "*":
        affichage_decors("pos_gauche", i)
    else:
        affichage_decors("pga_sol", i)
        if laby[pos[1] - rot[0] + rot[1]][pos[0] + rot[1] + rot[0]] == "*":
            affichage_decors("pga_face", i)


def aff_laby_face(laby, pos, rot, i):
    """
    Affiche les élément au niveau de la case en face du joueur et
    appelle les fonctions d'affichage des autres cases si nécessaire

    :param laby: Liste des éléments du labyrinthe
    :param pos: Couple des coordonnées de la position du joueur
    :param rot: Rotation, direction du regard du joueur
    :param i: Indice indiquant la hauteur de l'affichage des textures
        (pour les animations)
    """
    pos_face = [pos[0] + rot[0], pos[1] + rot[1]]

    # Sol et ciel
    affichage_decors("vue_sol", i)

    # Sortie en face
    if laby[pos_face[1]][pos_face[0]] == "x":
        affichage_decors("vue_sortie", i)

    # Case en face
    if laby[pos_face[1] + rot[1]][pos_face[0] + rot[0]] != "*":
        aff_laby_fond(laby, pos_face, rot, i)
    else:
        affichage_decors("vue_face", i)

    # Case à droite
    if laby[pos_face[1] + rot[0]][pos_face[0] - rot[1]] != "*":
        aff_laby_droite(laby, pos_face, rot, i)
    else:
        affichage_decors("vue_droite", i)

    # Case à gauche
    if laby[pos_face[1] - rot[0]][pos_face[0] + rot[1]] != "*":
        aff_laby_gauche(laby, pos_face, rot, i)
    else:
        affichage_decors("vue_gauche", i)


def aff_laby_droite(laby, pos_face, rot, i):
    """
    Affiche les éléments au niveau de la case à droite de la case en face
    du joueur

    :param laby: Liste des éléments du labyrinthe
    :param pos_face: Couple des coordonnées de la position en face du joueur
    :param rot: Rotation, direction du regard du joueur
    :param i: Indice indiquant la hauteur de l'affichage des textures
        (pour les animations)
    """
    pos_droite = [pos_face[0] - rot[1], pos_face[1] + rot[0]]

    # Sol et Ciel
    affichage_decors("vdr_sol", i)

    # Sortie à droite
    if laby[pos_droite[1]][pos_droite[0]] == "x":
        affichage_decors("vdr_sortie", i)

    # Face
    if laby[pos_droite[1] + rot[1]][pos_droite[0] + rot[0]] == "*":
        affichage_decors("vdr_face_plein", i)
    else:
        affichage_decors("vdr_face_vide", i)

    # Droite
    if laby[pos_droite[1] + rot[0]][pos_droite[0] - rot[1]] == "*":
        affichage_decors("vdr_droite_plein", i)
    else:
        affichage_decors("vdr_droite_vide", i)


def aff_laby_gauche(laby, pos_face, rot, i):
    """
    Affiche les éléments au niveau de la case à gauche de la case en face
    du joueur

    :param laby: Liste des éléments du labyrinthe
    :param pos_face: Couple des coordonnées de la position en face du joueur
    :param rot: Rotation, direction du regard du joueur
    :param i: Indice indiquant la hauteur de l'affichage des textures
        (pour les animations)
    """
    pos_gauche = [pos_face[0] + rot[1], pos_face[1] - rot[0]]

    # Sol et Ciel
    affichage_decors("vga_sol", i)

    # Sortie à gauche
    if laby[pos_gauche[1]][pos_gauche[0]] == "x":
        affichage_decors("vga_sortie", i)

    # Face
    if laby[pos_gauche[1] + rot[1]][pos_gauche[0] + rot[0]] == "*":
        affichage_decors("vga_face_plein", i)
    else:
        affichage_decors("vga_face_vide", i)

    # Gauche
    if laby[pos_gauche[1] - rot[0]][pos_gauche[0] + rot[1]] == "*":
        affichage_decors("vga_gauche_plein", i)
    else:
        affichage_decors("vga_gauche_vide", i)


def aff_laby_fond(laby, pos_face, rot, i):
    """
    Affiche les élément au niveau de la case qui se trouve deux cases
    devant le joueur

    :param laby: Liste des éléments du labyrinthe
    :param pos_face: Couple des coordonnées de la position en face du joueur
    :param rot: Rotation, direction du regard du joueur
    """
    pos_fond = [pos_face[0] + rot[0], pos_face[1] + rot[1]]

    # Sol et Ciel
    affichage_decors("vvue_sol", i)

    # Sortie au fond
    if laby[pos_fond[1]][pos_fond[0]] == "x":
        affichage_decors("vvue_sortie", i)

    # Face
    if laby[pos_fond[1] + rot[1]][pos_fond[0] + rot[0]] == "*":
        affichage_decors("vvue_face_plein", i)
    else:
        affichage_decors("vvue_face_vide", i)

    # Droite
    if laby[pos_fond[1] + rot[0]][pos_fond[0] - rot[1]] == "*":
        affichage_decors("vvue_droite_plein", i)
    else:
        affichage_decors("vvue_droite_vide", i)

    # Gauche
    if laby[pos_fond[1] - rot[0]][pos_fond[0] + rot[1]] == "*":
        affichage_decors("vvue_gauche_plein", i)
    else:
        affichage_decors("vvue_gauche_vide", i)


def affichage_decors(nom_texture, i):
    """
    Affiche l'élément du décors donné en paramètre dans le fenetre du jeu

    :param nom_texture: Chaine de caracteres correspondant au nom de la partie
        du décors à afficher
    :param i: Indice indiquant la hauteur de l'affichage des textures
        (pour les animations)
    """
    fltk.image(util.COOR_FEN_JEU[0][0], util.COOR_FEN_JEU[0][1] + i * 100,
               f"Assets/Decors/{nom_texture}.png", ancrage="nw")


def affichage_boussole(direcetion):
    """
    Affiche la boussole en haut à gauche de l'interface en fonction de
    l'orientation du joueur

    :param direction: Liste de la direction du regard du joueur
    """
    if direcetion == [1, 0]:
        fltk.image(5, 5, "Assets/Interface/boussole_e.png", ancrage="nw")
    elif direcetion == [0, -1]:
        fltk.image(5, 5, "Assets/Interface/boussole_n.png", ancrage="nw")
    elif direcetion == [-1, 0]:
        fltk.image(5, 5, "Assets/Interface/boussole_o.png", ancrage="nw")
    elif direcetion == [0, 1]:
        fltk.image(5, 5, "Assets/Interface/boussole_s.png", ancrage="nw")


###############################################################################
#                                  Carte                                      #
###############################################################################


def affiche_carte(carte, pos, rot):
    """
    Affiche la carte dans le coin de l'écran

    :param carte: Liste des éléments de la carte
    :param pos: Couple des coordonnées de la position du joueur
    :param rot: Rotation, direction du regard du joueur
    """
    # On garde que les cases à 6 cases ou moins du joueur
    carte_visuel = redimension_carte(carte, pos)

    for j in range(13):
        for i in range(13):
            x, y = coord_case_carte(i, j)

            # Au centre de la carte, affichage du joueur
            if i == 6 and j == 6:
                affichage_joueur_carte(x, y, rot)

            else:
                # Affichage des murs (carré noir)
                if carte_visuel[j][i] == "*":
                    fltk.rectangle(x - 10, y - 10, x + 10, y + 10,
                                   remplissage="black")

                # Affichage de la sortie (carré vert)
                if carte_visuel[j][i] == "x":
                    fltk.rectangle(x - 7, y - 7, x + 7, y + 7,
                                   remplissage="lime")

                # Affichage du point de départ (rond bleu)
                if carte_visuel[j][i] == "@":
                    fltk.cercle(x, y, 5, remplissage="cyan")


def affichage_joueur_carte(x, y, rot):
    """
    Affiche le joueur représenté par un triangle rouge sur la carte
    Il est orienté en fonction de la direction du joueur

    :param x: Coordonnée x où afficher le joueur
    :param y: Coordonnée y où afficher le joueur
    :param rot: Direction du joueur
    """
    # Nord
    if rot == [0, -1]:
        fltk.polygone([(x, y - 7), (x + 7, y + 7), (x - 7, y + 7)],
                      remplissage="red")

    # Sud
    elif rot == [0, 1]:
        fltk.polygone([(x, y + 7), (x + 7, y - 7), (x - 7, y - 7)],
                      remplissage="red")

    # Ouest
    elif rot == [-1, 0]:
        fltk.polygone([(x - 7, y), (x + 7, y + 7), (x + 7, y - 7)],
                      remplissage="red")

    # Est
    elif rot == [1, 0]:
        fltk.polygone([(x + 7, y), (x - 7, y + 7), (x - 7, y - 7)],
                      remplissage="red")


def redimension_carte(carte, pos):
    """
    Créé une liste ne contenant les éléments que 6 cases autour du joueur

    :param carte: Liste des éléments de la carte
    :param pos: Couple des coordonnées de la position du joueur
    :return: Liste des éléments 6 cases autour du joueur
    """
    carte_visuel = [["" for i in range(13)] for j in range(13)]

    # On "regarde" toutes les cases autour du joueur (rayon de 6)
    b = 0
    for j in range(pos[1] - 6, pos[1] + 7):
        a = 0
        for i in range(pos[0] - 6, pos[0] + 7):

            try:
                if i < 0 or j < 0:
                    # Si les valeurs sont négatives, on met des murs
                    carte_visuel[b][a] = "*"
                else:
                    # On remplit la carte de 13x13 avec les éléments du
                    # labyrinthe correspondants
                    carte_visuel[b][a] = carte[j][i]
            except IndexError:
                # Si on dépasse de la liste, on met des murs
                carte_visuel[b][a] = "*"

            a += 1
        b += 1
    return carte_visuel


def coord_case_carte(i, j):
    """
    Convertis les coordonnées des points de la carte (de 0 à 12) en pixels
    correspondants au centre du carré à dessiner

    :param i: Coordonnée aux abscisses
    :param j: Coordonnées aux ordonnées
    :return: Couple des coordonnées converties

    >>> coord_case_carte(0, 0)
    (1330, 650)

    >>> coord_case_carte(4, 2)
    (1410, 710)
    """
    x = util.TAILLE_FENETRE[0] - 270 + 20 * i
    y = util.TAILLE_FENETRE[1] - 270 + 20 * j

    return x, y


def init_carte(largeur, hauteur):
    """
    Créé une liste de listes de points avec un tour de * de 2 de large

    :param largeur: Largeur du labyrinthe
    :param hauteur: Hauteur du labyrinthe
    :return: Liste des éléments de la carte

    >>> init_carte(6, 5)
    [['*', '*', '*', '*', '*', '*'], ['*', '*', '*', '*', '*', '*'],\
        ['*', '*', '.', '.', '*', '*'], ['*', '*', '*', '*', '*', '*'],\
        ['*', '*', '*', '*', '*', '*']]
    """
    # Création d'une carte vide (que des .)
    carte = [["." for i in range(largeur)] for j in range(hauteur)]
    i = [0, 1, -1, -2]

    # 2 lignes de murs en haut et en bas
    for e in i:
        carte[e] = ["*"] * largeur

    # 2 colones de murs à droite et à gauche
    for k in carte:
        for e in i:
            k[e] = '*'
    return carte


def actualise_carte(carte, laby, pos, rot):
    """
    Actualise la liste carte en fonction de la nouvelle position et rotation
    du joueur dans le labyrinthe

    :param carte: Liste des éléments de la carte
    :param laby: Liste des éléments du labyrinthe
    :param pos_face: Couple des coordonnées de la position en face du joueur
    :param rot: Rotation, direction du regard du joueur
    :return: Liste des éléments de la carte
    """
    # Position du joueur
    carte[pos[1]][pos[0]] = laby[pos[1]][pos[0]]

    # Face
    carte[pos[1] + rot[1]][pos[0] + rot[0]]\
        = laby[pos[1] + rot[1]][pos[0] + rot[0]]
    carte[pos[1] + 2 * rot[1]][pos[0] + 2 * rot[0]]\
        = laby[pos[1] + 2 * rot[1]][pos[0] + 2 * rot[0]]

    # Droite
    carte[pos[1] + rot[0]][pos[0] - rot[1]]\
        = laby[pos[1] + rot[0]][pos[0] - rot[1]]
    carte[pos[1] + rot[0] + rot[1]][pos[0] - rot[1] + rot[0]]\
        = laby[pos[1] + rot[0] + rot[1]][pos[0] - rot[1] + rot[0]]

    # Gauche
    carte[pos[1] - rot[0]][pos[0] + rot[1]]\
        = laby[pos[1] - rot[0]][pos[0] + rot[1]]
    carte[pos[1] - rot[0] + rot[1]][pos[0] + rot[1] + rot[0]]\
        = laby[pos[1] - rot[0] + rot[1]][pos[0] + rot[1] + rot[0]]

    return carte


###############################################################################
#                              Déplacements                                   #
###############################################################################


def deplacements_joueur(touche, labyrinthe, position, direction):
    """
    Gère les déplacements du joueur en fonction de la touche pressée

    :param touche: Touche détecté avec fltk
    :param labyrinthe: Liste des éléments du labyrinthe
    :param position: Liste des coordonnées de la position du joueur
    :param direction: Liste de la direction du regard du joueur
    :return: position, direction

    >>> deplacements_joueur("z", [["*", ".", "*"], ["*", ".", "*"],\
        ["*", "*", "*"]], [1, 1], [0, -1])
    ([1, 0], [0, -1])

    >>> deplacements_joueur("d", [["*", ".", "*"], ["*", ".", "*"],\
        ["*", "*", "*"]], [1, 1], [1, 0])
    ([1, 1], [1, 0])

    >>> deplacements_joueur("e", [["*", ".", "*"], ["*", ".", "*"],\
        ["*", "*", "*"]], [1, 1], [0, -1])
    ([1, 1], [1, 0])
    """
    # Avancer
    if touche == 'z':
        pos_temp = [position[0] + direction[0], position[1] + direction[1]]
        if collisions_murs(labyrinthe, pos_temp):
            position = pos_temp[:]

    # Aller a gauche
    elif touche == 'q':
        pos_temp = [position[0] + direction[1], position[1] - direction[0]]
        if collisions_murs(labyrinthe, pos_temp):
            position = pos_temp[:]

    # Reculer
    elif touche == 's':
        pos_temp = [position[0] - direction[0], position[1] - direction[1]]
        if collisions_murs(labyrinthe, pos_temp):
            position = pos_temp[:]

    # Aller a droite
    elif touche == 'd':
        pos_temp = [position[0] - direction[1], position[1] + direction[0]]
        if collisions_murs(labyrinthe, pos_temp):
            position = pos_temp[:]

    # Tourner la caméra
    direction = rotation_joueur(touche, direction)

    return position, direction


def rotation_joueur(touche, direction):
    """
    Gère les rotations du joueur en fonction de la touche pressée

    :param touche: Touche détecté avec fltk
    :param direction: Liste de la direction du regard du joueur
    :return: direction

    >>> deplacements_joueur("e", [["*", ".", "*"], ["*", ".", "*"],\
        ["*", "*", "*"]], [1, 1], [1, 0])
    ([1, 1], [0, 1])

    >>> deplacements_joueur("a", [["*", ".", "*"], ["*", ".", "*"],\
        ["*", "*", "*"]], [1, 1], [-1, 0])
    ([1, 1], [0, 1])
    """
    # Tourner a droite
    if touche == 'e':
        direction = [- direction[1], direction[0]]

    # Tourner a gauche
    elif touche == 'a':
        direction = [direction[1], - direction[0]]

    return direction


def collisions_murs(labyrinthe, position):
    """
    Détecte si le joueur est dans un mur du labyrinthe

    :param labyrinthe: Liste des éléments du labyrinthe
    :param position: Liste des coordonnées de la position du joueur
    :return: False si collision entre le joueur et le mur

    >>> collisions_murs([["*", ".", "*"], ["*", ".", "*"], ["*", "*", "*"]],\
        [1, 0])
    True

    >>> collisions_murs([["*", ".", "*"], ["*", ".", "*"], ["*", "*", "*"]],\
        [1, 2])
    False
    """
    if labyrinthe[position[1]][position[0]] != "*":
        return True
    return False


###############################################################################
#                                Menu Pause                                   #
###############################################################################


def affichage_menu_pause(sauvegarde):
    """
    Affiche le menu pause

    :param sauvegarde: Booléen indiquant si le joueur a cliqué sur le
        bouton sauvegarder
    """
    fltk.efface_tout()

    fltk.image(0, 0, f"Assets/Menu/pause_{sauvegarde}.png", ancrage="nw")

    fltk.mise_a_jour()


def menu_pause(position, direction, carte, labyrinthe, nb_laby, temps,
               temps_total_restant, score, temps_dispo, temps_restant,
               difficulte):
    """
    Détecte le clic sur l'un des boutons du menu de pause et redirige
    l'utilisateur en conséquence

    :param position: Position du joueur dans le labyrinthe
    :param direction: Direction dans laquelle regarde le joueur
    :param carte: Liste des éléments de la carte
    :param labyrinthe: Schéma du labyrinthe
    :param nb_laby: Nombre de labyrinthe parcouru
    :param temps: Temps de jeu total
    :param temps_total_restant: Temps restant avant la defaite
    :param score: Score du joueur
    :param temps_dispo: Temps disponible pour finir le labyrinthe
    :param temps_restant: Temps restant pour finir le labyrinthe
    :param difficulte: Float représentant la difficulté
    :return: Couple de booléens donnant l'état du jeu
        continuer partie = (True, True) ; retour menu = (False, True) ;
        quitter le jeu = (False, False)
    """
    partie_sauvegaardee = False
    while True:

        affichage_menu_pause(partie_sauvegaardee)

        # Détection d'événements fltk
        evenement = fltk.attend_ev()
        type_evenement = fltk.type_ev(evenement)

        if type_evenement == "ClicGauche":

            # Continuer la partie
            if util.clic_dans_rectangle(evenement, 109, 385, 717, 513):
                return True, True

            # Retour au menu
            elif util.clic_dans_rectangle(evenement, 109, 648, 717, 776):
                return False, True

            # Sauvegarder la partie
            elif util.clic_dans_rectangle(evenement, 863, 385, 1471, 513):
                sauvegarde.sauvegarde_partie(position, direction, carte,
                                             labyrinthe, nb_laby, temps,
                                             temps_total_restant, score,
                                             temps_dispo, temps_restant,
                                             difficulte)
                partie_sauvegaardee = True

            # Quitter le jeu
            elif util.clic_dans_rectangle(evenement, 863, 648, 1471, 776):
                return False, False


###############################################################################
#                                  Divers                                     #
###############################################################################


def init_labyrinthe():
    """
    Initialise le labyrinthe, le joueur et la carte

    :return: labyrinthe, largeur, hauteur, position, direction, carte
    """
    labyrinthe, largeur, hauteur = generation_labyrinthe.generation()
    position = init_joueur_position(labyrinthe)
    direction = init_joueur_direction(labyrinthe, position)
    carte = init_carte(largeur, hauteur)

    return (labyrinthe, largeur, hauteur, position, direction, carte)


def init_joueur_position(labyrinthe):
    """
    Trouve les coordonnées de début de partie du joueur

    :param labyrinthe: Liste des éléments du labyrinthe
    :return: position du joueur [x, y]

    >>> init_joueur_position([["*", "*", "*"], ["*", "@", "*"],\
        ["*", "*", "*"]])
    [1, 1]
    """
    for i in range(len(labyrinthe)):
        if "@" in labyrinthe[i]:
            return [labyrinthe[i].index("@"), i]


def init_joueur_direction(labyrinthe, position):
    """
    Initialise la direction du joueur en début de partie en fonction de
    l'environement autour de celui-ci.

    :param labyrinthe: Liste des éléments du labyrinthe
    :param position: Liste des coordonnées [x, y] de la position du joueur
    :return: direction du joueur

    >>> init_joueur_direction([["*", ".", "*"], ["*", ".", "*"],\
        ["*", "*", "*"]], [1, 1])
    [0, -1]
    """
    possibilites = []

    # Nord
    if labyrinthe[position[1] - 1][position[0]] != "*":
        possibilites.append([0, -1])

    # Sud
    if labyrinthe[position[1] + 1][position[0]] != "*":
        possibilites.append([0, 1])

    # Ouest
    if labyrinthe[position[1]][position[0] - 1] != "*":
        possibilites.append([-1, 0])

    # Est
    if labyrinthe[position[1]][position[0] + 1] != "*":
        possibilites.append([1, 0])

    # Tirgage aléatoire
    return possibilites[randrange(0, len(possibilites))]


def sortie_laby(labyrinthe, position):
    """
    Détecte la sortie du labyrinthe si le joueur marche sur la sortie

    :param labyrinthe: Liste des éléments du labyrinthe
    :param position: Couple des coordonnées de la position du joueur
    :return: True si sortie du labyrinthe

    >>> sortie_laby([["*", "x", "*"], ["*", ".", "*"], ["*", "*", "*"]],\
        [1, 0])
    True

    >>> sortie_laby([["*", "x", "*"], ["*", ".", "*"], ["*", "*", "*"]],\
        [1, 1])
    False
    """
    if labyrinthe[position[1]][position[0]] == "x":
        return True
    return False


def choix_difficulte():
    """
    Gère le menu de choix de la difficulté

    :return: Float représentant la difficulté
    """
    while True:

        evenement = fltk.attend_ev()
        type_evenement = fltk.type_ev(evenement)

        # Facile
        if (type_evenement == "ClicGauche" and
                util.clic_dans_rectangle(evenement, 119, 168, 443, 324)):
            return 1

        # Normal
        elif (type_evenement == "ClicGauche" and
                util.clic_dans_rectangle(evenement, 1037, 352, 1405, 504)):
            return 0.75

        # Difficile
        elif (type_evenement == "ClicGauche" and
                util.clic_dans_rectangle(evenement, 386, 565, 732, 762)):
            return 0.5

        # ... (difficulté "secrete")
        elif (type_evenement == "ClicGauche" and
                util.clic_dans_rectangle(evenement, 1563, 873, 1590, 895)):
            return 0.25


def transition_fin_difficulte():
    """
    Affiche l'animation a la fin du choix de la difficulté
    """
    for i in range(10):
        fltk.efface_tout()
        fltk.image(0, 0, "Assets/Menu/ciel_grand.png", "nw")
        fltk.image(0, - i * 100, "Assets/Menu/difficulte.png", "nw")
        fltk.mise_a_jour()
        time.sleep(0.1)
    time.sleep(0.5)


###############################################################################
#                                  Temps                                      #
###############################################################################


def actualise_temps(temps, temps_precedent, temps_total_restant, temps_restant,
                    temps_dispo):
    """
    Actualise les variables liées au temps

    :param temps: Temps de jeu total
    :param temps_precedent: Temps relevé à l'actualisation précédente (sert à
        compter les secondes)
    :param temps_total_restant: Temps restant avant la défaite
    :param temps_restant: Temps restant pour finir le labyrinthe
    :param temps_dispo: Temps total pour finir le labyrinthe
    :return: temps, temps_precedent, temps_total_restant, temps_restant
    """
    # Si une seconde s'est écoulée depuis la dernière actualisation du temps
    if time.time() > temps_precedent + 1:
        temps += 1
        temps_total_restant -= 1
        temps_restant -= 1
        temps_precedent = time.time()

        # Si le joueur dépasse le temps pour finir un labyrinthe, le temps
        # total restant diminue plus rapidement
        if temps_restant < 0:
            temps_total_restant += temps_restant // temps_dispo

    return temps, temps_precedent, temps_total_restant, temps_restant


def actualise_score(surface, temps_dispo, temps_restant):
    """
    Actualise le score

    :param surface: Surface du labyrinthe
    :param temps_dispo: Temps total pour finir le labyrinthe
    :param temps_restant: Temps restant pour finir le labyrinthe
    :return: Score gagné dans le labyrinthe

    >>> actualise_score(100, 60, 30)
    50

    >>> actualise_score(36, 10, 14)
    0
    """
    return max(0, int(surface - (temps_dispo - temps_restant)
                      * (surface / temps_dispo)))


def init_temps(surface, difficulte):
    """
    Initialise les variables liées au temps

    :param surface: Surface du labyrinthe
    :param difficulte: Float représentant la difficulté
    """
    temps = 0
    temps_precedent = time.time()
    temps_total_restant = int(surface * difficulte)
    score = 0

    return temps, temps_precedent, temps_total_restant, score


def reinit_temps(surface, difficulte, largeur, hauteur):
    """
    Reinitialise le temps disponible pour sortir du labyrinthe

    :param surface: Surface du labyrinthe
    :param difficulte: Float représentant la difficulté
    :param largeur: Largeur du labyrinthe
    :param hauteur: Hauteur du labyrinthe
    :return: temps_dispo, temps_restant

    >>> reinit_temps(100, 0.5, 10, 10)
    (17, 17)
    """
    temps_dispo = int(((surface / (largeur + hauteur)) ** 2
                       + surface ** 0.5) * difficulte)
    temps_restant = temps_dispo
    return temps_dispo, temps_restant


def ecran_defaite(temps, score, nb_laby):
    """
    Affiche l'écran de défaite

    :param temps: Temps de jeu
    :param score: Score du joueur
    :param nb_laby: Nombre de labyrinthes terminés
    :return: False
    """
    # Affichage
    fltk.efface_tout()
    fltk.image(0, 0, "Assets/Menu/defaite.png", ancrage="nw")
    fltk.texte(1100, 502, "{:0>3d}".format(nb_laby), ancrage="center")
    fltk.texte(800, 502, "{:0>6d}".format(score), ancrage="center")
    fltk.texte(500, 502, "{:0>2d}:{:0>2d}".format(temps // 60, temps % 60),
               ancrage="center")

    while True:
        evenement = fltk.attend_ev()
        type_evenement = fltk.type_ev(evenement)

        # Retour au menu en cas de clic sur le bouton
        if (type_evenement == "ClicGauche" and
                util.clic_dans_rectangle(evenement, 505, 563, 1108, 666)):
            sauvegarde.effacer_partie()
            return False


def init_partie(nouvelle_partie):
    """
    Initialisation des variables d'une partie

    :param nouvelle_partie: Booléen indiquant si on utilise un fichier de
        sauvegarde ou si c'est une nouvelle partie
    :return: difficulte, labyrinthe, largeur, hauteur, joueur_position,
        joueur_direction, carte, surface, nb_laby, temps, temps_precedent,
        temps_total_restant, score, temps_dispo, temps_restant
    """
    # Si nouvelle partie
    if nouvelle_partie:

        # Difficulté
        difficulte = choix_difficulte()
        transition_fin_difficulte()

        # Labyrinthe
        labyrinthe, largeur, hauteur, joueur_position, joueur_direction,\
            carte = init_labyrinthe()
        surface = largeur * hauteur
        nb_laby = 1

        # temps
        temps, temps_precedent, temps_total_restant, score\
            = init_temps(surface, difficulte)
        temps_dispo, temps_restant = reinit_temps(surface, difficulte,
                                                  largeur, hauteur)

        # Animation d'entrée
        anim_entree_laby(labyrinthe, joueur_position, joueur_direction,
                         nb_laby, temps, temps_total_restant, temps_restant,
                         score, largeur, hauteur)

    # Si chargement de sauvegarde
    else:
        joueur_position, joueur_direction, carte, labyrinthe, nb_laby, temps,\
            temps_total_restant, score, temps_dispo, temps_restant, difficulte\
            = sauvegarde.chargement_partie()
        largeur = len(labyrinthe[0])
        hauteur = len(labyrinthe)
        surface = largeur * hauteur
        temps_precedent = time.time()

    return (difficulte, labyrinthe, largeur, hauteur, joueur_position,
            joueur_direction, carte, surface, nb_laby, temps, temps_precedent,
            temps_total_restant, score, temps_dispo, temps_restant)


def changement_labyrinthe(labyrinthe, joueur_position, joueur_direction,
                          nb_laby, temps, temps_total_restant, temps_restant,
                          score, largeur, hauteur, surface, temps_dispo,
                          difficulte):
    """
    Charge un nouveau labyrinthe et réinitialise les variables nécessaires à la
    fin d'un labyrinthe

    :param labyrinthe: Liste de listes représentant le labyrinthe
    :param joueur_position: Position du joueur
    :param joueur_direction: Direction du joueur
    :param nb_laby: Nombre de labyrinthe parcourus
    :param temps: Temps de jeu total
    :param temps_total_restant: Temps restant avant la défaite
    :param temps_restant: Temps restant pour finir le labyrinthe
    :param score: Score du joueur
    :param largeur: Largeur du labyrinthe
    :param hauteur: Hauteur du labyrinthe
    :param surface: Surface du labyrinthe
    :param temps_dispo: Temps disponible pour finir le labyrinthe
    :param difficulte: Float représentant la difficulté
    :return: score, temps_total_restant, nb_laby, labyrinthe, largeur, hauteur,
        joueur_position, joueur_direction, carte, surface, temps_dispo,
        temps_restant
    """
    # Animation de sortie
    anim_sortie_laby(labyrinthe, joueur_position, joueur_direction,
                     nb_laby, temps, temps_total_restant,
                     temps_restant,
                     score, largeur, hauteur)

    # Mise a jour score et temps total
    score += actualise_score(surface, temps_dispo, temps_restant)
    temps_total_restant += actualise_score(surface, temps_dispo,
                                           temps_restant)

    # Réinitialisation du labyrinthe
    nb_laby += 1
    labyrinthe, largeur, hauteur, joueur_position, joueur_direction, carte\
        = init_labyrinthe()
    surface = len(labyrinthe) * len(labyrinthe[0])
    temps_dispo, temps_restant = reinit_temps(surface, difficulte,
                                              largeur, hauteur)

    # Animation d'entrée
    anim_entree_laby(labyrinthe, joueur_position, joueur_direction,
                     nb_laby, temps, temps_total_restant,
                     temps_restant, score, largeur, hauteur)

    return (score, temps_total_restant, nb_laby, labyrinthe, largeur, hauteur,
            joueur_position, joueur_direction, carte, surface, temps_dispo,
            temps_restant)


###############################################################################
#                      Animation Changement Labyrinthe                        #
###############################################################################


def anim_entree_laby(laby, pos, rot, nb_laby, temps, temps_total_restant,
                     temps_restant, score, largeur, hauteur):
    """
    Affiche l'animation d'entrée dans un labyrinthe

    :param laby: Liste des éléments du labyrinthe
    :param pos: Couple des coordonnées de la position du joueur
    :param rot: Direction du regard du joueur
    :param nb_laby: Nombre de labyrinthe parcouru
    :param temps: Temps de jeu total
    :param temps_total_restant: Temps restant avant la defaite
    :param temps_restant: Temps restant pour finir le labyrinthe
    :param score: Score du joueur
    :param largeur: Largeur du labyrinthe
    :param hauteur: Hauteur du labyrinthe
    """
    for i in range(8, -1, -1):
        fltk.efface_tout()
        fltk.image(util.COOR_FEN_JEU[0][0], util.COOR_FEN_JEU[0][1],
                   "Assets/Menu/ciel.png", ancrage="nw")
        affichage_labyrinthe(laby, pos, rot, i)
        affichage_interface(rot, nb_laby, temps, temps_total_restant,
                            temps_restant, score, largeur, hauteur)
        fltk.mise_a_jour()
        time.sleep(0.1)
    time.sleep(0.5)


def anim_sortie_laby(laby, pos, rot, nb_laby, temps, temps_total_restant,
                     temps_restant, score, largeur, hauteur):
    """
    Affiche l'animation de sortie d'un labyrinthe

    :param laby: Liste des éléments du labyrinthe
    :param pos: Couple des coordonnées de la position du joueur
    :param rot: Direction du regard du joueur
    :param nb_laby: Nombre de labyrinthe parcouru
    :param temps: Temps de jeu total
    :param temps_total_restant: Temps restant avant la defaite
    :param temps_restant: Temps restant pour finir le labyrinthe
    :param score: Score du joueur
    :param largeur: Largeur du labyrinthe
    :param hauteur: Hauteur du labyrinthe
    """
    for i in range(0, -18, -1):
        fltk.efface_tout()
        affichage_labyrinthe(laby, pos, rot, i)
        fltk.image(util.COOR_FEN_JEU[0][0], util.COOR_FEN_JEU[0][1] + i * 100,
                   "Assets/Menu/bas_echelle.png", ancrage="nw")
        affichage_interface(rot, nb_laby, temps, temps_total_restant,
                            temps_restant, score, largeur, hauteur)
        fltk.mise_a_jour()
        time.sleep(0.1)
    time.sleep(0.5)


###############################################################################
#                                Principal                                    #
###############################################################################


def jeu(nouvelle_partie):
    """
    Boucle principale du jeu

    :param nouvelle_partie: Défini si le jeu doit se baser sur une sauvegarde
    :return: booléen indiquant si le programme doit s'arrêter ou retourner sur
    le menu
    """
    # Initialisation des variables
    difficulte, labyrinthe, largeur, hauteur, joueur_position,\
        joueur_direction, carte, surface, nb_laby, temps, temps_precedent,\
        temps_total_restant, score, temps_dispo, temps_restant\
        = init_partie(nouvelle_partie)

    # Boucle du jeu
    partie = True
    reste_sur_jeu = True
    while partie:

        # Mise à jour de la carte
        carte = actualise_carte(carte, labyrinthe, joueur_position,
                                joueur_direction)

        # Affiche les éléments du jeu
        affichage(labyrinthe, joueur_position, joueur_direction, carte,
                  nb_laby, temps, temps_total_restant, temps_restant, score,
                  largeur, hauteur)

        # Détection d'événements fltk
        evenement = fltk.donne_ev()
        type_evenement = fltk.type_ev(evenement)

        # Change de labyrinthe si le joueur marche sur la sortie
        if sortie_laby(labyrinthe, joueur_position):
            score, temps_total_restant, nb_laby, labyrinthe, largeur, hauteur,\
                joueur_position, joueur_direction, carte, surface,\
                temps_dispo, temps_restant = changement_labyrinthe(
                    labyrinthe, joueur_position, joueur_direction, nb_laby,
                    temps, temps_total_restant, temps_restant, score, largeur,
                    hauteur, surface, temps_dispo, difficulte)

        # Redirige vers le menu pause
        if (type_evenement == "Quitte" or
                (type_evenement == "ClicGauche"
                 and util.clic_dans_rectangle(evenement, 1498, 18,
                                              1581, 101))):
            partie, reste_sur_jeu = menu_pause(
                joueur_position, joueur_direction, carte, labyrinthe, nb_laby,
                temps, temps_total_restant, score, temps_dispo, temps_restant,
                difficulte)

        # Si touche pressée, déplacement du joueur (si c'est la bonne touche)
        elif type_evenement == "Touche":
            joueur_position, joueur_direction = deplacements_joueur(
                fltk.touche(evenement), labyrinthe, joueur_position,
                joueur_direction)

        # Si plus de temps : Défaite du joueur
        elif temps_total_restant <= 0:
            partie = ecran_defaite(temps, score, nb_laby - 1)

        # Actualisation du temps
        temps, temps_precedent, temps_total_restant, temps_restant\
            = actualise_temps(temps, temps_precedent, temps_total_restant,
                              temps_restant, temps_dispo)

    return reste_sur_jeu
