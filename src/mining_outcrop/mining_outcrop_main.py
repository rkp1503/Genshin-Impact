"""
Author: Rayla Kurosaki

GitHub: https://github.com/rkp1503
"""

import datetime
import itertools
import json
import os
import shutil

import openpyxl

import mining_outcrop_helper as moh
import misc.merge_sort as ms
import misc.table_functions as tf

NATIONS: list = [
    "Mondstadt", "Liyue", "Inazuma", "Sumeru", "Fontaine",
    # "Natlan", "Snezhnaya"
]


def get_json_data(path_to_file: str) -> dict:
    if os.path.getsize(path_to_file) < 2:
        json_data: dict = {
            "last_updated": "2020-09-28",
            "Mondstadt": {
                "data": {},
                "npc_data": {}
            },
            "Liyue": {
                "data": {},
                "npc_data": {}
            },
            "Inazuma": {
                "data": {},
                "npc_data": {}
            },
            "Sumeru": {
                "data": {},
                "npc_data": {}
            },
            "Fontaine": {
                "data": {},
                "npc_data": {}
            },
            "Natlan": {
                "data": {},
                "npc_data": {}
            },
            "Snezhnaya": {
                "data": {},
                "npc_data": {}
            }
        }
        pass
    else:
        with open(path_to_file, "r") as file:
            json_data: dict = json.load(file)
            pass
        pass
    return json_data


def add_excel_data_to_json(path_to_excel_file: str,
                           path_to_copied_excel_file: str,
                           json_data: dict) -> None:
    prev_date = datetime.datetime.strptime(json_data["last_updated"],
                                           '%Y-%m-%d')
    shutil.copyfile(path_to_excel_file, path_to_copied_excel_file)
    workbook = openpyxl.load_workbook(path_to_copied_excel_file)

    nations: list = [
        "Mondstadt", "Liyue", "Inazuma", "Sumeru", "Fontaine",
        # "Natlan", "Snezhnaya"
    ]
    for nation in NATIONS:
        moh.add_excel_data_to_json_helper(prev_date, workbook, nation,
                                          json_data)
        pass

    # os.remove(path_to_copied_excel_file)
    return None


def ley_line_occurrences_analysis(nation: str, json_data: dict,
                                  sort: str | None = None) -> None:
    moh.print_header("Ley Line Pairing Probabilities")
    data_to_print: list = []
    total_entries: int = moh.get_num_of_entries(nation, json_data)
    for (ley_line, entries) in json_data[nation]["data"].items():
        wealth, revelation = ley_line.split(" | ")
        data_to_print.append([wealth, revelation, len(entries)])
        pass
    for (i, lst) in enumerate(data_to_print):
        lst[2] /= total_entries
        pass
    if sort is not None:
        ms.merge_sort_asc(data_to_print, 1)
        ms.merge_sort_asc(data_to_print, 0)
        if sort == "probability":
            ms.merge_sort_desc(data_to_print, 2)
            pass
        pass
    for (i, lst) in enumerate(data_to_print):
        lst[2] = f"{lst[2]:.2%}"
        pass
    data_to_print.insert(0, ["Wealth", "Revelation", "Probability"])
    tf.print_data_as_table(data_to_print)
    return None


def ley_line_mining_locations_probabilities(nation: str,
                                            json_data: dict) -> None:
    moh.print_header("Ley Line Mining Location Analysis")
    data_to_print: list = []
    for (ley_line, entries) in json_data[nation]["data"].items():
        wealth, revelation = ley_line.split(" | ")
        data_to_print.append([wealth, revelation, entries])
        pass
    ms.merge_sort_asc(data_to_print, 1)
    ms.merge_sort_asc(data_to_print, 0)
    for lst in data_to_print:
        print(f"• {lst[0]} | {lst[1]}")
        pass
    return None


def npc_analysis(nation: str, json_data: dict) -> None:
    moh.print_header("NPC Analysis")
    npc_data: dict = json_data[nation]["npc_data"]
    num_npc: int = moh.get_num_npc(nation)
    if len(npc_data) == 0:
        npc_data: dict = moh.generate_empty_data(num_npc)
        pass
    temp_data: dict = moh.generate_empty_data(num_npc)
    for lst in json_data[nation]["data"].values():
        for e_dict in lst:
            for npc in npc_data.keys():
                if not e_dict[npc]:
                    continue
                    pass
                if e_dict[npc] not in temp_data[npc]:
                    temp_data[npc].append(e_dict[npc])
                    pass
                pass
            pass
        pass
    for (key, lst) in temp_data.items():
        all_locs: list = sorted(
            list(set([e for sub_lst in lst for e in sub_lst])))
        sol_index: list = [[] for _ in range(len(all_locs))]
        permutations: list = list(itertools.permutations(all_locs))
        for permutation in permutations:
            is_valid: list = []
            for sub_lst in lst:
                i_s: list = [permutation.index(e) for e in sub_lst]
                if i_s == sorted(i_s):
                    is_valid.append(True)
                    pass
                else:
                    is_valid.append(False)
                    pass
                pass
            if all(is_valid):
                for (i, e) in enumerate(permutation):
                    sol_index[i].append(e)
                    pass
                pass
            pass
        sol_set: list = [sorted(list(set(sub_lst))) for sub_lst in sol_index]
        for sol in sol_set:
            if len(sol) == 1:
                npc_data[key].append(sol[0])
                pass
            else:
                npc_data[key].append(sol)
                pass
            pass
        pass
    for (npc, data) in npc_data.items():
        for (i, lst) in enumerate(data):
            if isinstance(lst, list):
                lst: list = [str(e) for e in sorted([int(e) for e in lst])]
                data[i] = f"{{{','.join(lst)}}}"
                pass
            else:
                data[i] = lst
                pass
            pass
        print(f"{npc}: {" -> ".join(data)}")
        pass
    return None


def print_full_analysis(nation: str, json_data: dict,
                        sort: str | None = None) -> None:
    if nation in NATIONS:
        moh.print_header(f"{nation} Full Analysis")
        print(f"Size of data: {moh.get_num_of_entries(nation, json_data)}")
        print()
        ley_line_occurrences_analysis(nation, json_data, sort=sort)
        print()
        ley_line_mining_locations_probabilities(nation, json_data)
        print()
        npc_analysis(nation, json_data)
        pass
    return None
