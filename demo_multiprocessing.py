import multiprocessing


def surveiller_energie(file_energie):

    total_energie = 0

    while True:
        operation = file_energie.get()

        if operation is None:
            break

        nom, consommation = operation

        total_energie += consommation

        print(
            f"{nom} : {consommation} kWh"
        )

    print(f"Consommation totale : {total_energie} kWh")


if __name__ == "__main__":

    file_energie = multiprocessing.Queue()

    processus = multiprocessing.Process(
        target=surveiller_energie,
        args=(file_energie,)
    )

    processus.start()

    # Transmission des opérations
    file_energie.put(("Fabrication", 5))
    file_energie.put(("Assemblage", 3))
    file_energie.put(("Contrôle", 2))

    # Signal de fin
    file_energie.put(None)

    processus.join()

    print("Surveillance énergétique terminée.")