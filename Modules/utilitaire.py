###############################################################################
#                            Module de Project X                              #
#                                 Utilitaire                                  #
#                     Valentin Bernier - Alain Coserariu                      #
###############################################################################


import fltk


# Initialisation de la taille de l'écran et de la fenetre de jeu
TAILLE_FENETRE = (1600, 900)
COOR_FEN_JEU = ((20, 160), (1300, 880))


def clic_dans_rectangle(evenement, ax, ay, bx, by):
    """
    Détecte si un clic est effectué dans un rectangle

    :param evenement: Evenement détecté par fltk
    :param ax: Abscisse du coin supérieur gauche
    :param ay: Ordonnée du coin supérieur gauche
    :param bx: Abscisse du coin inférieur droit
    :param by: Ordonnée du coin inférieur droit
    :return: True si clic dans le rectangle, False sinon
    """
    if ax <= fltk.abscisse(evenement) <= bx and \
            ay <= fltk.ordonnee(evenement) <= by:
        return True
    return False
