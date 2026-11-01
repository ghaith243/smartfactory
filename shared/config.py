
class Machine:
    def __init__(self, nom):
        self.nom = nom
        self.active = True
        self.compteur = 0

    def produire(self):
        if self.active:
            self.compteur += 1
            print(f"{self.nom} : produit numéro {self.compteur}")

    def arreter(self):
        self.active = False
        print(f"{self.nom} est arrêtée.")

    def demarrer(self):
        self.active = True
        print(f"{self.nom} est démarrée.")
