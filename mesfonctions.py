"""Collection de fonctions utilitaires."""

from collections import Counter
from math import gcd


def addition(a, b):
    return a + b


def soustraction(a, b):
    return a - b


def multiplication(a, b):
    return a * b


def division(a, b):
    if b == 0:
        raise ValueError("Division par zero interdite")
    return a / b


def factorielle(n):
    if n < 0:
        raise ValueError("n doit etre positif")
    resultat = 1
    for i in range(2, n + 1):
        resultat *= i
    return resultat


def est_premier(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def inverser_chaine(texte):
    return texte[::-1]


def compter_voyelles(texte):
    voyelles = "aeiouyAEIOUY"
    return sum(1 for caractere in texte if caractere in voyelles)


def pgcd(a, b):
    return gcd(a, b)


def mode_liste(valeurs):
    if not valeurs:
        raise ValueError("La liste ne peut pas etre vide")
    compte = Counter(valeurs)
    max_occurrence = max(compte.values())
    modes = [valeur for valeur, occ in compte.items() if occ == max_occurrence]
    return min(modes)
