from dataclasses import dataclass
from typing import List


@dataclass
class Entrant:
    name: str
    id: str
    opponents: List[str]
    points: int
    received_bye: bool
    floated_down: bool
    floated_up: bool
    seed: int

    def float_down(self):
        print(f"[{self.name} FLOATED DOWN!]")
        self.floated_down = True

    def float_up(self):
        print(f"[{self.name} FLOATED UP!]")
        self.floated_up = True

    def give_bye(self):
        print(f"[{self.name} GETS BYE!]")
        self.received_bye = True

    def __str__(self):
        bye = "received bye" if self.received_bye else ""
        floated_down = "floated_down" if self.floated_down else ""
        floated_up = "floated_up" if self.floated_up else ""
        return f"{self.points} {self.name} {self.seed}         {bye} {floated_down} {floated_up}"


def to_entrant(entrant_data, entrants_pairing_data, use_start_seed: bool):
    matchingPairingData = next((e for e in entrants_pairing_data if e['id'] == entrant_data['id']), None)
    if matchingPairingData is None:
        raise Exception(
            f"No matching pairing data found for entrant '{entrant_data['name']}' (id: {entrant_data[id]})")
    return Entrant(entrant_data['name'], entrant_data['id'], entrant_data['opponents'],
                   entrant_data['points'], matchingPairingData['received_bye'],
                   matchingPairingData['floated_down'],
                   matchingPairingData['floated_up'],
                   matchingPairingData['start_seed'] if use_start_seed else entrant_data['current_seed'])
