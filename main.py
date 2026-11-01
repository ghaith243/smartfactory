
from queue import Queue
import threading

from clients.machine import (
    MachineFabrication,
    MachineAssemblage,
    MachineControle
)
lock = threading.Lock()
total_operations = 0
statistiques = {
    "total_operations": 0
}
semaphore = threading.Semaphore(2)
# 1. Création des files d'attente
file_pieces = Queue()
file_produits = Queue()

# 2. Création des machines
machine_A = MachineFabrication("Machine A")
machine_B = MachineAssemblage("Machine B")
machine_C = MachineControle("Machine C")

# 3. Création des threads
thread_A = threading.Thread(
    target=machine_A.fabriquer,
    args=(file_pieces, lock, statistiques)
)

thread_B = threading.Thread(
    target=machine_B.assembler,
    args=(file_pieces, file_produits, lock, statistiques)
)

thread_C = threading.Thread(
    target=machine_C.controler_qualite,
    args=(file_produits,lock, statistiques)
)
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

# 1. Lancer les maintenances
maintenance_A.start()
maintenance_B.start()
maintenance_C.start()

# 2. Attendre la fin des maintenances
maintenance_A.join()
maintenance_B.join()
maintenance_C.join()

# 3. Lancer la production
thread_A.start()
thread_B.start()
thread_C.start()

# 4. Attendre la fin de la production
thread_A.join()
thread_B.join()
thread_C.join()

# 6. Bilan
print("\n--- Bilan de production ---")
print("Pièces fabriquées :", machine_A.compteur)
print("Produits assemblés :", machine_B.compteur)
print("Produits contrôlés :", machine_C.compteur)
print("Total des opérations :", statistiques["total_operations"])
