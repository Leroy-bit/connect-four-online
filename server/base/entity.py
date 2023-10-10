import typing

if typing.TYPE_CHECKING:
    from explorer import Explorer

class BaseEntity:

    def __init__(self, explorer: 'Explorer'):
        self.explorer = explorer
        self._init_()

    def _init_(self) -> None:
        return None
