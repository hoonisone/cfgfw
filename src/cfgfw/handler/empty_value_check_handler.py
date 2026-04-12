
from typing import Any
from ..context import RecursiveContext
from ..tool import DictTool
from .handler import ConfigHandler


EMPTY_TAG = "WillBeOverridden"

class EmptyValueCheckHandler(ConfigHandler):
    """
        config 안에 EMPTY_TAG 가 있는지 체크하고
        있다면 오류와 함께 Empty key 목록을 출력한다.
    """
    def __init__(self, empty_tag:Any=EMPTY_TAG)->None:
        self.empty_tag = empty_tag

    def is_target(self, state:Any)->bool:
        return state['data'] is self.empty_tag

    def make_return(self, state:Any)->Any:
        keys = state['ref_history']
        return keys

    def handle(self, config:Any)->Any:
        empty_keys =RecursiveContext.find(
            data = config,
            is_target = self.is_target,
            make_return = self.make_return
        )

        if len(empty_keys) > 0:
            error_text = "Empty value found:\n"
            for key in empty_keys:
                error_text += f"    {key}\n"
            raise ValueError(error_text)

        return config