from pathlib import Path as _Path

from dataclasses import dataclass as _dataclass
from dataclasses import asdict as _asdict
from dataclasses import field as _field
from cfgfw.empty_tag import EMPTY_TAG as _EMPTY_TAG
from cfgfw.empty_tag import EmptyTag as _EmptyTag

@_dataclass
class _HyperParams:
    epoch:int|_EmptyTag = _field(default_factory=lambda: _EMPTY_TAG, )
    log_step:int|_EmptyTag = _field(default_factory=lambda: _EMPTY_TAG, )


hyper_params = _asdict(_HyperParams(epoch=10, log_step=10))
