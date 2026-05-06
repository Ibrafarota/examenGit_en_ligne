"""Ludo personnalise avec interface graphique tkinter."""

import random
import tkinter as tk
from tkinter import messagebox

TAILLE_CASE = 46
MARGE = 30
RAYON_PION = 13

COULEURS_JOUEURS = ["red", "green", "blue", "gold"]
NOMS_JOUEURS = {
    "red": "Rouge",
    "green": "Vert",
    "blue": "Bleu",
    "gold": "Or",
}
EMOJIS = {
    "red": "🔥",
    "green": "🌿",
    "blue": "🌊",
    "gold": "⭐",
}


def creer_parcours():
    """Cree un parcours carre de 24 cases."""
    parcours = []
    for x in range(6):
        parcours.append((x, 0))
    for y in range(1, 6):
        parcours.append((5, y))
    for x in range(4, -1, -1):
        parcours.append((x, 5))
    for y in range(4, 0, -1):
        parcours.append((0, y))
    return parcours


PARCOURS = creer_parcours()
TAILLE_PARCOURS = len(PARCOURS)
INDEX_DEPART = {"red": 0, "green": 6, "blue": 12, "gold": 18}


class JeuLudo:
    def __init__(self, racine):
        self.racine = racine
        self.racine.title("Ludo Personnalise - Ibra Edition")
        self.racine.configure(bg="#1f2937")
        self.racine.resizable(False, False)

        self.joueur_courant = 0
        self.positions = {couleur: -1 for couleur in COULEURS_JOUEURS}
        self.nb_victoires = {couleur: 0 for couleur in COULEURS_JOUEURS}
        self.derniere_valeur_de = None
        self.jeu_termine = False

        largeur = MARGE * 2 + 6 * TAILLE_CASE
        hauteur = MARGE * 2 + 6 * TAILLE_CASE
        self.canvas = tk.Canvas(
            self.racine,
            width=largeur,
            height=hauteur,
            bg="#111827",
            highlightthickness=0,
        )
        self.canvas.grid(row=0, column=0, padx=12, pady=12)

        panneau = tk.Frame(self.racine, bg="#1f2937")
        panneau.grid(row=0, column=1, sticky="ns", padx=(0, 14), pady=12)

        self.lbl_titre = tk.Label(
            panneau,
            text="Ludo Personnalise",
            font=("Segoe UI", 16, "bold"),
            bg="#1f2937",
            fg="#f9fafb",
        )
        self.lbl_titre.pack(pady=(5, 12))

        self.lbl_tour = tk.Label(
            panneau,
            text="Tour: -",
            font=("Segoe UI", 12, "bold"),
            bg="#1f2937",
            fg="#d1d5db",
            justify="left",
        )
        self.lbl_tour.pack(anchor="w")

        self.lbl_de = tk.Label(
            panneau,
            text="De: -",
            font=("Consolas", 13, "bold"),
            bg="#1f2937",
            fg="#93c5fd",
        )
        self.lbl_de.pack(anchor="w", pady=(7, 14))

        self.btn_lancer = tk.Button(
            panneau,
            text="Lancer le de",
            command=self.lancer_de,
            bg="#2563eb",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            activebackground="#1d4ed8",
            activeforeground="white",
            width=18,
        )
        self.btn_lancer.pack(pady=5)

        self.btn_nouvelle_partie = tk.Button(
            panneau,
            text="Nouvelle partie",
            command=self.reinitialiser,
            bg="#059669",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            activebackground="#047857",
            activeforeground="white",
            width=18,
        )
        self.btn_nouvelle_partie.pack(pady=5)

        self.lbl_regles = tk.Label(
            panneau,
            text=(
                "Regles rapides:\n"
                "- Faire 6 pour sortir.\n"
                "- Capturer un adversaire le renvoie base.\n"
                "- Le premier qui boucle gagne."
            ),
            justify="left",
            bg="#1f2937",
            fg="#e5e7eb",
            font=("Segoe UI", 10),
        )
        self.lbl_regles.pack(anchor="w", pady=(12, 10))

        self.lbl_score = tk.Label(
            panneau,
            text="",
            justify="left",
            bg="#1f2937",
            fg="#f3f4f6",
            font=("Consolas", 10),
        )
        self.lbl_score.pack(anchor="w", pady=(0, 8))

        self.dessiner_plateau()
        self.mettre_a_jour_affichage()

    def case_vers_pixel(self, coord):
        x, y = coord
        px = MARGE + x * TAILLE_CASE + TAILLE_CASE // 2
        py = MARGE + y * TAILLE_CASE + TAILLE_CASE // 2
        return px, py

    def dessiner_plateau(self):
        self.canvas.delete("all")
        for index, coord in enumerate(PARCOURS):
            x, y = coord
            x1 = MARGE + x * TAILLE_CASE
            y1 = MARGE + y * TAILLE_CASE
            x2 = x1 + TAILLE_CASE
            y2 = y1 + TAILLE_CASE
            couleur = "#374151" if index % 2 == 0 else "#4b5563"
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=couleur, outline="#9ca3af")

        for couleur, depart in INDEX_DEPART.items():
            px, py = self.case_vers_pixel(PARCOURS[depart])
            self.canvas.create_oval(
                px - 8, py - 8, px + 8, py + 8, fill=couleur, outline="white", width=2
            )

        self.canvas.create_text(
            MARGE + 3 * TAILLE_CASE,
            MARGE + 3 * TAILLE_CASE,
            text="LUDO\nIBRA",
            fill="#f9fafb",
            font=("Segoe UI", 14, "bold"),
            justify="center",
        )

        for i, couleur in enumerate(COULEURS_JOUEURS):
            pos = self.positions[couleur]
            if pos == -1:
                bx = MARGE + (1 + (i % 2) * 4) * TAILLE_CASE
                by = MARGE + (1 + (i // 2) * 4) * TAILLE_CASE
                px = bx
                py = by
            else:
                px, py = self.case_vers_pixel(PARCOURS[pos])

            self.canvas.create_oval(
                px - RAYON_PION,
                py - RAYON_PION,
                px + RAYON_PION,
                py + RAYON_PION,
                fill=couleur,
                outline="black",
                width=2,
            )

    def lancer_de(self):
        if self.jeu_termine:
            return

        couleur = COULEURS_JOUEURS[self.joueur_courant]
        nom_joueur = NOMS_JOUEURS[couleur]
        self.derniere_valeur_de = random.randint(1, 6)
        self.lbl_de.config(text=f"De: {self.derniere_valeur_de}")

        position = self.positions[couleur]
        if position == -1:
            if self.derniere_valeur_de == 6:
                self.positions[couleur] = INDEX_DEPART[couleur]
                self.verifier_capture(couleur)
            else:
                messagebox.showinfo("Tour", f"{nom_joueur}: il faut faire 6 pour sortir.")
                self.passer_au_joueur_suivant()
        else:
            nouvelle_pos = (position + self.derniere_valeur_de) % TAILLE_PARCOURS
            self.positions[couleur] = nouvelle_pos
            self.verifier_capture(couleur)

            if nouvelle_pos == INDEX_DEPART[couleur]:
                self.nb_victoires[couleur] += 1
                self.jeu_termine = True
                self.dessiner_plateau()
                self.mettre_a_jour_affichage()
                messagebox.showinfo(
                    "Victoire",
                    f"{EMOJIS[couleur]} {nom_joueur} gagne cette partie !",
                )
                return

            if self.derniere_valeur_de != 6:
                self.passer_au_joueur_suivant()

        self.dessiner_plateau()
        self.mettre_a_jour_affichage()

    def verifier_capture(self, couleur_actuelle):
        position_actuelle = self.positions[couleur_actuelle]
        for couleur in COULEURS_JOUEURS:
            if couleur == couleur_actuelle:
                continue
            if self.positions[couleur] == position_actuelle:
                self.positions[couleur] = -1
                messagebox.showinfo(
                    "Capture",
                    f"{EMOJIS[couleur_actuelle]} {NOMS_JOUEURS[couleur_actuelle]} "
                    f"capture {NOMS_JOUEURS[couleur]} !",
                )

    def passer_au_joueur_suivant(self):
        self.joueur_courant = (self.joueur_courant + 1) % len(COULEURS_JOUEURS)

    def reinitialiser(self):
        self.positions = {couleur: -1 for couleur in COULEURS_JOUEURS}
        self.joueur_courant = 0
        self.derniere_valeur_de = None
        self.jeu_termine = False
        self.dessiner_plateau()
        self.mettre_a_jour_affichage()

    def mettre_a_jour_affichage(self):
        couleur = COULEURS_JOUEURS[self.joueur_courant]
        self.lbl_tour.config(text=f"Tour: {EMOJIS[couleur]} {NOMS_JOUEURS[couleur]}")

        score = []
        for c in COULEURS_JOUEURS:
            score.append(f"{EMOJIS[c]} {NOMS_JOUEURS[c]}: {self.nb_victoires[c]}")
        self.lbl_score.config(text="Score\n" + "\n".join(score))


def lancer_jeu():
    racine = tk.Tk()
    JeuLudo(racine)
    racine.mainloop()


if __name__ == "__main__":
    lancer_jeu()
