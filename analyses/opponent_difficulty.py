import json

# pair output files to analyze
ENTRANTS_PAIRING_RESULT_PATHS = [
    '../data/output/entrants_pairing_results_1.json'
]

# for converting the ids to actual names
ENTRANTS_JSON_PATH = '../data/entrants.json'


def analyze_pair_json(pairs_json, dct):
    for pair in pairs_json:
        p1 = pair[0]
        p2 = pair[1]
        if p1["id"] == p2["id"]:
            continue
        diff = p1["seed"] - p2["seed"]
        if p1["id"] not in dct.keys():
            dct[p1["id"]] = 0
        if p2["id"] not in dct.keys():
            dct[p2["id"]] = 0
        dct[p1["id"]] -= diff
        dct[p2["id"]] += diff
    return dct


def convert_ids_to_names(id_dct):
    with open(ENTRANTS_JSON_PATH) as file:
        entrants_json = json.load(file)
        file.close()

    names_dct = {}
    for player_id in id_dct:
        for entrant in entrants_json:
            if player_id == entrant["id"]:
                names_dct[entrant["name"]] = id_dct[player_id]
    return names_dct


if __name__ == '__main__':
    pair_jsons = []
    for path in ENTRANTS_PAIRING_RESULT_PATHS:
        with open(path) as file:
            pair_jsons.append(json.load(file))
            file.close()

    seed_diff_dict = {}
    for pair_json in pair_jsons:
        seed_diff_dict = analyze_pair_json(pair_json, seed_diff_dict)
    seed_diff_names_dict = convert_ids_to_names(seed_diff_dict)

    # take average
    for player in seed_diff_names_dict:
        seed_diff_names_dict[player] /= len(ENTRANTS_PAIRING_RESULT_PATHS)

    # print (use -x[1] to reverse sort)
    for key, value in sorted(seed_diff_names_dict.items(), key=lambda x: x[1]):
        print(f"{key}: {value}")
