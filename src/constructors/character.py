"""
Author: Rayla Kurosaki

GitHub: https://github.com/rkp1503
"""


class Character:
    def __init__(self, name: str, quality: int, sex: str | None,
                 element: str | None, nation: str | None, weapon_type: str,
                 model_type: str, signature_weapon: str | None,
                 base_hp: float, base_atk: float, base_def: float,
                 special_stat: str, release_date: str, sort_order: int | None):
        # Database Data
        self.name: str = name
        self.quality: int = quality
        self.sex: str | None = sex
        self.element: str | None = element
        self.nation: str | None = nation
        self.weapon_type: str = weapon_type
        self.model_type: str = model_type
        self.signature_weapon: str | None = signature_weapon
        self.base_hp: float = base_hp
        self.base_atk: float = base_atk
        self.base_def: float = base_def
        self.special_stat: str = special_stat
        self.release_date: str = release_date
        self.sort_order: int = sort_order

        # In-Game Data
        self.level: int = 1
        self.ascension: int = 0
        self.hp: float = 0.0
        self.attack: float = 0.0
        self.defense: float = 0.0
        self.elemental_mastery: float = 0.0
        self.crit_rate: float = 0.05
        self.crit_damage: float = 0.5
        self.healing_bonus: float = 0.0
        self.energy_recharge: float = 1.0

        self.anemo_damage_bonus: float = 0.0
        self.anemo_resistance: float = 0.0
        self.geo_damage_bonus: float = 0.0
        self.geo_resistance: float = 0.0
        self.electro_damage_bonus: float = 0.0
        self.electro_resistance: float = 0.0
        self.dendro_damage_bonus: float = 0.0
        self.dendro_resistance: float = 0.0
        self.hydro_damage_bonus: float = 0.0
        self.hydro_resistance: float = 0.0
        self.pyro_damage_bonus: float = 0.0
        self.pyro_resistance: float = 0.0
        self.cryo_damage_bonus: float = 0.0
        self.cryo_resistance: float = 0.0
        self.physical_damage_bonus: float = 0.0
        self.physical_resistance: float = 0.0
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

    def get_sex(self) -> str | None:
        return self.sex

    def set_sex(self, sex: str | None) -> None:
        self.sex = sex
        return None

    def get_element(self) -> str | None:
        return self.element

    def set_element(self, element: str | None) -> None:
        self.element = element
        return None

    def get_nation(self) -> str | None:
        return self.nation

    def set_nation(self, nation: str | None) -> None:
        self.nation = nation
        return None

    def get_weapon_type(self) -> str:
        return self.weapon_type

    def set_weapon_type(self, weapon_type: str) -> None:
        self.weapon_type = weapon_type
        return None

    def get_model_type(self) -> str:
        return self.model_type

    def set_model_type(self, model_type: str) -> None:
        self.model_type = model_type
        return None

    def get_signature_weapon(self) -> str:
        return self.signature_weapon

    def set_signature_weapon(self, signature_weapon: str) -> None:
        self.signature_weapon = signature_weapon
        return None

    def get_base_hp(self) -> float:
        return self.base_hp

    def set_base_hp(self, base_hp: float) -> None:
        self.base_hp = base_hp
        return None

    def get_base_atk(self) -> float:
        return self.base_atk

    def set_base_atk(self, base_atk: float) -> None:
        self.base_atk = base_atk
        return None

    def get_base_def(self) -> float:
        return self.base_def

    def set_base_def(self, base_def: float) -> None:
        self.base_def = base_def
        return None

    def get_ascension_stat(self) -> str:
        return self.special_stat

    def set_ascension_stat(self, ascension_stat: str) -> None:
        self.special_stat = ascension_stat
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

    def compute_base_hp_value(self) -> float:
        return -1

    def compute_base_atk_value(self) -> float:
        return -1

    def compute_base_def_value(self) -> float:
        return -1

    pass
