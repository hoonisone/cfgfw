from ..tool import DictTool
from .handler import ConfigHandler
class BaseFlatHandler(ConfigHandler):

    def __init__(self, dict_tool:DictTool)->None:
        self.dict_tool = dict_tool

    def handle(self, config:dict)->dict:
        if "_base" in config:

            base:dict = config["_base"]        
            config.pop("_base")

            assert isinstance(base, dict), f"base must be a dict or Config, but base's type is {type(base)}"
            config = self.dict_tool.merge_config(base, config)
        return config