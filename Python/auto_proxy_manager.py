from typing import Dict


class AutoProxyManager(object):
    def __init__(self) -> None:
        self._allowed_types = (object,)
        self._properties: Dict[str, object] = {}

    def _register(self, name: str, obj: object):
        if name in self._properties:
            raise ValueError(f'{name} already registered!')
        if not any(map(lambda T: isinstance(obj, T), self._allowed_types)):
            raise ValueError(f'Type `{obj.__class__.__name__}` is not allowed. Accepted types: '
                             f'{", ".join(map(lambda T: T.__name__, self._allowed_types))}')
        self._properties[name] = obj
        exec(f'self.{name} = obj')

    def __getattr__(self, attr: str):
        """__getattr__ will be called after __getattribute__ if accessed attr is not found.
        This is an auto proxy implemented via the Python class attribute fallback mechanism.
        """
        if attr not in self._properties:
            raise AttributeError(f'Attribute `{attr}` is not found.')
        return self._properties[attr]
