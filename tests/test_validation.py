import importlib
import sys
import types


def _get_validator():
    epd_module = types.ModuleType("waveshare_epd")
    epd7_module = types.ModuleType("waveshare_epd.epd7in3f")
    epd7_module.EPD = object
    sys.modules["waveshare_epd"] = epd_module
    sys.modules["waveshare_epd.epd7in3f"] = epd7_module
    epd_module.epd7in3f = epd7_module
    import dashboard

    importlib.reload(dashboard)
    return dashboard._validate_words


def test_duplicate_tags():
    validator = _get_validator()
    cleaned, error = validator({"tag": [{"name": "A"}, {"name": "a"}]}, "tag")
    assert error == "Duplicate tags"
    assert cleaned is None


def test_invalid_payload():
    validator = _get_validator()
    cleaned, error = validator({"invalid": []}, "tag")
    assert error == "Invalid payload"
    assert cleaned is None
