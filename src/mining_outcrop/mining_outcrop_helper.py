"""
Author: Rayla Kurosaki

GitHub: https://github.com/rkp1503
"""

import datetime
import json

import openpyxl


def update_json_file(path_to_file: str, json_data: dict) -> None:
    json_data["last_updated"] = datetime.datetime.today().strftime('%Y-%m-%d')
    with open(path_to_file, "w") as file:
        json.dump(json_data, file, indent=2)
        pass
    return None


def convert_data(data: str | None) -> list:
    if data is None:
        return []
    elif isinstance(data, int):
        return [str(data)]
    else:
        return data.split(", ")
    pass


def get_num_npc(nation: str) -> int:
    if nation in ["Mondstadt"]:
        return 3
    elif nation in ["Liyue", "Inazuma", "Sumeru"]:
        return 4
    elif nation in ["Fontaine"]:
        return 7
    else:
        pass
    pass


def row_to_dict(nation: str, row) -> dict:
    buffer: int = 0
    if nation == "Liyue":
        buffer = 1
        pass
    row_as_dict: dict = {
        "day": row[0].value,
        "wealth": row[1 + buffer].value,
        "revelation": row[2 + buffer].value,
        "unmarked": convert_data(row[3 + buffer].value),
        "blacksmith": convert_data(row[4 + buffer].value),
    }
    num_npc: int = get_num_npc(nation)
    for i in range(num_npc):
        npc: str = f"npc_{chr(ord('`') + i + 1)}"
        row_as_dict[npc] = convert_data(row[5 + i + buffer].value)
        pass
    return row_as_dict


def add_excel_data_to_json_helper(prev_date: datetime.datetime,
                                  workbook: openpyxl.Workbook,
                                  nation: str, json_data: dict) -> None:
    today = datetime.datetime.today()
    worksheet = workbook[nation]
    for row in worksheet.iter_rows(min_row=2):
        row_as_dict: dict = row_to_dict(nation, row)
        if row_as_dict["day"] > today:
            break
            pass
        if prev_date > row_as_dict["day"]:
            continue
            pass
        ley_line: str = f"{row_as_dict['wealth']} | {row_as_dict['revelation']}"
        if ley_line not in json_data[nation]["data"]:
            json_data[nation]["data"][ley_line] = []
            pass
        row_as_dict.pop("day")
        row_as_dict.pop("wealth")
        row_as_dict.pop("revelation")
        json_data[nation]["data"][ley_line].append(row_as_dict)
        pass
    return None


def print_header(header: str) -> None:
    print(f" {header} ".center(79, "~"))
    return None


def get_num_of_entries(nation: str, json_data: dict) -> int:
    n: int = 0
    for entries in json_data[nation]["data"].values():
        n += len(entries)
        pass
    return n


def generate_empty_data(num_npc: int) -> dict:
    return {f"npc_{chr(ord('`') + i + 1)}": [] for i in range(num_npc)}
