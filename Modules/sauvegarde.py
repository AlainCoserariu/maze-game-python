###############################################################################
#                            Module de Project X                              #
#                                 Sauvegarde                                  #
#                     Valentin Bernier - Alain Coserariu                      #
###############################################################################


def partie_existante():
    """
    Défini si une partie à déjà été commencée et sauvegardée

    :return: Booléen; True si il y a une sauvegarde présente, False sinon
    """
    with open("Sauvegardes/joueur.txt", 'r') as joueur:
        partie_existante = int(joueur.readlines()[1])

    return bool(partie_existante)


def effacer_partie():
    """
    Supprime les données d'une partie
    """
    with open("Sauvegardes/joueur.txt", "w") as joueur:
        joueur.write("0 0;0 0;\n0\n0\n0;0;0;0;0;0")


def sauvegarde_partie(position, direction, carte, labyrinthe, nb_laby, temps,
                      temps_total_restant, score, temps_dispo, temps_restant,
                      difficulte):
    """
    Sauvegarde la partie

    :param position: Couple des coordonnées de la position du joueur
    :param direction: Direction du regard du joueur
    :param carte: Schéma de la carte à sauvegarder
    :param labyrinthe: Schéma du labyrinthe à sauvegarder
    :param nb_laby: Nombre de labyrinthe parcouru
    :param temps: Temps de jeu total
    :param temps_total_restant: Temps restant avant la defaite
    :param score: Score du joueur
    :param temps_dispo: Temps disponible pour finir le labyrinthe
    :param temps_restant: Temps restant pour finir le labyrinthe
    :param difficulte: Float représentant la difficulté
    """
    with open("Sauvegardes/joueur.txt", "w") as joueur:

        joueur.write(f"{position[0]} {position[1]};{direction[0]} "
                     f"{direction[1]};")
        joueur.write("\n1")
        joueur.write(f"\n{difficulte}")
        joueur.write(f"\n{nb_laby};{temps};{temps_total_restant};{score};"
                     f"{temps_dispo};{temps_restant}")

    sauvegarde_labyrinthe(carte, "carte")
    sauvegarde_labyrinthe(labyrinthe, "labyrinthe")


def chargement_partie():
    """
    Charge la partie

    :return: position, direction, carte, labyrinthe, nb_laby, temps,
        temps_total_restant, score, temps_dispo, temps_restant, difficulte
    """
    with open("Sauvegardes/joueur.txt", "r") as joueur:
        lignes = joueur.readlines()

        donnes_joueur = lignes[0].split(";")
        position = [int(i) for i in donnes_joueur[0].split(" ")]
        direction = [int(i) for i in donnes_joueur[1].split(" ")]

        difficulte = float(lignes[2])

        nb_laby, temps, temps_total_restant, score, temps_dispo, temps_restant\
            = [int(i) for i in lignes[3].split(";")]

    return position, direction, chargement_labyrinthe("carte"),\
        chargement_labyrinthe("labyrinthe"), nb_laby, temps,\
        temps_total_restant, score, temps_dispo, temps_restant, difficulte


def sauvegarde_labyrinthe(labyrinthe, fichier):
    """
    Sauvegarde le labyrinthe donné en paramètre

    :param labyrinthe: Liste du labyrinthe à sauvegarder
    :param fichier: Fichier où sauvegarder le labyrinthe
    """
    with open(f"Sauvegardes/{fichier}.txt", "w") as f_laby:
        for j in labyrinthe:
            for i in j:
                f_laby.write(i)
            f_laby.write("\n")


def chargement_labyrinthe(fichier):
    """
    Charge la disposition d'un labyrinthe depuis un fichier

    :param fichier: Fichier depuis lequel charger le labyrinthe
    :return: Liste des éléments du labyrinthe
    """
    labyrinthe = []
    with open(f"Sauvegardes/{fichier}.txt", "r") as f_laby:
        for ligne in f_laby:
            labyrinthe.append(list(ligne.strip()))
    return labyrinthe
