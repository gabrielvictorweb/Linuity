import io
import json

from linuity.infra import update_checker


def _use_tmp_cache(monkeypatch, tmp_path):
    monkeypatch.setattr(update_checker, "CACHE_PATH", str(tmp_path / "latest_version"))


def test_parse_versions():
    assert update_checker._parse("v0.4.0") == (0, 4, 0)
    assert update_checker._parse("1.2.3") == (1, 2, 3)
    assert update_checker._parse("not-a-version") is None
    assert update_checker._parse(None) is None


def test_check_returns_newer_version(monkeypatch, tmp_path):
    _use_tmp_cache(monkeypatch, tmp_path)
    monkeypatch.setattr(update_checker, "_fetch_latest", lambda: "v0.5.0")

    assert update_checker.check_for_update("0.4.0") == "0.5.0"


def test_check_returns_none_when_up_to_date(monkeypatch, tmp_path):
    _use_tmp_cache(monkeypatch, tmp_path)
    monkeypatch.setattr(update_checker, "_fetch_latest", lambda: "v0.4.0")

    assert update_checker.check_for_update("0.4.0") is None


def test_check_swallows_fetch_errors(monkeypatch, tmp_path):
    _use_tmp_cache(monkeypatch, tmp_path)

    def boom():
        raise OSError("network down")

    monkeypatch.setattr(update_checker, "_fetch_latest", boom)

    assert update_checker.check_for_update("0.4.0") is None


def test_check_uses_fresh_cache_without_fetching(monkeypatch, tmp_path):
    _use_tmp_cache(monkeypatch, tmp_path)
    (tmp_path / "latest_version").write_text("v9.9.9")

    def boom():
        raise AssertionError("should not fetch when cache is fresh")

    monkeypatch.setattr(update_checker, "_fetch_latest", boom)

    assert update_checker.check_for_update("0.4.0") == "9.9.9"


def test_check_refetches_when_cache_expired(monkeypatch, tmp_path):
    _use_tmp_cache(monkeypatch, tmp_path)
    cache = tmp_path / "latest_version"
    cache.write_text("v9.9.9")
    monkeypatch.setattr(update_checker, "CACHE_TTL", -1)
    monkeypatch.setattr(update_checker, "_fetch_latest", lambda: "v0.5.0")

    assert update_checker.check_for_update("0.4.0") == "0.5.0"
    assert cache.read_text() == "v0.5.0"


def test_check_caches_empty_result(monkeypatch, tmp_path):
    _use_tmp_cache(monkeypatch, tmp_path)
    monkeypatch.setattr(update_checker, "_fetch_latest", lambda: None)

    assert update_checker.check_for_update("0.4.0") is None
    assert (tmp_path / "latest_version").read_text() == ""


def test_fetch_latest_picks_highest_tag(monkeypatch):
    payload = [{"name": "v0.3.2"}, {"name": "v0.10.0"}, {"name": "junk"}, {}]

    def fake_urlopen(request, timeout):
        return io.BytesIO(json.dumps(payload).encode())

    monkeypatch.setattr(update_checker.urllib.request, "urlopen", fake_urlopen)

    assert update_checker._fetch_latest() == "v0.10.0"


def test_fetch_latest_returns_none_without_valid_tags(monkeypatch):
    def fake_urlopen(request, timeout):
        return io.BytesIO(b"[]")

    monkeypatch.setattr(update_checker.urllib.request, "urlopen", fake_urlopen)

    assert update_checker._fetch_latest() is None


def test_write_cache_ignores_os_errors(monkeypatch):
    monkeypatch.setattr(update_checker, "CACHE_PATH", "/proc/forbidden/latest_version")

    update_checker._write_cache("v1.0.0")
