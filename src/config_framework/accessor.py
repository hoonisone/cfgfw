import runpy
from pathlib import Path
from abc import ABC, abstractmethod

class ConfigAccessor(ABC):
    @abstractmethod
    def load_config(self, path:str|Path)->dict:
        pass
    @abstractmethod
    def dump_config(self, config: dict, path: str|Path) -> None:
        pass

class YamlConfigAccessor(ConfigAccessor):

    @classmethod
    def load_config(cls, path:str|Path)->dict:
        import yaml

        with open(path, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        return config

    @classmethod
    def dump_config(cls, config: dict, path: str|Path) -> None:
        import yaml
        if isinstance(path, Path):
            path = str(path)
        yaml.dump(config, open(path, 'w'))



class PythonConfigAccessor(ConfigAccessor):
    @classmethod
    def load_config(cls, path:str|Path)->dict:
        """파이썬 파일을 실행하고 최종 전역 변수 dict만 반환"""
        # runpy는 일단 파일을 실행한 뒤 전체 변수 dict를 돌려줌
        if isinstance(path, Path):
            path = str(path)

        g = runpy.run_path(path)

        # config 파일 실행으로 생긴 변수만 골라내기
        config = {
            k: v for k, v in g.items()
            if not k.startswith("__")   # 파이썬 시스템용 변수 제외
            and not callable(v)         # 함수는 대부분 config 아님
            and not isinstance(v, type) # 클래스도 제외 가능(원하면 빼도 됨)
        }

        return config

    @classmethod
    def dump_config(cls, config: dict, path: str|Path) -> None:
        from mmengine.config import Config
        if isinstance(path, Path):
            path = str(path)

        cfg = Config(config)
        cfg.dump(path)
