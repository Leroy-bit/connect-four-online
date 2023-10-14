import typing

if typing.TYPE_CHECKING:
    from explorer import Explorer

class BaseEntity:
    '''
    Base class for all entities.

    Attributes:
        explorer: Explorer instance.

    '''

    def __init__(self, explorer: 'Explorer'):
        self.explorer = explorer
        self._init_()

    def _init_(self) -> None:
        return None
