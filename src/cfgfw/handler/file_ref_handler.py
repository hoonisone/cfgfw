from typing import Optional, Hashable, TYPE_CHECKING, Any
from ..context import RecursiveContext

if TYPE_CHECKING:
    from ..manager import ConfigManager

from .handler import ConfigHandler
from ..tool import DictTool
from pathlib import Path

class FileConfigReferHandler(ConfigHandler):

    MARK = "@file_cfg:"

    def __init__(self,
            dict_tool:DictTool,
            config_manager:"ConfigManager",
        )->None:
        self.dict_tool = dict_tool
        self.config_manager = config_manager

    def is_target(self, value:Optional[Hashable])->bool:
        return isinstance(value, str) and value.startswith(self.MARK)

    def load(self, v:str)->Any:
        v = v.removeprefix(self.MARK)
        tokens = v.split(":")
        file_path = tokens[0]
        value_path = tokens[1] if len(tokens) > 1 else None

        file_path = Path(file_path).resolve()
        config = self.config_manager.load_config(file_path, handling=True, lazy_handling=False)

        if value_path is not None:
            value_path = value_path.split(".")
            return self.dict_tool.get(config, value_path)
        else:
            return config

    def handle(self, x:dict)->dict:

        return RecursiveContext.replace(
            data = x,
            is_target = lambda v, k, idx: self.is_target(v),
            replacement = lambda v, k, idx: self.load(v), 
        )
