from typing import Optional, List

from .accessor import ConfigAccessor
from .handler.handler import ConfigHandler
WillBeOverridden = "WillBeOverridden"


from pathlib import Path

class ConfigManager:
    def __init__(self,
            config_accessor:ConfigAccessor,
            handlers:List[ConfigHandler],
            lazy_handlers:List[ConfigHandler]
        )->None:
        self.dict_accessor = config_accessor
        self.handlers = handlers
        self.lazy_handlers = lazy_handlers

    def load_config(self, path:str|Path, handling:bool = True, lazy_handling:bool = True)->dict:
        config = self.dict_accessor.load_config(path)

        if handling:
            config = self.run_all_handlers(config, self.handlers)

        if lazy_handling:
            config = self.run_all_handlers(config, self.lazy_handlers)

        return config

    def run_all_handlers(self, 
            config:dict, 
            handlers:List[ConfigHandler]
        )->dict:

        for handler in handlers:
            try:
                config = handler.handle(config)
            except Exception as e:
                print(e)
                raise e

        return config
