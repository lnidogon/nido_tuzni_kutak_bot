import json
from pathlib import Path
from utils import *
from typing import *
from Stats import Stats
from types import MappingProxyType

def save_func(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.save_stats()
        return result
    return wrapper


class StatsManager:
    STATS_FILE = Path("stats.json")
    stats: Dict[int, Stats]
    def __init__(self):
        self.load_stats()


    def load_stats(self):
        if not self.STATS_FILE.exists():
            self.stats = {}
            return
        with open(self.STATS_FILE, "r") as f:
            loaded_data = json.load(f)

        self.stats = {
            int(member_id): Stats.from_dict(stat_data)
            for member_id, stat_data in loaded_data.items()
        }

    def save_stats(self):
        with open(self.STATS_FILE, "w") as f:
            json.dump({str(k): v.to_json() for k, v in self.stats.items()}, f, indent=4)

    def get_stats(self):
        return MappingProxyType(self.stats)
    
    def get_stat(self, id: int, name: str):
        return self.get_stats()[id].get_data()[name]
    
    def get_credit(self, id: int):
        return self.get_stats()[id].get_data()['goriot_credit']

    def is_playing_the_game(self, member_id: int):
        return member_id in self.stats.keys()
    
    @save_func
    def update_factor(self, member_id: int, coef: Dict[str, float]):
        for name, value in coef.items():
            self.stats[member_id].update_stat(name + 'factor', value)
        self.stats[member_id].normalise_factors()
        
    @save_func
    def update_stat(self, member_id: int, name: str, amount: int):
        self.stats[member_id].update_stat(name, amount)
    
    @save_func
    def give_credit(self, member_id: int, amount: float):
        self.stats[member_id].update_stat("goriot_credit", amount)

    @save_func
    def init_person(self, member_id: int):
        if(member_id in self.stats.keys()):
            self.stats[member_id].actualise()
            return False
        self.stats[member_id] = Stats()
        return True