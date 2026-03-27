from typing import Any, Optional, Callable, Hashable

class RecursiveContext:    
    # 파이썬 자료 구조 (dict, list, tuple) 를 순회하며 작업하는 context 제공

    IsTargetType = Callable[[Any, Optional[Hashable], Optional[int]], bool] # (data, key, index) -> bool
    ReplacementType = Callable[[Any, Optional[Hashable], Optional[int]], Any] # (data, key, index) -> Any
    KeyType = Optional[Hashable]
    ValueType = Any

    @classmethod
    def replace(cls, 
        data:ValueType, 
        is_target:IsTargetType, 
        replacement:ReplacementType,
        k:KeyType = None,           # key
        idx:Optional[int] = None,
        depth:int = 0,
        d_limit:Optional[int] = None
    )->ValueType:

        if d_limit is not None and depth > d_limit:
            return data
        
        if is_target(data, k, idx):
            return replacement(data, k, idx)
        
        if isinstance(data, dict):
            for k, v in data.items():
                data[k] = cls.replace(v, is_target, replacement, k=k, depth = depth + 1, d_limit=d_limit)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                data[i] = cls.replace(item, is_target, replacement, idx=i, depth = depth + 1, d_limit=d_limit)
        elif isinstance(data, tuple):
            data = tuple(cls.replace(item, is_target, replacement, idx=i, depth = depth + 1, d_limit=d_limit) for i, item in enumerate(data))
        return data

    @classmethod
    def filter(cls, 
        data:ValueType, 
        is_remove_target:IsTargetType, 
        k:KeyType = None,           # key
        idx:Optional[int] = None,
        depth:int = 0,
        d_limit:Optional[int] = None
    )->ValueType:
        
        if d_limit is not None and depth > d_limit:
            return data
        
        if isinstance(data, dict):
            return {k: cls.filter(v, is_remove_target, k=k, depth = depth + 1, d_limit=d_limit) for k, v in data.items() if not is_remove_target(v, k, None)}
        elif isinstance(data, list):
            return [cls.filter(item, is_remove_target, idx=i, depth = depth + 1, d_limit=d_limit) for i, item in enumerate(data) if not is_remove_target(item, None, i)]
        else:
            return data
