from typing import Any

class EmptyTag:
    def __init__(self, value:Any)->None:
        self.value = value

    def __repr__(self)->str:
        return self.value

    def __eq__(self, other:Any)->bool:
        if not isinstance(other, EmptyTag):
            return False
        return self.value == other.value

EMPTY_TAG = EmptyTag("EmptyTag")
# EMPTY_TAG = "WillBeOverridden"