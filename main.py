import json
import os

from entrant import to_entrant
from pair_calculator import PairCalculator

USE_START_SEED = True

if __name__ == '__main__':
    data_path: str = "./data/entrants.json"
    pairing_data_path: str = "./data/entrants_pairing.json"

    if not os.path.exists(data_path):
        raise FileNotFoundError(
            f"File {data_path} does not exist, please create it first following entrantData.example.json")

    with open(data_path) as file:
        entrantsData = json.load(file)
        file.close()

    if not os.path.exists(pairing_data_path):
        new_entrants_pairing_data = [{
            "name": entrantData["name"],
            "id": entrantData["id"],
            "start_seed": entrantData["current_seed"],
            "received_bye": False,
            "floated_down": False,
            "floated_up": False
        } for entrantData in entrantsData]

        file = open(pairing_data_path, "a")
        file.write(json.dumps(new_entrants_pairing_data, indent=2))
        file.close()
        print(f"Created {pairing_data_path}")

    with open(pairing_data_path) as file:
        entrants_pairing_data = json.load(file)
        file.close()

    entrants = [to_entrant(entrant_data, entrants_pairing_data, USE_START_SEED) for entrant_data in entrantsData]
    pair_calculator = PairCalculator(entrants)
    pair_calculator.pair()
