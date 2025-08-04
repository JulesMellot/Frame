import frame.deviantart  # noqa: F401
import frame.plex  # noqa: F401
import frame.fixed_download  # noqa: F401
from frame.plugins import PLUGINS


def test_builtin_plugins_registered():
    assert {"deviantart", "plex", "fixed"} <= set(PLUGINS)
