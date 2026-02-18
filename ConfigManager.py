import json
from pathlib import Path
from types import MappingProxyType
from utils import *
from typing import *

def save_func(func):
    async def wrapper(self, *args, **kwargs):
        result = await func(self, *args, **kwargs)
        await self.save_config()
        return result
    return wrapper


class ConfigManager:
    all_configs = [
        "demba",
        "velikivoda",
        "ulogasmrti",
        "kanalsmrti",
        "goriotpolicija",
        "pollkanal",
    ]
    CONFIG_FILE = Path("config.json")
    config: Dict[str, str]
    def __init__(self):
        self._lock = asyncio.Lock()
        self.load_config()


    def load_config(self):
        if not self.CONFIG_FILE.exists():
            self.config = {}
            return
        with open(self.CONFIG_FILE, "r") as f:
            loaded_data = json.load(f)
        self.config = {
            key: value
            for key, value in loaded_data.items()
        }
        for c in self.all_configs:
            if c not in self.config:
                self.config[c] = ""
      
    async def save_config(self):
        async with self._lock:
            temp_file = self.CONFIG_FILE.with_suffix(".tmp")
            with open(temp_file, "w") as f:
                json.dump(
                    self.config,
                    f,
                    indent=4
                )
            temp_file.replace(self.CONFIG_FILE)
 
    def get_all_config(self):
        return MappingProxyType(self.config)

    def get_config(self, name: str):
        return self.config.get(name, "")

    @save_func
    async def set_config(self, name: str, value: str):
        self.config[name] = value
