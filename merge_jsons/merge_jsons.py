import datetime
import json
import os

if __name__ == '__main__':
    now_str = datetime.datetime.now().isoformat().replace(':', '_')
    entrants_path: str = "./data/entrants_without_seed.json"
    lb_path: str = "./data/bingo_leaderboard.json"
    output_path = "./data/output"
    new_entrants_path = output_path + rf"/entrants_{now_str}.json"

    if not os.path.exists(entrants_path):
        raise FileNotFoundError(
            f"File {entrants_path} does not exist, please create it first following entrants_without_seed.example.json")

    if not os.path.exists(lb_path):
        raise FileNotFoundError(
            f"File {entrants_path} does not exist, please create it first following bingo_leaderboard.example.json (/api/leaderboard)")

    with open(entrants_path) as file:
        entrants_data = json.load(file)
        file.close()

    with open(lb_path) as file:
        lb_data = json.load(file)
        file.close()

    for entrant_data in entrants_data:
        matching_lb_entry = next((entry for entry in lb_data['entries'] if entry['playerId'] == entrant_data['id']),
                                 None)
        if (matching_lb_entry is None):
            raise Exception(f"Could not find bingo leaderboard data for entrant {entrant_data['name']}")
        entrant_data['current_seed'] = matching_lb_entry['leaderboardScore']

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    file = open(new_entrants_path, "a")
    print(new_entrants_path)
    file.write(json.dumps(entrants_data, indent=2))
    file.close()
