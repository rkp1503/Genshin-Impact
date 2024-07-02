"""
Author: Rayla Kurosaki

GitHub: https://github.com/rkp1503
"""


def sort_table(order: str = "asc") -> None:
    return None


def get_table_widths(data: list) -> list:
    widths = [0 for _ in range(len(data[0]))]
    for lst in data:
        for (i, e) in enumerate(lst):
            length: int = len(e)
            if widths[i] < length:
                widths[i] = length
                pass
            pass
        pass
    return widths


def print_header(header: list, widths: list) -> None:
    strings = ["| "]
    for (i, (row_header, width)) in enumerate(zip(header, widths)):
        strings.append(row_header.center(width, " "))
        # strings.append(row_header.ljust(width, " "))
        if i == len(widths) - 1:
            strings.append(" |")
            pass
        else:
            strings.append(" | ")
            pass
        pass
    print("".join(strings))
    return None


def print_separator(widths: list) -> None:
    strings = ["|-"]
    for (i, (width)) in enumerate(widths):
        strings.append("".ljust(width, "-"))
        if i == len(widths) - 1:
            strings.append("-|")
            pass
        else:
            strings.append("-+-")
            pass
        pass
    print("".join(strings))
    return None


def print_data(data: list, widths: list) -> None:
    for lst in data:
        strings = ["| "]
        for (i, (row_header, width)) in enumerate(zip(lst, widths)):
            strings.append(row_header.ljust(width, " "))
            if i == len(widths) - 1:
                strings.append(" |")
                pass
            else:
                strings.append(" | ")
                pass
            pass
        print("".join(strings))
        pass
    return None


def print_data_as_table(data: list) -> None:
    widths: list = get_table_widths(data)
    header: list = data.pop(0)
    print_header(header, widths)
    print_separator(widths)
    print_data(data, widths)
    return None
