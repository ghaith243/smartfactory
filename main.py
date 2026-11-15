
import threading
import multiprocessing
from queue import Queue

from clients.machine import (
    MachineFabrication,
    MachineAssemblage,
    MachineControle
)


# Fonction exécutée par le processus de surveillance énergétique
def surveiller_energie(file_energie):

    total_energie = 0

    consommation_machines = {
        "Fabrication": 0,
        "Assemblage": 0,
        "Contrôle": 0
    }

    while True:
        operation = file_energie.get()

        if operation is None:
            break

        nom, consommation = operation

        total_energie += consommation
        consommation_machines[nom] += consommation

        print(
            f"[Surveillance énergétique] "
            f"{nom} : {consommation} kWh",
            flush=True
        )

    print("\n--- Bilan énergétique ---")

    for nom, consommation in consommation_machines.items():
        print(f"{nom} : {consommation} kWh")

    print(f"Consommation totale : {total_energie} kWh")


def main():

    # 1. Création des mécanismes de synchronisation
    lock = threading.Lock()

    statistiques = {
        "total_operations": 0
    }

    semaphore = threading.Semaphore(2)

    # 2. Création des files d'attente
    file_pieces = Queue()
    file_produits = Queue()
    file_energie = multiprocessing.Queue()

    # 3. Création des machines
    machine_A = MachineFabrication("Machine A")
    machine_B = MachineAssemblage("Machine B")
    machine_C = MachineControle("Machine C")

    # 4. Création des threads de production
    thread_A = threading.Thread(
        target=machine_A.fabriquer,
        args=(file_pieces, lock, statistiques, file_energie),
        name="Thread-A"
    )

    thread_B = threading.Thread(
        target=machine_B.assembler,
        args=(file_pieces, file_produits, lock, statistiques, file_energie),
        name="Thread-B"
    )

    thread_C = threading.Thread(
        target=machine_C.controler_qualite,
        args=(file_produits, lock, statistiques, file_energie),
        name="Thread-C"
    )

    # 5. Création du processus énergétique
    processus_energie = multiprocessing.Process(
        target=surveiller_energie,
        args=(file_energie,)
    )

    # 6. Création des threads de maintenance
    maintenance_A = threading.Thread(
        target=machine_A.maintenance,
        args=(semaphore,)
    )

    maintenance_B = threading.Thread(
        target=machine_B.maintenance,
        args=(semaphore,)
    )

    maintenance_C = threading.Thread(
        target=machine_C.maintenance,
        args=(semaphore,)
    )

    # 7. Exécution des maintenances
    maintenance_A.start()
    maintenance_B.start()
    maintenance_C.start()

    maintenance_A.join()
    maintenance_B.join()
    maintenance_C.join()

    # 8. Démarrage du processus énergétique
    processus_energie.start()

    # 9. Démarrage des threads de production (une seule fois)
    thread_A.start()
    thread_B.start()
    thread_C.start()

    # 10. Attendre la fin de la production
    thread_A.join()
    thread_B.join()
    thread_C.join()

    # 11. Envoyer le signal de fin au processus énergétique
    file_energie.put(None)

    processus_energie.join()

    # 12. Affichage du bilan de production
    print("\n--- Bilan de production ---")
    print("Pièces fabriquées :", machine_A.compteur)
    print("Produits assemblés :", machine_B.compteur)
    print("Produits contrôlés :", machine_C.compteur)
    print("Total des opérations :", statistiques["total_operations"])

    file_energie.close()


if __name__ == "__main__":
    main()
