from abc import ABC, abstractmethod
from typing import Any

class ConfigHandler(ABC):
    @abstractmethod
    def handle(self, config:dict)->Any:
        pass