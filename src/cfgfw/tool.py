import runpy
from pathlib import Path
from typing import Any, Callable
from copy import deepcopy
from abc import ABC, abstractmethod



class DictTool:
    def __init__(self, empty_tag: Any)->None:
        self.empty_tag = empty_tag

    def filter_temp_values(
        self, 
        data:Any, 
        is_target:Callable[[str], bool], 
        recursive:bool = True,
        depth:int = 0
        )->dict:

        # data를 순회하며 is_target 함수를 만족하지 않는 값들을 제거
        
        if recursive == False and depth > 0:
            return data
        
        if isinstance(data, dict):
            new_cfg = {}

            for k, v in data.items():
            # remove temp keys starting with a single underscore; keep double-underscore keys
                if is_target(k):
                    continue
            
                new_cfg[k] = self.filter_temp_values(v, is_target, recursive, depth + 1)

            return new_cfg
        elif isinstance(data, list):
            return [self.filter_temp_values(item, is_target, recursive, depth + 1) for item in data]
        else:
            return data



    def merge_config(self, base: dict, override: dict, empty_tag: Any=None) -> dict:
        empty_tag = empty_tag or self.empty_tag

        for key, value in override.items():
            if value is empty_tag:
                continue

            
            if isinstance(value, dict) and value.get('__delete__', False):
                new_val = deepcopy(value)
                new_val.pop('__delete__', None)
                base[key] = new_val
                continue

            if key not in base:
                base[key] = deepcopy(value)
                continue

            if isinstance(value, dict) and isinstance(base.get(key), dict):
                self.merge_config(base[key], value, empty_tag)
                continue

            if isinstance(value, list) and isinstance(base.get(key), list):
                base[key] = deepcopy(value)
                continue

            base[key] = deepcopy(value)
        return base
    

    def merge(self, configs:list[dict])->dict:
        
        cfg = {}
        for config in configs:
            try:
                cfg = self.merge_config(cfg, config)
            except Exception as e:
                print(e)
                print(config)
                exit()
        return cfg


    def get(self, data:dict, keys:list[str])->Any:
        try:
            for key in keys:
                data = data[key]
            return data
        except Exception as e:
            print(e)
            print(keys)
            exit()
    

    def set(self, data:dict, keys:list[str], value:Any)->None:
        for key in keys[:-1]:
            data = data[key]
        data[keys[-1]] = value