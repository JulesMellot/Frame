"""Plugin registry for image sources."""
from typing import Callable, Dict

PLUGINS: Dict[str, Callable[[], bool]] = {}


def register_plugin(name: str, func: Callable[[], bool]) -> None:
    """Register a new image source plugin."""
    PLUGINS[name.lower()] = func


def get_plugin(name: str) -> Callable[[], bool] | None:
    """Retrieve a plugin by name."""
    return PLUGINS.get(name.lower())
