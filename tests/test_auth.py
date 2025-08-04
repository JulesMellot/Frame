import importlib
import json
import sys
import types
import pytest


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("API_TOKEN", "testtoken")
    epd_module = types.ModuleType("waveshare_epd")
    epd7_module = types.ModuleType("waveshare_epd.epd7in3f")
    epd7_module.EPD = object  # minimal stub
    sys.modules["waveshare_epd"] = epd_module
    sys.modules["waveshare_epd.epd7in3f"] = epd7_module
    epd_module.epd7in3f = epd7_module
    import frame.config as config

    importlib.reload(config)
    import dashboard

    importlib.reload(dashboard)
    monkeypatch.setattr(dashboard, "WEB_DIR", tmp_path)
    dashboard.app.static_folder = str(tmp_path)
    for name, content in [("tags.json", "[]"), ("bantag.json", "[]"), ("function.json", "{}")]:
        (tmp_path / name).write_text(content)
    return dashboard.app.test_client()


def test_auth_required(client):
    resp = client.post("/api/tags", json={"tag": [{"name": "foo"}]})
    assert resp.status_code == 401


def test_auth_success(client):
    headers = {"Authorization": "Bearer testtoken"}
    payload = {"tag": [{"name": "foo"}]}
    resp = client.post("/api/tags", json=payload, headers=headers)
    assert resp.status_code == 200
    assert resp.get_json()["success"] is True
