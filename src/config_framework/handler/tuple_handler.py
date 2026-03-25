from typing import Any
from ..context import RecursiveContext
from ..tool import DictTool
from .handler import ConfigHandler

class TupleMergeHandler(ConfigHandler):
    # config 내부에 (cfg1, cfg2, cfg3) 형태의 튜플이 있으면 튜플을 병합하여 반환

    def __init__(self, dict_tool:DictTool)->None:
        self.dict_tool = dict_tool

    def replacement(self, config:Any)->Any:
        return self.dict_tool.merge(list(config))
        if self.is_tuple_merge_structure(config):
            return 

    def is_target(self, config:Any)->bool:
        return isinstance(config, tuple) and all([isinstance(x, dict) for x in config])

    def handle(self, config:Any)->Any:
        return RecursiveContext.replace(
            data = config,
            is_target = lambda v, k, idx: self.is_target(v),
            replacement = lambda v, k, idx: self.replacement(v)
        )