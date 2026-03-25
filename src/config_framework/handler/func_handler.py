from typing import Any
from ..context import RecursiveContext
from .handler import ConfigHandler


class FunctionHandler(ConfigHandler):
    MARK = "@func:"
    
    def is_func_refer(self, value:Any)->bool:
        return isinstance(value, str) and value.startswith(self.MARK)

    def func_handle(self, value:str, locals:dict)->Any:
        command = value.removeprefix(self.MARK)
        return eval(command, {}, locals)


    def handle(self, config:Any)->Any:
        return RecursiveContext.replace(
            data = config,
            is_target = lambda v, k, idx: self.is_func_refer(v),
            replacement = lambda v, k, idx: self.func_handle(v, config)
        )

        return RecursiveContext.filter(
            data = config,
            is_remove_target = lambda v, k, idx: self.is_func_refer(v)
        )