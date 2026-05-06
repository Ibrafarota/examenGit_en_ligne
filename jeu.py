"""Jeu console: devinez le nombre."""

import random


def generer_nombre_secret(minimum=1, maximum=100):
    return random.randint(minimum, maximum)


def verifier_proposition(secret, proposition):
    if proposition < secret:
        return "plus grand"
    if proposition > secret:
        return "plus petit"
    return "gagne"


def jouer():
    print("Bienvenue dans le jeu: Devinez le nombre !")
    secret = generer_nombre_secret()
    essais = 0

    while True:
        valeur = input("Entrez un nombre entre 1 et 100: ").strip()
        if not valeur.isdigit():
            print("Entree invalide. Tapez un entier positif.")
            continue

        proposition = int(valeur)
        essais += 1
        resultat = verifier_proposition(secret, proposition)

        if resultat == "gagne":
            print(f"Bravo ! Vous avez trouve en {essais} essai(s).")
            break
        print(f"Indice: prenez {resultat}.")


if __name__ == "__main__":
    jouer()
