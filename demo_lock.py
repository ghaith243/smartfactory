import threading
import time

compteur = 0
lock = threading.Lock()

def incrementer():
    global compteur

    for i in range(100):
        with lock:
            ancienne_valeur = compteur

            time.sleep(0.001)

            compteur = ancienne_valeur + 1


thread_A = threading.Thread(target=incrementer)
thread_B = threading.Thread(target=incrementer)

thread_A.start()
thread_B.start()

thread_A.join()
thread_B.join()

print("Valeur finale :", compteur)
print("Valeur attendue :", 200)