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


def toEntrant(entrantData, entrantsPairingData):
    matchingPairingData = next((e for e in entrantsPairingData if e['id'] == entrantData['id']), None)
    if matchingPairingData is None:
        raise Exception(
            f"No matching pairing data found for entrant '{entrantData['name']}' (id: {entrantData[id]})")
    return Entrant(entrantData['name'], entrantData['id'], entrantData['opponents'],
                   entrantData['points'], matchingPairingData['received_bye'],
                   matchingPairingData['floated_down'],
                   matchingPairingData['floated_up'],
                   matchingPairingData['start_seed'] if USE_START_SEED else entrantData['current_seed'])
