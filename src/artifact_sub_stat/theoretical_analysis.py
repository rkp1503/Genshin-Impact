"""
Author: Rayla Kurosaki

GitHub: https://github.com/rkp1503
"""

import copy

import matplotlib.pyplot as plt
import seaborn as sns

RVS: list = [0.0, 0.7, 0.8, 0.9, 1.0]


def get_data_set(num_sub_stats: int) -> list[list[float]]:
    data_set: list[list[float]] = []
    if num_sub_stats == 1:
        data_set = [
            [a] for a in RVS
            if (a > 0)
        ]
    elif num_sub_stats == 2:
        data_set = [
            [a, b] for a in RVS for b in RVS
            if (a > 0) and (b > 0)
        ]
    elif num_sub_stats == 3:
        data_set = [
            [a, b, c] for a in RVS for b in RVS for c in RVS
            if (a > 0) and (b > 0) and (c > 0)
        ]
    elif num_sub_stats == 4:
        data_set = [
            [a, b, c, d] for a in RVS for b in RVS for c in RVS for d in RVS
            if (a > 0) and (b > 0) and (c > 0) and (d > 0)
        ]
    return data_set


def add_next_roll(data_set: list[list[float]], data_counts: list[int],
                  next_roll: list[float], count: int) -> None:
    if next_roll not in data_set:
        data_set.append(next_roll)
        data_counts.append(count)
        pass
    else:
        data_counts[data_set.index(next_roll)] += count
        pass
    return None


def create_next_roll(data_set: list[list[float]], data_counts: list[int],
                     roll: list[float], count: int, i: int) -> None:
    for e in RVS:
        next_roll: list[float] = copy.deepcopy(roll)
        next_roll[i] = float(f"{next_roll[i] + e:.1f}")
        add_next_roll(data_set, data_counts, next_roll, count)
        pass
    return None


def get_all_possible_rolls(num_sub_stats: int,
                           num_rolls: int = len(RVS)) -> tuple[
    list[list[float]], list[int]]:
    data_set: list[list[float]] = get_data_set(num_sub_stats)
    data_counts: list[int] = [1 for _ in range(len(data_set))]
    for _ in range(num_rolls):
        temp_data_set: list[list[float]] = copy.deepcopy(data_set)
        temp_data_counts: list[int] = copy.deepcopy(data_counts)
        for (roll, count) in zip(temp_data_set, temp_data_counts):
            for i in range(num_sub_stats):
                create_next_roll(data_set, data_counts, roll, count, i)
                pass
            pass
        pass
    return data_set, data_counts


def update_rv_dict(rv_dict: dict[float, int], rv: float, count: int) -> None:
    if rv not in rv_dict:
        rv_dict[rv] = count
        pass
    else:
        rv_dict[rv] += count
        pass
    return None


def convert_rolls_to_rv(data_set: list[list[float]],
                        data_counts: list[int]) -> dict[float, int]:
    rv_dict: dict[float, int] = {}
    for (roll, count) in zip(data_set, data_counts):
        update_rv_dict(rv_dict, float(f"{sum(roll):.1f}"), count)
        pass
    rv_dict = dict(sorted(rv_dict.items()))
    return rv_dict


def generate_figure(num_sub_stats: int, rv_dict: dict[float, int],
                    fig_type: str = "distribution") -> None:
    num_to_wrd: dict[int, str] = {
        1: "Single",
        2: "Double",
        3: "Triple",
        4: "Quad"
    }
    if fig_type == "line":
        plt.plot(list(rv_dict.keys()), list(rv_dict.values()))
        pass
    else:
        data: list[float] = [rv for (rv, i) in rv_dict.items() for _ in
                             range(i)]
        sns.displot(data, kind="kde", bw_adjust=num_sub_stats)
        pass
    plt.title(f"{num_to_wrd[num_sub_stats]} Sub Stat Distribution")
    plt.xlabel(f"Roll Value")
    plt.show()
    return None


def main(num_sub_stats: int) -> None:
    data_set, data_counts = get_all_possible_rolls(num_sub_stats)

    rv_dict: dict[float, int] = convert_rolls_to_rv(data_set, data_counts)

    generate_figure(num_sub_stats, rv_dict)
    return None


if __name__ == '__main__':
    num_sub_stats: int = 1
    main(num_sub_stats)
    pass
