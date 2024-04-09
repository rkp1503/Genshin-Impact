"""
Author: Rayla Kurosaki

GitHub: https://github.com/rkp1503
"""


class Character:
    def __init__(self):
        self.name: str = ""
        self.quality: int = 0
        self.vision: str | None = None
        self.sex: str | None = None
        self.nation: str | None = None
        self.weapon: str = ""
        self.signature_weapon: str = ""
        self.ascension_stat: str = ""
        self.ascension_stat_val: float = 0.0
        self.release_date: str = ""
        self.sort_order: int = -1
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

    def get_vision(self) -> str | None:
        return self.vision

    def set_vision(self, element: str | None) -> None:
        self.vision = element
        return None

    def get_sex(self) -> str | None:
        return self.sex

    def set_sex(self, sex: str | None) -> None:
        self.sex = sex
        return None

    def get_nation(self) -> str | None:
        return self.nation

    def set_nation(self, nation: str | None) -> None:
        self.nation = nation
        return None

    def get_weapon(self) -> str:
        return self.weapon

    def set_weapon(self, weapon: str) -> None:
        self.weapon = weapon
        return None

    def get_signature_weapon(self) -> str:
        return self.signature_weapon

    def set_signature_weapon(self, signature_weapon: str) -> None:
        self.signature_weapon = signature_weapon
        return None

    def get_ascension_stat(self) -> str:
        return self.ascension_stat

    def set_ascension_stat(self, ascension_stat: str) -> None:
        self.ascension_stat = ascension_stat
        return None

    def get_ascension_stat_val(self) -> float:
        return self.ascension_stat_val

    def set_ascension_stat_val(self, ascension_stat_val: str,
                               local: bool = False) -> None:
        if (self.ascension_stat == "Elemental Mastery") or local:
            self.ascension_stat_val = float(ascension_stat_val)
            pass
        else:
            self.ascension_stat_val = float(ascension_stat_val[:-1]) / 100
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

    def get_character_details(self) -> str:
        details: str = (
            f"Name: {self.name}\n"
            f"\tStars: {self.quality}\n"
            f"\tVision: {self.vision}\n"
            f"\tSex: {self.sex}\n"
            f"\tNation: {self.nation}\n"
            f"\tWeapon Type: {self.weapon}\n"
            f"\tSignature Weapon: {self.signature_weapon}\n"
            f"\tAscension Stat: {self.ascension_stat}\n"
            f"\tAscension Stat Value: {self.ascension_stat_val}\n"
            f"\tRelease Date: {self.release_date}\n"
            f"\tSort Order: {self.sort_order}\n"
        )
        return details

    pass
