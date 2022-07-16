from typing import List, Tuple

from entrant import Entrant


class PairCalculator:

    def __init__(self, entrants: List[Entrant]):
        self.entrants: List[Entrant] = [e for e in entrants]
        self.original_entrants: List[Entrant] = [e for e in entrants]
        self.pairs: List[Tuple[Entrant, Entrant]] = []

    def current_downfloaters(self):
        return [e for e in self.original_entrants if e.floated_down]

    def current_upfloaters(self):
        return [e for e in self.original_entrants if e.floated_up]

    def current_byes(self):
        return [e for e in self.original_entrants if e.received_bye]

    def pair(self):
        self.print_entrants(self.entrants)
        current_points = sorted(list(set([e.points for e in self.entrants])), reverse=True)
        self.award_bye()
        unpaired = []
        for points in current_points:
            print(f"\nGroup {points}")
            to_pair = [e for e in self.entrants if e.points == points] + unpaired
            unpaired = []
            if len(to_pair) % 2 != 0:
                downfloater, to_pair = self.get_downfloater(to_pair)
                unpaired.append(downfloater)
            self.fold_pair(to_pair)

        self.verify_results()
        self.print_results()
        return self.get_pairs_json()

    def award_bye(self):
        if len(self.entrants) % 2 == 0:
            return
        min_points = min([e.points for e in self.entrants])
        candidates = sorted([e for e in self.entrants if e.points == min_points], key=lambda e: -e.seed)
        for candidate in candidates:
            if not candidate.floated_down and not candidate.received_bye:
                self.award_bye_to_entrant(candidate)
                return
            print(f"(Skipping {candidate.name} for bye, already floated down or received bye)")
        for candidate in candidates:
            if not candidate.received_bye:
                self.award_bye_to_entrant(candidate)
                return
            print(f"(Skipping {candidate.name} for bye, already received bye)")
        raise Exception("Can't find candidate for bye!")

    def award_bye_to_entrant(self, entrant):
        entrant.give_bye()
        self.pairs.append((entrant, entrant))
        self.entrants.remove(entrant)

    def get_downfloater(self, to_pair: List[Entrant]):
        to_pair = sorted(to_pair, key=lambda e: -e.seed)
        for entrant in to_pair:
            if not entrant.floated_down and not entrant.received_bye:
                entrant.float_down()
                to_pair.remove(entrant)
                return entrant, to_pair
            print(f"(Skipping {entrant.name} for floatdown, already floated down or received bye)")
        for entrant in to_pair:
            if not entrant.floated_down:
                entrant.float_down()
                to_pair.remove(entrant)
                return entrant, to_pair
            print(f"(Skipping {entrant.name} for floatdown, already floated down)")
        raise Exception("Can't find any downfloater!")

    def fold_pair(self, to_pair: List[Entrant]):
        to_pair = sorted(to_pair, key=lambda e: -e.seed)
        while (len(to_pair) > 1):
            e1 = to_pair[0]
            e2 = self.fold_pair_opponent(e1, to_pair)
            self.pairs.append((e1, e2))
            print(f"{e1.name} vs {e2.name}")
        return to_pair

    def fold_pair_opponent(self, e1: Entrant, to_pair: List[Entrant]):
        for i in range(len(to_pair)):
            e2 = to_pair[-(i + 1)]
            if e1.id is not e2.id and self.pairable(e1, e2):
                to_pair.remove(e1)
                to_pair.remove(e2)
                return e2
        raise Exception(f"Could not find opponent for {e1.name}!")

    def pairable(self, entrant: Entrant, opponent: Entrant):
        if entrant.id in opponent.opponents or opponent.id in entrant.opponents:
            print(f"(Skipping match up {entrant.name} vs {opponent.name}, they already played each other)")
            return False
        if entrant not in self.current_downfloaters():
            return True
        if opponent.floated_up:
            print(f"(Skipping {opponent.name} for float up, already floated up)")
            return False
        else:
            opponent.float_up()
            return True

    def print_entrants(self, entrants: List[Entrant]):
        for entrant in sorted(entrants, key=lambda e: (-e.points, -e.seed)):
            print(entrant)

    def print_results(self):
        print(f"\nRESULTS:")
        byes = []
        for e1, e2 in self.pairs:
            if e1.id == e2.id:
                byes.append(e1)
            else:
                print(f"{e1.name} ({e1.points} {e1.seed}) vs {e2.name} ({e2.points} {e2.seed})")
        for e in byes:
            print(f"{e.name} ({e.points} {e.seed}) (bye)")
        print(f"\nNEW DOWNFLOATERS: {[e.name for e in self.current_downfloaters()]}")
        print(f"NEW UPFLOATERS: {[e.name for e in self.current_upfloaters()]}")
        print(f"NEW BYES: {[e.name for e in self.current_byes()]}")

    def get_pairs_json(self):
        json = []
        for pair in self.pairs:
            new_pair = []
            for entrant in pair:
                if not any(entrant.id == e['id'] for e in new_pair):
                    new_pair.append(
                        {'id': entrant.id, 'points': entrant.points, 'tourney_points': entrant.tourney_points,
                         'seed': entrant.seed})
            json.append(new_pair)
        return json

    def verify_results(self):
        print('\nVerifying results...')
        expected_entrants_length = len(self.original_entrants) - len(self.current_downfloaters()) - len(
            self.current_upfloaters()) - len(self.current_byes())

        if (len(self.entrants) is not expected_entrants_length):
            raise Exception(f"Entrants has length {len(self.entrants)} but it should be {expected_entrants_length}")

        for e in self.original_entrants:
            occurrences = 0
            for e1, e2 in self.pairs:
                if e.id == e1.id:
                    occurrences += 1
                if e.id == e2.id:
                    occurrences += 1
            if e in self.current_byes():
                if occurrences != 2:
                    raise Exception(f"{e.name} with bye) appears {occurrences} times in paired results!")
            elif occurrences != 1:
                raise Exception(f"{e.name} appears {occurrences} times in paired results!")
        print("Results verified, every entrant appears once (or 2 times if bye)")
