"""
Author: Rayla Kurosaki

GitHub: https://github.com/rkp1503
"""

import copy
import itertools
import json
import math
import sys

import misc.table_functions as tf

MAX_ROLL: int = 6

COLUMNS: list[str] = ["Single", "Double", "Triple", "Quad"]

RVS: list[float] = [0.7, 0.8, 0.9, 1.0]


class ArtifactPiece:
    def __init__(self, level: int, ssv_dict: dict[str, float | int]):
        self.level: int = level
        self.ssv_dict: dict[str, float | int] = ssv_dict
        self.rv_dict: dict[str, float] = {}
        self.ssr_dict: dict[str, int] = {}
        pass

    def get_level(self) -> int:
        return self.level

    def get_sub_stats(self) -> list[str]:
        return list(self.ssv_dict.keys())

    def get_sub_stat_values(self) -> list[float | int]:
        return list(self.ssv_dict.values())

    def get_sub_stat_values_dict(self) -> dict:
        return self.ssv_dict

    def get_roll_values(self) -> list[float]:
        return list(self.rv_dict.values())

    def get_roll_values_dict(self) -> dict:
        return self.rv_dict

    def get_sub_stat_rolls(self) -> list[int]:
        return list(self.ssr_dict.values())

    def get_sub_stat_rolls_dict(self) -> dict:
        return self.ssr_dict

    def convert_ssv_to_rv(self, json_data: dict) -> None:
        for sub_stat in self.ssv_dict:
            rv: float = self.ssv_dict[sub_stat] / float(
                json_data[sub_stat]["X"])
            rv = float(f"{rv:.1f}")
            self.rv_dict[sub_stat] = rv
            self.ssr_dict[sub_stat] = compute_num_rolls(rv)
            pass
        return None

    def get_valid_num_rolls(self, possible_num_rolls: list) -> list:
        valid_num_rolls: list = []
        nr_1, nr_2, nr_3, nr_4 = list(self.get_sub_stat_rolls())
        for e_1 in nr_1:
            for e_2 in nr_2:
                for e_3 in nr_3:
                    for e_4 in nr_4:
                        e_s: list = [e_1, e_2, e_3, e_4]
                        if sum(e_s) in possible_num_rolls:
                            valid_num_rolls.append(e_s)
                            pass
                        pass
                    pass
                pass
            pass
        return valid_num_rolls

    def num_rolls_safety_check(self, possible_num_rolls: list,
                               valid_num_rolls: list) -> None:
        if len(valid_num_rolls) != 1:
            temp: list = []
            for valid_num_roll in valid_num_rolls:
                if sum(valid_num_roll) in possible_num_rolls:
                    temp.append(valid_num_roll)
                pass
            if not temp:
                print(f"Number of rolls conflict.\n"
                      f"Possible: {possible_num_rolls}\n"
                      f"Valid: {valid_num_rolls}")
                sys.exit(0)
                pass
            valid_num_rolls = temp
            pass
        for (i, sub_stat) in enumerate(self.get_sub_stats()):
            num_rolls: int = valid_num_rolls[0][i]
            self.get_sub_stat_rolls_dict()[sub_stat] = num_rolls
            pass
        return None

    def get_totals(self, seq) -> tuple[float, int]:
        total_rv: float = 0.0
        total_num_rolls: int = 0
        for sub_stat in list(seq):
            total_rv = total_rv + self.get_roll_values_dict()[sub_stat]
            total_rv = float(f"{total_rv:.1f}")
            total_num_rolls += self.get_sub_stat_rolls_dict()[sub_stat]
            pass
        return total_rv, total_num_rolls

    def get_results(self, i: int, ratings: dict, seq) -> tuple:
        total_rv, total_num_rolls = self.get_totals(seq)
        sub_stat_str: str = "/".join(list(seq))
        rating: str = ""
        if i + 1 < 4:
            rating = rate_sub_stat(total_rv, ratings)
            pass
        p: float = 100 * total_rv / (MAX_ROLL + i)
        return sub_stat_str, rating, float(f"{p:.2f}")

    def evaluate(self) -> None:
        possible_num_rolls: list = [
            3 + math.floor(self.level / 4), 4 + math.floor(self.level / 4)
        ]
        valid_num_rolls: list = self.get_valid_num_rolls(possible_num_rolls)
        self.num_rolls_safety_check(possible_num_rolls, valid_num_rolls)
        data_to_print: list = [
            ["" for _ in range(len(COLUMNS))] for _ in range(6)
        ]
        for i in range(len(COLUMNS)):
            results: list = []
            ratings: dict = roll_ratings(i + 1)
            for seq in itertools.combinations(self.get_sub_stats(), i + 1):
                result = self.get_results(i, ratings, seq)
                results.append(result)
                pass
            tableize_results(data_to_print, i, results)
            pass
        data_to_print.insert(0, [f"{col} Sub Stat" for col in COLUMNS])
        tf.print_data_as_table(data_to_print)
        return None

    def generate_future_rolls(self) -> list[list[float]]:
        future_rolls: list = [[self.get_roll_values()]]
        for i in range(5 - math.floor(self.get_level() / 4)):
            future_rolls_i: list = []
            for current_roll in future_rolls[-1]:
                create_next_roll(current_roll, future_rolls_i)
                pass
            future_rolls.append(future_rolls_i)
            pass
        future_rolls.pop(0)
        return [roll for roll_i in future_rolls for roll in roll_i]

    def compute_sub_stat_probabilities(self, future_rolls: list[list[float]],
                                       ratings: dict, seq) -> dict[str, str]:
        sub_stat_index: list = [
            self.get_sub_stats().index(e) for e in list(seq)
        ]
        grade_counters: dict = get_rating_counters(future_rolls,
                                                   sub_stat_index,
                                                   ratings)
        return get_rating_p(grade_counters)

    def compute_potential(self) -> None:
        future_rolls: list[list[float]] = self.generate_future_rolls()
        for (i, col) in enumerate(COLUMNS[:-1]):
            print(f"{col} Sub Stat Probabilities:")
            ratings: dict = roll_ratings(i + 1)
            seqs = itertools.combinations(self.get_sub_stats(), i + 1)
            for seq in seqs:
                sub_stat: str = "/".join(list(seq))
                grade_p: dict = self.compute_sub_stat_probabilities(
                    future_rolls, ratings, seq)
                print(f"\t{sub_stat}: {grade_p}")
                pass
            pass
        return None

    def analyze(self, json_data: dict) -> None:
        self.convert_ssv_to_rv(json_data)
        if self.level == 20:
            self.evaluate()
            pass
        else:
            self.compute_potential()
            pass
        pass

    pass


def get_rating_counters(future_rolls: list[list[float]],
                        sub_stat_index: list, ratings: dict) -> dict:
    rating_counters: dict[str, int] = {
        "S+": 0, "S": 0, "A": 0, "B": 0, "C": 0, "D": 0, "F": 0
    }
    for roll in future_rolls:
        rv_s: list = [roll[index] for index in sub_stat_index]
        total_rv: float = float(f"{sum(rv_s):.1f}")
        rating: str = rate_sub_stat(total_rv, ratings)
        rating_counters[rating] += 1
        pass
    return rating_counters


def compute_num_rolls(rv: float) -> int | list:
    num_rolls: list = []
    for i in range(1, MAX_ROLL + 1):
        for seq in itertools.combinations(sorted(RVS * i), i):
            if float(f"{sum(seq):.1f}") == rv:
                if len(seq) not in num_rolls:
                    num_rolls.append(len(seq))
                    pass
                pass
            pass
        pass
    return num_rolls


def roll_ratings(num_sub_stats: int) -> dict:
    ratings: dict[str, list[float]] = {
        "S+": [], "S": [], "A": [], "B": [], "C": [], "D": [], "F": []
    }
    if num_sub_stats == 1:
        ratings["S+"] = [6.0, 6.0]  # 1.67%
        ratings["S"] = [4.9, 5.9]  # 16.67%
        ratings["A"] = [3.9, 4.8]  # 15.00%
        ratings["B"] = [3.0, 3.8]  # 13.33%
        ratings["C"] = [2.1, 2.9]  # 13.33%
        ratings["D"] = [1.4, 2.0]  # 10.00%
        ratings["F"] = [0.0, 1.0]  # 16.67% (23.33%)
        pass
    elif num_sub_stats == 2:
        ratings["S+"] = [7.0, 7.0]  # 1.43%
        ratings["S"] = [5.8, 6.9]  # 15.71%
        ratings["A"] = [4.7, 5.7]  # 14.29%
        ratings["B"] = [3.8, 4.6]  # 11.43%
        ratings["C"] = [2.9, 3.7]  # 11.43%
        ratings["D"] = [2.1, 2.8]  # 10.00%
        ratings["F"] = [0.0, 2.0]  # 28.57%
        pass
    elif num_sub_stats == 3:
        ratings["S+"] = [8.0, 8.0]  # 1.25%
        ratings["S"] = [6.7, 7.9]  # 15.00%
        ratings["A"] = [5.6, 6.6]  # 12.50%
        ratings["B"] = [4.6, 5.5]  # 11.25%
        ratings["C"] = [3.7, 4.5]  # 10.00%
        ratings["D"] = [2.9, 3.6]  # 8.75%
        ratings["F"] = [0.0, 2.8]  # 35.00%
        pass
    else:
        pass
    return ratings


def rate_sub_stat(total_rv: float, ratings: dict) -> str:
    for (rating, (rv_min, rv_max)) in ratings.items():
        if rv_min <= total_rv <= rv_max:
            return rating
        pass
    pass


def tableize_results(data_to_print: list, i: int, results: list) -> None:
    results = sorted(results, key=lambda x: x[2], reverse=True)
    for (j, result) in enumerate(results):
        sub_stat, rating, p = result
        if i + 1 < 4:
            data_to_print[j][i] = f"{sub_stat}: {rating} ({p}%)"
            pass
        else:
            data_to_print[j][i] = f"{sub_stat}: ({p}%)"
            pass
        pass
    return None


def create_next_roll(current_roll: list[float], future_rolls_i: list) -> None:
    for j in range(len(current_roll)):
        for rv in RVS:
            next_roll = copy.deepcopy(current_roll)
            next_roll[j] = float(f"{next_roll[j] + rv:.1f}")
            future_rolls_i.append(next_roll)
            pass
        pass
    return None


def get_rating_p(grade_counters: dict) -> dict:
    ratings_p: dict = {}
    total_count: int = sum(list(grade_counters.values()))
    for (rating, count) in grade_counters.items():
        if count > 0:
            p: float = 100 * count / total_count
            ratings_p[rating] = f"{p:.2f}%"
            pass
        pass
    return ratings_p


def test() -> None:
    with open("../assets/data/sub_stats.json", "r") as file:
        json_data: dict = json.load(file)
        pass

    HP, ATK, DEF, HPp, ATKp, DEFp, EM, ER, CR, CD = list(json_data.keys())

    level: int = 20

    sub_stat_dict: dict[str, float] = {
        CR: 14.0,
        CD: 6.2,
        ER: 9.7,
        HP: 239
    }

    artifact_piece: ArtifactPiece = ArtifactPiece(level, sub_stat_dict)
    artifact_piece.analyze(json_data)
    return None


if __name__ == '__main__':
    test()
    pass
