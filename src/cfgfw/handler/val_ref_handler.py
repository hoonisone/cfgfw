from typing import Optional, Hashable
from ..context import RecursiveContext
from ..tool import DictTool

from .handler import ConfigHandler
class ValueReferHandler(ConfigHandler):
    def __init__(self, dict_tool:DictTool)->None:
        self.dict_tool = dict_tool

    def is_val_refer(self, value:Optional[Hashable])->bool:
        return isinstance(value, str) and value.startswith("@val:")

    def get_keys(self, string:str)->list[str]:
        type, keys = string.split(":")
        return keys.split(".")

    def replace_val(self, x, v):
        try:
            return self.dict_tool.get(x, self.get_keys(v))
        except Exception as e:
            print(e)
            print(v)
            print(x)
            raise e

    def handle(self, x:dict)->dict:

        return RecursiveContext.replace(
            data = x,
            is_target = lambda v, k, idx: self.is_val_refer(v),
            replacement = lambda v, k, idx: self.replace_val(x, v)
        )
