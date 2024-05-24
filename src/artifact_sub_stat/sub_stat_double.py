"""
Author: Rayla Kurosaki

GitHub: https://github.com/rkp1503
"""

import copy

import sub_stat_helper as ssh


def get_all_possible_rolls(json_data: dict, sub_stats: list[str],
                           num_rolls: int = 5) -> list[list[float]]:
    a_s, b_s = ssh.get_sub_stat_lists(json_data, sub_stats)
    data: list[list[float]] = [
        [a, b] for a in a_s for b in b_s
        if (a > 0) and (b > 0)
    ]
    for _ in range(num_rolls):
        for vals in copy.deepcopy(data):
            for a in a_s:
                data.append([vals[0] + a, vals[1]])
                pass
            for b in b_s:
                data.append([vals[0], vals[1] + b])
                pass
            pass
        pass
    return data


def evaluate_normalized_roll_value(nrv: float) -> str:
    nrv_dict: dict[str, list[float]] = {
        "S+": [6.4, 7.0],
        "S": [5.7, 6.3],
        "A": [4.7, 5.6],
        "B": [3.7, 4.6],
        "C": [2.9, 3.6],
        "D": [2.1, 2.8],
        "F": [0.0, 2.0]
    }
    return ssh.evaluate_normalized_roll_value(nrv, nrv_dict)


def analyze_sub_stats(json_data: dict, all_sub_stats: list[str],
                      all_sub_stat_values: list[float], m: int) -> None:
    print(f"Double Sub Stat Ratings:")
    results: list[tuple[str, str, float]] = []
    n: int = len(all_sub_stats)
    for i in range(0, n):
        for j in range(i + 1, n):
            sub_stats: list[str] = [
                all_sub_stats[i], all_sub_stats[j]
            ]
            data: list[list[float]] = [
                [
                    all_sub_stat_values[i], all_sub_stat_values[j]
                ]
            ]
            rv: float = ssh.convert_data_to_roll_value(json_data, sub_stats,
                                                       data)[0]
            max_roll_values: list[float] = ssh.get_max_roll_values(json_data,
                                                                   sub_stats)
            nrv: float = round(rv / max(max_roll_values), 1)
            rating: str = evaluate_normalized_roll_value(nrv)
            results.append(("/".join(sub_stats), rating, nrv))
            pass
        pass
    ssh.print_results(results, m)
    return None


def compute_probabilities(json_data: dict, all_sub_stats: list[str],
                          rolls: list[list[float]]) -> None:
    n: int = len(all_sub_stats)
    for i in range(0, n):
        for j in range(i + 1, n):
            sub_stats: list[str] = [
                all_sub_stats[i], all_sub_stats[j]
            ]
            max_roll_values: list[float] = ssh.get_max_roll_values(json_data,
                                                                   sub_stats)
            grade_counters: dict[str, int] = {"S+": 0, "S": 0, "A": 0, "B": 0,
                                              "C": 0, "D": 0, "F": 0}
            for roll in rolls:
                temp: list[list[float]] = [
                    [roll[i], roll[j]]
                ]
                rv: float = ssh.convert_data_to_roll_value(json_data,
                                                           sub_stats, temp)[0]
                nrv: float = round(rv / max(max_roll_values), 1)
                rating: str = evaluate_normalized_roll_value(nrv)
                grade_counters[rating] += 1
                pass
            ssh.compute_probabilities(grade_counters, sub_stats)
            pass
        pass
    return None
