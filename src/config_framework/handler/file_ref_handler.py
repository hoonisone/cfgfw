from typing import Optional, Hashable
from ..context import RecursiveContext

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..manager import ConfigManager

from .handler import ConfigHandler


class FileConfigReferHandler(ConfigHandler):

    MARK = "@file_cfg:"

    def __init__(self,
            config_manager:"ConfigManager"
        )->None:
        self.config_manager = config_manager

    def is_target(self, value:Optional[Hashable])->bool:
        return isinstance(value, str) and value.startswith(self.MARK)

    def handle(self, x:dict)->dict:

        return RecursiveContext.replace(
            data = x,
            is_target = lambda v, k, idx: self.is_target(v),
            replacement = lambda v, k, idx: self.config_manager.load_config(
                path = v.removeprefix(self.MARK), 
                # val_refer_handling = False,  # It'll be conducted at final loading stage
                # function_handling = False, # It'll be conducted at final loading stage
                # remove_temp_values = False, # It'll be conducted at final loading stage
            )
        )
