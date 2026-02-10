from typing import List, Dict
from types import MappingProxyType
class Stats:
    data: Dict[str, float] = {}
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
        "gambling"
        ]

    def __init__(self, **kwargs):
        if kwargs:
            self.data  = {key: float(val) for key, val in kwargs.items()}
        self.actualise()
    def actualise(self):
        for stat in self.all_stats:
            if(stat not in self.data):
                self.data[stat] = 0
    def to_json(self):
        return {key: str(val) for key, val in self.data.items()}
    
    def get_data(self):
        return MappingProxyType(self.data)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
