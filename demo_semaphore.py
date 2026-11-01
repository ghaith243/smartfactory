import threading
import time

semaphore = threading.Semaphore(2)

def maintenance(nom):
    print(f"{nom} demande le poste de maintenance")

    with semaphore:
        print(f"{nom} entre en maintenance")

        time.sleep(3)

        print(f"{nom} termine la maintenance")


thread_A = threading.Thread(
    target=maintenance,
    args=("Machine A",)
)

thread_B = threading.Thread(
    target=maintenance,
    args=("Machine B",)
)

thread_C = threading.Thread(
    target=maintenance,
    args=("Machine C",)
)

thread_A.start()
thread_B.start()
thread_C.start()

thread_A.join()
thread_B.join()
thread_C.join()