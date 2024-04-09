"""
Author: Rayla Kurosaki

GitHub: https://github.com/rkp1503
"""


class Weapon:
    def __init__(self):
        self.name: str = ""
        self.quality: int = 0
        self.weapon_type: str = ""
        self.base_atk: int = 0
        self.sub_stat: str = ""
        self.sub_stat_val: float = 0
        self.release_date: str = ""

        self.sort_order: int = -1
        self.refinement: int = 0
        self.level: int = 0
        pass

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name
        return None

    def get_quality(self) -> int:
        return self.quality

    def set_quality(self, quality: int) -> None:
        self.quality = quality
        return None

    def get_weapon_type(self) -> str:
        return self.weapon_type

    def set_weapon_type(self, weapon_type: str) -> None:
        self.weapon_type = weapon_type
        return None

    def get_base_atk(self) -> int:
        return self.base_atk

    def set_base_atk(self, base_atk: int) -> None:
        self.base_atk = base_atk
        return None

    def get_sub_stat(self) -> str:
        return self.sub_stat

    def set_sub_stat(self, sub_stat: str) -> None:
        self.sub_stat = sub_stat
        return None

    def get_sub_stat_val(self) -> float:
        return self.sub_stat_val

    def set_sub_stat_val(self, sub_stat_val: str, local: bool = False) -> None:
        if (self.sub_stat == "Elemental Mastery") or local:
            self.sub_stat_val = float(sub_stat_val)
            pass
        else:
            self.sub_stat_val = float(sub_stat_val[:-1]) / 100
            pass
        return None

    def get_release_date(self) -> str:
        return self.release_date

    def set_release_date(self, release_date: str) -> None:
        self.release_date = release_date
        return None

    def get_sort_order(self) -> int:
        return self.sort_order

    def set_sort_order(self, sort_order: int) -> None:
        self.sort_order = sort_order
        return None

    def get_refinement(self) -> int:
        return self.refinement

    def set_refinement(self, refinement: int) -> None:
        self.refinement = refinement
        return None

    def get_level(self) -> int:
        return self.level

    def set_level(self, level: int) -> None:
        self.level = level
        return None

    def get_weapon_details(self) -> str:
        details: str = (
            f"Name: {self.name}\n"
            f"\tStars: {self.quality}\n"
            f"\tType: {self.weapon_type}\n"
            f"\tBase ATK (Lv 90): {self.base_atk}\n"
            f"\tSub Stat: {self.sub_stat}\n"
            f"\tSub Stat Value: {self.sub_stat_val}\n"
            f"\tRelease Date: {self.release_date}\n"
        )
        return details

    pass
