from .accessor import ConfigAccessor
from .manager import ConfigManager
from .accessor import PythonConfigAccessor , YamlConfigAccessor
from .handler import *

from typing import List
from .tool import DictTool

from functools import cached_property

class DefaultConfigManagerFactory:

    @cached_property
    def overridden_tag(self)->str:
        return "WillBeOverridden"

    @cached_property
    def dict_tool(self)->DictTool:
        return DictTool(self.overridden_tag)

    @cached_property
    def config_accessor(self)->ConfigAccessor:
        return PythonConfigAccessor()

    def make_config_handlers(self, config_manager:ConfigManager)->List[ConfigHandler]:
        return [
            FileConfigReferHandler(config_manager=config_manager),
            TupleMergeHandler(dict_tool=self.dict_tool),
            BaseFlatHandler(dict_tool=self.dict_tool),
            FunctionHandler(),
            ValueReferHandler(dict_tool=self.dict_tool),
            ValueRemoveHandler(),
            TupleMergeHandler(dict_tool=self.dict_tool),
        ]
    
    @cached_property
    def config_manager(self)->ConfigManager:
        config_manager = ConfigManager(config_accessor=self.config_accessor, handlers=[])
        handlers = self.make_config_handlers(config_manager)
        config_manager.handlers =  handlers
        return config_manager