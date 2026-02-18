from typing import List, Dict
from types import MappingProxyType
class Stats:
    data: Dict[str, float]
    all_stats: List[str] = [
        "vfactor", 
        "bfactor", 
        "gfactor", 
        "lfactor", 
        "nfactor", 
        "rfactor", 
        
        "goriot_credit",
        
        "sus",
        "pravicnost",
        "zloba",
        "zahvalnost",
        "benjavicnost",
        "rossini odanost",
        "closetness",
        "gambling",
        
        "steals",
        "judged_steals",
        "judge",
        "kills",
        "dead",

        ]
    lower_bound: Dict[str, float] = {
        "closetness" : 0,
        "zahvalnost" : 0,
        "pravicnost" : 0,
        "benjavicnost" : 0,
    }

    def __init__(self, **kwargs):
        self.data = {}
        if kwargs:
            self.data  = {key: float(val) for key, val in kwargs.items()}
        self.actualise()
    def actualise(self):
        for stat in self.all_stats:
            if(stat not in self.data.keys()):
                self.data[stat] = 0
    def to_json(self):
        return {key: str(val) for key, val in self.data.items()}
    
    def get_data(self):
        return MappingProxyType(self.data)

    def update_stat(self, name: str, coef: float):
        if name not in self.data:
            print(f"{name} is not a stat")
        self.data[name] = self.data.get(name, 0) + coef
        
    def set_stat(self, name: str, coef: float):
        if name not in self.data:
            print(f"{name} is not a stat")
        self.data[name] = coef

    def normalise_factors(self):
        fvalue_list = [self.data.get(x, 0) for x in self.all_stats[0:6]]
        min_value = min(fvalue_list)
        for i in range(6):
            fvalue_list[i] = fvalue_list[i] - min_value
        factorsum = sum(fvalue_list)
        for factor_name in self.all_stats[0:6]:
            self.data[factor_name] = (self.data.get(factor_name, 0) - min_value) / factorsum * 100
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)
