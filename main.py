import json
import os

from entrant import toEntrant
from pair_calculator import PairCalculator

USE_START_SEED = True

if __name__ == '__main__':
    dataPath: str = "./data/entrants_data.json"
    pairingDataPath: str = "./data/entrants_pairing_data.json"

    if not os.path.exists(dataPath):
        raise FileNotFoundError(
            f"File {dataPath} does not exist, please create it first following entrantData.example.json")

    with open(dataPath) as file:
        entrantsData = json.load(file)
        file.close()

    if not os.path.exists(pairingDataPath):
        newEntrantsPairingData = [{
            "name": entrantData["name"],
            "id": entrantData["id"],
            "start_seed": entrantData["current_seed"],
            "received_bye": False,
            "floated_down": False,
            "floated_up": False
        } for entrantData in entrantsData]

        file = open(pairingDataPath, "a")
        file.write(json.dumps(newEntrantsPairingData, indent=2))
        file.close()
        print(f"Created {pairingDataPath}")

    with open(pairingDataPath) as file:
        entrantsPairingData = json.load(file)
        file.close()

    entrants = [toEntrant(entrantData, entrantsPairingData) for entrantData in entrantsData]
    pair_calculator = PairCalculator(entrants)
    pair_calculator.pair()
