def register_globals(values: dict, target_globals: dict | None = None, *, overwrite: bool = True) -> None:
    """
    dict의 key를 변수명으로, value를 값으로 전역 변수에 등록한다.

    Parameters
    ----------
    values:
        {"변수명": 값} 형태의 딕셔너리
    target_globals:
        보통 globals()를 넘기면 됨. 생략하면 이 함수가 정의된 모듈의 globals()에 등록됨.
    overwrite:
        이미 같은 이름의 전역 변수가 있을 때 덮어쓸지 여부
    """
    if target_globals is None:
        target_globals = globals()

    for name, value in values.items():
        if not isinstance(name, str):
            raise TypeError(f"global variable name must be str, got {type(name).__name__}: {name!r}")

        if not name.isidentifier():
            raise ValueError(f"invalid Python identifier: {name!r}")

        if name in {"False", "True", "None"}:
            raise ValueError(f"cannot assign to reserved constant: {name!r}")

        if not overwrite and name in target_globals:
            raise KeyError(f"global variable already exists: {name!r}")

        target_globals[name] = value


from ..factory import DefaultConfigManagerFactory
factory = DefaultConfigManagerFactory()
config_accessor = factory.config_accessor
# config_manager = factory.config_manager


# def Base(config:dict)->None:
#     register_globals(config)

from pathlib import Path
from typing import Any

def File(path:Path|str)->Any:
    return config_accessor.load_config(path)


import inspect

def Base(config: dict) -> None:

    frame = inspect.currentframe()
    assert frame is not None
    caller_frame = frame.f_back
    assert caller_frame is not None
    caller_frame.f_globals["_base"] = config
    # register_globals(config, caller_frame.f_globals)

def Ref(ref:str)->Any:
    return "@ref:" + ref
