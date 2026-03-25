from abc import ABC, abstractmethod

class ConfigHandler(ABC):
    @abstractmethod
    def handle(self, config:dict)->dict:
        pass