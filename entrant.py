from dataclasses import dataclass
from typing import List


@dataclass
class Entrant:
    name: str
    id: str
    opponentIds: List[str]
    points: int  # incl virtual point
    tourney_points: int  # excl virtual point
    received_bye: bool
    floated_down: bool
    floated_up: bool
    current_float_down: bool
    current_float_up: bool
    current_receive_bye: bool
    seed: int

    def float_down(self):
        print(f"[{self.name} FLOATED DOWN!]")
        self.floated_down = True
        self.current_float_down = True

    def float_up(self):
        print(f"[{self.name} FLOATED UP!]")
        self.floated_up = True
        self.current_float_up = True

    def give_bye(self):
        print(f"[{self.name} GETS BYE!]")
        self.received_bye = True
        self.current_receive_bye = True

    def __str__(self):
        bye = "received bye" if self.received_bye else ""
        floated_down = "floated_down" if self.floated_down else ""
        floated_up = "floated_up" if self.floated_up else ""
        return f"{self.points} {self.name} {self.seed}         {bye} {floated_down} {floated_up}"

    def to_new_pairing_data(self, old_entrants_pairing_data):
        matching_old_pairing_data = next((e for e in old_entrants_pairing_data if e['id'] == self.id), None)
        if matching_old_pairing_data is None:
            raise Exception(f"No matching pairing data found for entrant '{self.name}' (id: {self.id})")
        return {
            "name": self.name,
            "id": self.id,
            "start_seed": matching_old_pairing_data['start_seed'],
            "received_bye": self.received_bye,
            "floated_down": self.floated_down,
            "floated_up": self.floated_up,
            "virtual_point": matching_old_pairing_data['virtual_point']
        }


def to_entrant(entrant_data, entrants_pairing_data, use_start_seed: bool, use_virtual_point: bool):
    matching_pairing_data = next((e for e in entrants_pairing_data if e['id'] == entrant_data['id']), None)
    if matching_pairing_data is None:
        raise Exception(
            f"No matching pairing data found for entrant '{entrant_data['name']}' (id: {entrant_data['id']})")
    points = entrant_data['points']
    if use_virtual_point and matching_pairing_data['virtual_point']:
        points += 1
    return Entrant(entrant_data['name'], entrant_data['id'], [opponent['id'] for opponent in entrant_data['opponents']],
                   points, entrant_data['points'], matching_pairing_data['received_bye'],
                   matching_pairing_data['floated_down'],
                   matching_pairing_data['floated_up'],
                   False, False, False,
                   matching_pairing_data['start_seed'] if use_start_seed else entrant_data['current_seed'])
