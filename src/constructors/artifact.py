"""
Author: Rayla Kurosaki

GitHub: https://github.com/rkp1503
"""

import copy
import math

import artifact_sub_stat.sub_stat_double as ssd
import artifact_sub_stat.sub_stat_helper as ssh
import artifact_sub_stat.sub_stat_single as sss
import artifact_sub_stat.sub_stat_triple as sst
import misc.table_functions as tf

FUNCS: list = [
    sss, ssd, sst,
    # ssq
]
COLUMNS: list[str] = [
    "Single", "Double", "Triple",
    # "Quad"
]
MAX_SUBSTATS: int = len(COLUMNS)


class ArtifactPiece:
    def __init__(self, level: int, sub_stats: list[str],
                 sub_stat_values: list[float]):
        self.level: int = level
        self.sub_stat_1: str = sub_stats[0]
        self.sub_stat_2: str = sub_stats[1]
        self.sub_stat_3: str = sub_stats[2]
        self.sub_stat_4: str = sub_stats[3]
        self.sub_stat_1_value: float = sub_stat_values[0]
        self.sub_stat_2_value: float = sub_stat_values[1]
        self.sub_stat_3_value: float = sub_stat_values[2]
        self.sub_stat_4_value: float = sub_stat_values[3]
        pass

    def get_all_sub_stats(self) -> list[str]:
        return [
            self.sub_stat_1, self.sub_stat_2, self.sub_stat_3, self.sub_stat_4
        ]

    def get_all_sub_stat_values(self) -> list[float]:
        return [
            self.sub_stat_1_value, self.sub_stat_2_value,
            self.sub_stat_3_value, self.sub_stat_4_value
        ]

    def print_details(self) -> None:
        print(f"Current Level: {self.level}\n"
              f"\tSub Stat 1: {self.sub_stat_1}+{self.sub_stat_1_value}\n"
              f"\tSub Stat 2: {self.sub_stat_2}+{self.sub_stat_2_value}\n"
              f"\tSub Stat 3: {self.sub_stat_3}+{self.sub_stat_3_value}\n"
              f"\tSub Stat 4: {self.sub_stat_4}+{self.sub_stat_4_value}")
        return None

    def full_evaluation(self, json_data: dict) -> None:
        sub_stats: list[str] = self.get_all_sub_stats()
        sub_stat_vals: list[float] = self.get_all_sub_stat_values()
        data_to_print: list = [
            ["" for _ in range(MAX_SUBSTATS)] for _ in range(6)
        ]
        for (i, func) in enumerate(FUNCS):
            res: list[tuple[str, str, float]] = func.analyze_sub_stats(
                json_data, sub_stats, sub_stat_vals)
            for (j, e) in enumerate(ssh.format_results(res, i + 1)):
                data_to_print[j][i] = e
                pass
            pass
        data_to_print.insert(0, [f"{col} Sub Stat" for col in COLUMNS])
        tf.print_data_as_table(data_to_print)
        return None

    def evaluate(self, json_data: dict, n: int = 0) -> None:
        sub_stats: list[str] = self.get_all_sub_stats()
        sub_stat_vals: list[float] = self.get_all_sub_stat_values()
        if n == 1:
            print(f"Single Sub Stat Ratings:")
            res: list[tuple[str, str, float]] = sss.analyze_sub_stats(
                json_data, sub_stats, sub_stat_vals)
            ssh.print_results(res, n)
            pass
        elif n == 2:
            print(f"Double Sub Stat Ratings:")
            res: list[tuple[str, str, float]] = ssd.analyze_sub_stats(
                json_data, sub_stats, sub_stat_vals)
            ssh.print_results(res, n)
            pass
        elif n == 3:
            print(f"Triple Sub Stat Ratings:")
            res: list[tuple[str, str, float]] = sst.analyze_sub_stats(
                json_data, sub_stats, sub_stat_vals)
            ssh.print_results(res, n)
            pass
        return None

    def compute_full_probabilities(self) -> None:
        return None


    def simulate_all_possible_rolls(self,
                                    json_data: dict) -> list[list[float]]:
        future_rolls: list[list[float]] = []
        for i in range(5 - math.floor(self.level / 4)):
            if i == 0:
                rolls_iter: list[list[float]] = [
                    self.get_all_sub_stat_values()
                ]
            else:
                rolls_iter: list[list[float]] = copy.deepcopy(future_rolls)
                pass
            for roll in rolls_iter:
                self.simulate_all_possible_rolls_helper(json_data, roll,
                                                        future_rolls)
                pass
            pass
        return future_rolls

    def simulate_all_possible_rolls_helper(self, json_data: dict,
                                           roll: list[float],
                                           data: list[list[float]]) -> None:
        for (i, sub_stat) in enumerate(self.get_all_sub_stats()):
            for val in sorted(json_data[sub_stat].values()):
                temp: list[float] = copy.deepcopy(roll)
                temp[i] += val
                data.append(temp)
                pass
            pass
        return None

    pass
