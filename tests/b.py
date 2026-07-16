from dataclasses import dataclass as _dataclass
from dataclasses import asdict as _asdict
from dataclasses import field as _field
from cfgfw.empty_tag import EMPTY_TAG as _EMPTY_TAG
from cfgfw.empty_tag import EmptyTag as _EmptyTag

@_dataclass
class _HyperParams:
    epoch:int|_EmptyTag = _field(default_factory=lambda: _EMPTY_TAG, )
    log_step:int|_EmptyTag = _field(default_factory=lambda: _EMPTY_TAG, )


from cfgfw.elements.base import File as _File
from cfgfw.elements.base import Base as _Base
from cfgfw.elements.base import Ref as _Ref

_Base(_File(f"{__file__}/../a.py"))
hyper_params = _asdict(_HyperParams(epoch=100))
a = _Ref("hyper_params.epoch")

