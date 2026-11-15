
import time
import threading

from shared.config import (
    DUREE_ASSEMBLAGE,
    DUREE_CONTROLE,
    DUREE_FABRICATION,
    DUREE_MAINTENANCE,
    ENERGIE_ASSEMBLAGE,
    ENERGIE_CONTROLE,
    ENERGIE_FABRICATION,
    NOMBRE_PIECES,
    SEUIL_PANNE,
    SIMULER_PANNE
)


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

            time.sleep(DUREE_MAINTENANCE)

            print(f"{self.nom} termine la maintenance")


class MachineFabrication(Machine):

    def fabriquer(self, file_pieces, lock, statistiques, file_energie):

        for i in range(NOMBRE_PIECES):

            if self.active:
                self.compteur += 1
                piece = f"Piece-{self.compteur}"

                print(
                    f"{self.nom} [{threading.current_thread().name}] "
                    f": fabrication de {piece}"
                )

                file_pieces.put(piece)

                # Envoyer la consommation énergétique
                file_energie.put(("Fabrication", ENERGIE_FABRICATION))

                with lock:
                    statistiques["total_operations"] += 1

                time.sleep(DUREE_FABRICATION)

                if SIMULER_PANNE and self.compteur == SEUIL_PANNE:
                    print("PANNE détectée sur Machine A !")
                    self.arreter()
                    break

        file_pieces.put(None)
        print(f"{self.nom} : fin de fabrication.")


class MachineAssemblage(Machine):

    def assembler(self, file_pieces, file_produits, lock, statistiques, file_energie):

        while True:
            piece = file_pieces.get()

            if piece is None:
                print(f"{self.nom} : fin des assemblages.")
                file_produits.put(None)
                break

            self.compteur += 1
            produit = f"Produit-{self.compteur}"

            print(
                f"{self.nom} [{threading.current_thread().name}] "
                f": assemblage de {piece} -> {produit}"
            )

            file_produits.put(produit)

            # Envoyer la consommation énergétique
            file_energie.put(("Assemblage", ENERGIE_ASSEMBLAGE))

            with lock:
                statistiques["total_operations"] += 1

            time.sleep(DUREE_ASSEMBLAGE)


class MachineControle(Machine):

    def controler_qualite(self, file_produits, lock, statistiques, file_energie):

        while True:
            produit = file_produits.get()

            if produit is None:
                print(f"{self.nom} : fin des contrôles.")
                break

            self.compteur += 1

            print(
                f"{self.nom} [{threading.current_thread().name}] "
                f": contrôle qualité de {produit} terminé"
            )

            # Envoyer la consommation énergétique
            file_energie.put(("Contrôle", ENERGIE_CONTROLE))

            with lock:
                statistiques["total_operations"] += 1

            time.sleep(DUREE_CONTROLE)
