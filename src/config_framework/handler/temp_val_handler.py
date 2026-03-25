
from typing import Any
from ..context import RecursiveContext
from ..tool import DictTool
from .handler import ConfigHandler


class ValueRemoveHandler(ConfigHandler):
    def is_target(self, key:Any)->bool:
        return isinstance(key, str) and key.startswith("_")

    def handle(self, config:Any)->Any:
        return RecursiveContext.filter(
            data = config,
            is_remove_target = lambda v, k, idx: self.is_target(k)
        )

