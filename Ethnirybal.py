###############################################################################
#                     Projet Fin Semestre 1: Labyrinthe                       #
#                           Project X - Ethnirybal                            #
#                                  v1.0.0                                     #
#                     Valentin Bernier - Alain Coserariu                      #
###############################################################################


import fltk
from Modules import utilitaire as util
from Modules import jeu
from Modules import sauvegarde
import time


def ecran_demarrage():
    """
    Affiche le nom Project X au lancement du jeu pendant 3 secondes.
    Permet de quitter sur cet écran
    Permet d'aller directement au menu en appuyant sur une touche quelconque

    :return: False si le jeu est fermé, True si on se rend sur le menu
    """
    # Affichage du logo "Project X"
    debut_ecran_demarrage = time.time()
    while True:

        fltk.efface_tout()
        fltk.image(0, 0, "Assets/Menu/projectx.png", ancrage="nw")
        fltk.mise_a_jour()

        # Detection de l'événement fltk
        evenement = fltk.donne_ev()
        type_evenement = fltk.type_ev(evenement)

        # Quitter
        if type_evenement == "Quitte":
            return False

        # Si le temps dépasse 3 secondes ou si un événement se produit (clic,
        # clavier), ferme l'écran de démarrage et envoie au menu
        elif (time.time() > debut_ecran_demarrage + 3
              or type_evenement is not None):
            return True


def affiche_menu():
    """
    Affiche les éléments du menu
    """
    fltk.efface_tout()

    partie_existante = sauvegarde.partie_existante()
    if partie_existante:
        fltk.image(0, 0, "Assets/Menu/menu_continuer.png", "nw")
    else:
        fltk.image(0, 0, "Assets/Menu/menu_nouveau.png", "nw")

    fltk.mise_a_jour()


def redirection_boutons_menu(evenement):
    """
    Détecte le clic sur l'un des boutons du menu et redirige l'utilisateur en
    conséquence

    :param evenement: Evenement détecté par fltk
    :return: True si retour au menu, False si fermeture du jeu
    """
    partie_existante = sauvegarde.partie_existante()

    # Continuer la partie (si sauvegarde existante)
    if util.clic_dans_rectangle(evenement, 153, 375, 626, 570)\
            and partie_existante:
        animation_lancement("continuer", False)
        return jeu.jeu(False)

    # Commencer une nouvelle partie
    elif util.clic_dans_rectangle(evenement, 1129, 493, 1481, 674):
        if partie_existante:
            animation_lancement("continuer", True)
        else:
            animation_lancement("nouveau", True)
        return jeu.jeu(True)

    # Quitter le jeu
    elif util.clic_dans_rectangle(evenement, 531, 728, 802, 850):
        return False

    return True


def animation_lancement(continuer, difficulte):
    """
    Affiche une animation lors du lancement d'une partie

    :param continuer: Chaine de caractères indiquant si une partie exite ou non
    :param difficulte: Booléen indiquant si un choix de difficulté
        doit être fait
    """
    for i in range(10):
        fltk.efface_tout()
        if difficulte:
            fltk.image(0, 900 - i * 100, "Assets/Menu/difficulte.png", "nw")
        else:
            fltk.image(0, 0, "Assets/Menu/ciel_grand.png", "nw")
        fltk.image(0, - i * 100, f"Assets/Menu/menu_{continuer}.png", "nw")
        fltk.mise_a_jour()
        time.sleep(0.1)
    time.sleep(0.5)


if __name__ == "__main__":

    # Créé la fenetre fltk
    fltk.cree_fenetre(util.TAILLE_FENETRE[0], util.TAILLE_FENETRE[1])

    # Affiche l'écran de démarrage
    menu = ecran_demarrage()

    # Boucle principale
    while menu:

        # Affiche les éléments du menu
        affiche_menu()

        # Détection d'événements fltk
        evenement = fltk.donne_ev()
        type_evenement = fltk.type_ev(evenement)

        # Quitter le jeu
        if type_evenement == "Quitte":
            menu = False

        elif type_evenement == "ClicGauche":
            # Evalue si le clic est sur un bouton et si oui, démarre le jeu
            menu = redirection_boutons_menu(evenement)
