from typing import Optional, List

from .accessor import ConfigAccessor
from .handler.handler import ConfigHandler
WillBeOverridden = "WillBeOverridden"


from pathlib import Path

class ConfigManager:
    def __init__(self,
            config_accessor:ConfigAccessor,
            handlers:List[ConfigHandler]
        )->None:
        self.dict_accessor = config_accessor
        self.handlers = handlers

    def load_config(self, path:str|Path, handling:bool = True)->dict:
        config = self.dict_accessor.load_config(path)
        if handling:
            config = self.handle(config)
        return config

    def handle(self, 
            config:dict
        )->dict:

        for handler in self.handlers:
            try:
                config = handler.handle(config)
            except Exception as e:
                print(e)
                raise e

        return config
