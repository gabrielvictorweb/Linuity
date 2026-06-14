import json
import logging
import os
import time
import urllib.request

logger = logging.getLogger(__name__)

TAGS_URL = "https://api.github.com/repos/gabrielvictorweb/linuity/tags"
CACHE_PATH = os.path.expanduser("~/.cache/linuity/latest_version")
CACHE_TTL = 24 * 60 * 60


def check_for_update(current):
    """Return the latest version string if newer than current, else None.

    Never raises: network errors, rate limits and malformed data are
    swallowed so an update check can never break the tool.
    """
    latest = _read_cache()
    if latest is None:
        try:
            latest = _fetch_latest() or ""
        except Exception as e:
            logger.debug("Update check failed: %s", e)
            return None
        _write_cache(latest)

    current_parts = _parse(current)
    latest_parts = _parse(latest)
    if current_parts and latest_parts and latest_parts > current_parts:
        return latest.lstrip("v")
    return None


def _parse(version):
    try:
        return tuple(int(part) for part in version.lstrip("v").split("."))
    except (ValueError, AttributeError):
        return None


def _fetch_latest():
    request = urllib.request.Request(TAGS_URL, headers={"Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(request, timeout=2) as response:
        tags = json.load(response)
    versions = [tag["name"] for tag in tags if _parse(tag.get("name"))]
    if not versions:
        return None
    return max(versions, key=_parse)


def _read_cache():
    try:
        if time.time() - os.path.getmtime(CACHE_PATH) < CACHE_TTL:
            with open(CACHE_PATH) as f:
                return f.read().strip()
    except OSError:
        pass
    return None


def _write_cache(latest):
    try:
        os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
        with open(CACHE_PATH, "w") as f:
            f.write(latest)
    except OSError as e:
        logger.debug("Could not write update cache: %s", e)
