"""
Author: Rayla Kurosaki

GitHub: https://github.com/rkp1503
"""

import copy

import sub_stat_helper as ssh


def get_all_possible_rolls(json_data: dict, sub_stats: list[str],
                           num_rolls: int = 5) -> (
        tuple)[list[list[float]], list[int]]:
    a_s, b_s, c_s = ssh.get_sub_stat_lists(json_data, sub_stats)
    data_set: list[list[float]] = [
        [a, b, c] for a in a_s for b in b_s for c in c_s
        if (a > 0) and (b > 0) and (c > 0)
    ]
    data_counts: list[int] = [1 for _ in range(len(data_set))]
    for _ in range(num_rolls):
        temp_data_set: list[list[float]] = copy.deepcopy(data_set)
        temp_data_counts: list[int] = copy.deepcopy(data_counts)
        for (roll, count) in zip(temp_data_set, temp_data_counts):
            for a in a_s:
                next_roll_a: list[float] = [roll[0] + a, roll[1], roll[2]]
                ssh.next_roll_helper(next_roll_a, count, data_set, data_counts)
                pass
            for b in b_s:
                next_roll_b: list[float] = [roll[0], roll[1] + b, roll[2]]
                ssh.next_roll_helper(next_roll_b, count, data_set, data_counts)
                pass
            for c in c_s:
                next_roll_c: list[float] = [roll[0], roll[1], roll[2] + c]
                ssh.next_roll_helper(next_roll_c, count, data_set, data_counts)
                pass
            pass
        pass
    return data_set, data_counts


def evaluate_normalized_roll_value(nrv: float) -> str:
    nrv_dict: dict[str, list[float]] = {
        "S+": [7.4, 8.0],
        "S": [6.6, 7.3],
        "A": [5.5, 6.5],
        "B": [4.5, 5.4],
        "C": [3.6, 4.4],
        "D": [2.8, 3.5],
        "F": [0.0, 2.7]
    }
    return ssh.evaluate_normalized_roll_value(nrv, nrv_dict)


def analyze_sub_stats(json_data: dict, all_sub_stats: list[str],
                      all_sub_stat_values: list[float], m: int) -> None:
    print(f"Triple Sub Stat Ratings:")
    results: list[tuple[str, str, float]] = []
    n: int = len(all_sub_stats)
    for i in range(0, n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                sub_stats: list[str] = [
                    all_sub_stats[i], all_sub_stats[j],
                    all_sub_stats[k]
                ]
                data: list[list[float]] = [
                    [
                        all_sub_stat_values[i], all_sub_stat_values[j],
                        all_sub_stat_values[k]
                    ]
                ]
                rv: float = ssh.convert_data_to_roll_value(json_data,
                                                           sub_stats, data)[0]
                max_roll_values: list[float] = ssh.get_max_roll_values(
                    json_data, sub_stats
                )
                nrv: float = round(rv / max(max_roll_values), 1)
                rating: str = evaluate_normalized_roll_value(nrv)
                results.append(("/".join(sub_stats), rating, nrv))
                pass
            pass
        pass
    ssh.print_results(results, m)
    return None


def compute_probabilities(json_data: dict, all_sub_stats: list[str],
                          rolls: list[list[float]]) -> None:
    n: int = len(all_sub_stats)
    for i in range(0, n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                sub_stats: list[str] = [
                    all_sub_stats[i], all_sub_stats[j], all_sub_stats[k]
                ]
                max_roll_values: list[float] = ssh.get_max_roll_values(
                    json_data, sub_stats
                )
                grade_counters: dict[str, int] = {"S+": 0, "S": 0, "A": 0,
                                                  "B": 0, "C": 0, "D": 0,
                                                  "F": 0}
                for roll in rolls:
                    temp: list[list[float]] = [
                        [roll[i], roll[j], roll[k]]
                    ]
                    rv: float = ssh.convert_data_to_roll_value(json_data,
                                                               sub_stats,
                                                               temp)[0]
                    nrv: float = round(rv / max(max_roll_values), 1)
                    rating: str = evaluate_normalized_roll_value(nrv)
                    grade_counters[rating] += 1
                    pass
                ssh.compute_probabilities(grade_counters, sub_stats)
                pass
            pass
        pass
    return None


def main(json_data: dict, sub_stats: list[str], normalize: bool) -> None:
    data_set, data_counts = get_all_possible_rolls(json_data, sub_stats)
    rv_lst: list[float] = ssh.convert_data_to_roll_value(json_data, sub_stats,
                                                         data_set,
                                                         normalize=normalize)
    data: list[float] = [
        rv for (rv, i) in zip(rv_lst, data_counts) for _ in range(i)
    ]
    ssh.display_distribution(sub_stats, data, normalize=normalize, bw_adjust=3)
    return None
