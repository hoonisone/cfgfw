from pathlib import Path as _Path

_base = (
    f"@file_cfg:{_Path(__file__).parent / 'b.py'}",

)


a = 1

c = f"@file_cfg:{_Path(__file__).parent / 'c.py'}"

A = f"@val:a"