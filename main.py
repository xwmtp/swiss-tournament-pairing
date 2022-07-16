import datetime
import json
import math
import os

from entrant import to_entrant
from pair_calculator import PairCalculator

# settings
USE_START_SEED = True
USE_VIRTUAL_POINT = True

if __name__ == '__main__':
    now_str = datetime.datetime.now().isoformat().replace(':', '_')
    data_path: str = "./data/entrants.json"
    pairing_data_path: str = "./data/entrants_pairing.json"
    output_path = "./data/output"
    new_pairing_data_path: str = output_path + rf"/entrants_pairing_{now_str}.json"
    new_pairing_results_path: str = output_path + rf"/entrants_pairing_results_{now_str}.json"

    if not os.path.exists(data_path):
        raise FileNotFoundError(
            f"File {data_path} does not exist, please create it first following entrant.example.json")

    with open(data_path) as file:
        entrants_data = json.load(file)
        file.close()

    entrants_data = sorted(entrants_data,
                           key=lambda entrantData: (-entrantData['current_seed'], entrantData['name'].lower()))
    halfLength = math.ceil(len(entrants_data) / 2)

    if not os.path.exists(pairing_data_path):
        initial_entrants_pairing_data = [{
            "name": entrantData["name"],
            "id": entrantData["id"],
            "start_seed": entrantData["current_seed"],
            "received_bye": False,
            "floated_down": False,
            "floated_up": False,
            "virtual_point": USE_VIRTUAL_POINT and i < halfLength
        } for (i, entrantData) in enumerate(entrants_data)]

        file = open(pairing_data_path, "a")
        file.write(json.dumps(initial_entrants_pairing_data, indent=2))
        file.close()
        print(f"Created {pairing_data_path}")

    with open(pairing_data_path) as file:
        entrants_pairing_data = json.load(file)
        file.close()

    # do pairing
    entrants = [to_entrant(entrant_data, entrants_pairing_data, USE_START_SEED, USE_VIRTUAL_POINT) for entrant_data in
                entrants_data]
    pair_calculator = PairCalculator(entrants)
    pairs = pair_calculator.pair()

    # save new entrant data
    new_entrants_pairing_data = [e.to_new_pairing_data(entrants_pairing_data) for e in entrants]
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    file = open(new_pairing_data_path, "a")
    file.write(json.dumps(new_entrants_pairing_data, indent=2))
    file.close()

    # save pairs
    file = open(new_pairing_results_path, "a")
    file.write(json.dumps(pairs, indent=2))
    file.close()
