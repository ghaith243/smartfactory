import time
import threading
class Machine:
    def __init__(self, nom):
        self.nom = nom
        self.active = True
        self.compteur = 0

    def arreter(self):
        self.active = False
        print(f"{self.nom} est arrêtée.")

    def demarrer(self):
        self.active = True
        print(f"{self.nom} est démarrée.")
    def maintenance(self, semaphore):
       print(f"{self.nom} demande le poste de maintenance")

       with semaphore:
         print(f"{self.nom} commence la maintenance")

         time.sleep(3)

         print(f"{self.nom} termine la maintenance")


class MachineFabrication(Machine):
   def fabriquer(self, file_pieces, lock, statistiques):
     for i in range(5):
        if self.active:
            self.compteur += 1
            piece = f"Piece-{self.compteur}"

            print(
                f"{self.nom} [{threading.current_thread().name}] "
                f": fabrication de {piece}"
            )

            file_pieces.put(piece)

            with lock:
                statistiques["total_operations"] += 1

            time.sleep(2)


class MachineAssemblage(Machine):
    def assembler(self, file_pieces, file_produits, lock, statistiques):
        for i in range(5):
          if self.active:
            piece = file_pieces.get()

            self.compteur += 1
            produit = f"Produit-{self.compteur}"

            print(f"{self.nom} [{threading.current_thread().name}] : assemblage de {piece} -> {produit}")
            file_produits.put(produit)
            with lock:
             statistiques["total_operations"] += 1

            time.sleep(3)

class MachineControle(Machine):
   def controler_qualite(self, file_produits, lock, statistiques):
      for i in range(5):
        if self.active:
            produit = file_produits.get()

            self.compteur += 1

            print(f"{self.nom} [{threading.current_thread().name}] : contrôle qualité de {produit} terminé")
            with lock:
                statistiques["total_operations"] += 1

            time.sleep(1)