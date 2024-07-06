"""
Author: Rayla Kurosaki

GitHub: https://github.com/rkp1503
"""

import matplotlib.pyplot as plt
import seaborn as sns


def get_sub_stat_lists(json_data: dict,
                       sub_stats: list[str]) -> list[list[float]]:
    sub_stat_lsts: list[list[float]] = [
        list(json_data[sub_stat].values()) for sub_stat in sub_stats
    ]
    if len(sub_stats) < 4:
        for (i, sub_stat_lst) in enumerate(sub_stat_lsts):
            sub_stat_lst.append(0)
            sub_stat_lsts[i] = sorted(sub_stat_lst)
            pass
        pass
    return sub_stat_lsts


def convert_data_to_roll_value(json_data: dict, sub_stats: list[str],
                               data: list[list[float]],
                               normalize: bool = False) -> list[float]:
    all_vals: list[float] = [
        json_data[sub_stat]["X"] for sub_stat in sub_stats
    ]
    max_val: float = max(all_vals)
    multipliers: list[float] = [max_val / val for val in all_vals]
    norm: float = 1.0
    if normalize:
        norm: float = 1 / max_val
        pass
    roll_values: list[float] = []
    for roll in data:
        rv: float = 0.0
        for i in range(len(all_vals)):
            rv += roll[i] * multipliers[i] * norm
            pass
        roll_values.append(rv)
        pass
    return roll_values


def display_distribution(sub_stats: list[str], data: list[float],
                         normalize: bool = False, bw_adjust: int = 1) -> None:
    num_to_wrd: dict[int, str] = {
        1: "Single",
        2: "Double",
        3: "Triple",
        4: "Quad"
    }
    prefix_2: str = num_to_wrd[len(sub_stats)]
    if normalize:
        prefix_1: str = f"Normalized"
        prefix_3: str = f"Normalized "
        pass
    else:
        prefix_1: str = f"{'/'.join(sub_stats)}:"
        prefix_3: str = f""
        pass
    sns.displot(data, kind="kde", bw_adjust=bw_adjust)
    plt.title(f"{prefix_1} {prefix_2} Sub Stat Distribution")
    plt.xlabel(f"{prefix_3}Roll Value")
    plt.show()
    return None


def evaluate_normalized_roll_value(nrv: float,
                                   nrv_dict: dict[str, list[float]]) -> str:
    for (grade, nrvs) in nrv_dict.items():
        nrv_min, nrv_max = nrvs
        if nrv_min <= nrv <= nrv_max:
            return grade
        pass
    pass


def format_results(results: list[tuple[str, str, float]], n: int) -> list[str]:
    res_fmt: list[str] = []
    for result in sorted(results, key=lambda x: x[2], reverse=True):
        sub_stat, rating, nrv = result
        p: float = round(100 * nrv / (5 + n), 2)
        res_fmt.append(f"{sub_stat}: {rating} ({p}%)")
        pass
    return res_fmt


def print_results(results: list[tuple[str, str, float]], n: int) -> None:
    for res in format_results(results, n):
        print(f"\t{res}")
        pass
    return None


def get_max_roll_values(json_data: dict, sub_stats: list[str]) -> list[float]:
    all_rv_vals_lst: list[list[float]] = [
        list(json_data[sub_stat].values()) for sub_stat in sub_stats
    ]
    max_lst: list = [max(lst) for lst in all_rv_vals_lst]
    return all_rv_vals_lst[max_lst.index(max(max_lst))]


def compute_probabilities(grade_counters: dict[str, int],
                          sub_stats: list[str]) -> None:
    grade_probabilities: dict[str, str] = {}
    for (grade, counter) in grade_counters.items():
        p: float = round(100 * counter / sum(list(grade_counters.values())), 2)
        if p > 0:
            grade_probabilities[grade] = f"{p}%"
            pass
        pass
    print(f"\t{'/'.join(sub_stats)}: {grade_probabilities}")
    return None


def next_roll_helper(next_roll: list[float], count: int,
                     data_set: list[list[float]],
                     data_counts: list[int]) -> None:
    if next_roll not in data_set:
        data_set.append(next_roll)
        data_counts.append(count)
        pass
    else:
        data_counts[data_set.index(next_roll)] += count
        pass
    return None
