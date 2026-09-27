"""
SessionStorage helpers for Playwright UI tests.

Why page.context.cookies() does NOT capture sessionStorage
----------------------------------------------------------
Cookies and sessionStorage are different browser storage mechanisms:

- Cookies are HTTP header state managed by the browser and exposed via the
  CookieStore / Playwright's context.cookies() API. They are sent with
  matching network requests.
- sessionStorage is a per-origin, per-tab Web Storage API that lives only in
  the page's JavaScript heap. It is never attached to HTTP requests and is
  not part of the cookie jar.

Therefore context.cookies() can never return sessionStorage keys. Capture
those values with page.evaluate() against window.sessionStorage instead.

Note: SauceDemo currently stores cart IDs in localStorage ('cart-contents').
These helpers intentionally target sessionStorage as required by the
assignment; tests may mirror application state into sessionStorage for demos.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from playwright.sync_api import Page

from utils.json_utils import TESTDATA_DIR
from utils.logger import get_logger, log_data, log_step

logger = get_logger("session_storage")

DEFAULT_SESSION_FILE = TESTDATA_DIR / "session_data.json"


def write_session_item(page: Page, key: str, value: str) -> None:
    """Writes a single key/value pair into page sessionStorage."""
    log_step(logger, f"Writing sessionStorage key: {key}")
    page.evaluate(
        """([storageKey, storageValue]) => {
            sessionStorage.setItem(storageKey, storageValue);
        }""",
        [key, value],
    )


def read_session_item(page: Page, key: str) -> str | None:
    """Reads one sessionStorage value by key. Returns None if missing."""
    log_step(logger, f"Reading sessionStorage key: {key}")
    return page.evaluate(
        """(storageKey) => sessionStorage.getItem(storageKey)""",
        key,
    )


def read_all_session_storage(page: Page) -> dict[str, str]:
    """Returns the full sessionStorage map for the current origin."""
    log_step(logger, "Reading all sessionStorage entries")
    data = page.evaluate(
        """() => Object.fromEntries(Object.entries(sessionStorage))"""
    )
    log_data(logger, {"session_keys": list(data.keys())})
    return data


def clear_session_storage(page: Page) -> None:
    """Clears all sessionStorage entries for the current origin."""
    log_step(logger, "Clearing sessionStorage")
    page.evaluate("""() => sessionStorage.clear()""")


def save_session_storage(
    page: Page, file_path: str | os.PathLike[str] = DEFAULT_SESSION_FILE
) -> dict[str, str]:
    """Captures sessionStorage and persists it to a JSON file."""
    data = read_all_session_storage(page)
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
    log_step(logger, f"Saved sessionStorage to {path}")
    return data


def restore_session_storage(
    page: Page, file_path: str | os.PathLike[str] = DEFAULT_SESSION_FILE
) -> dict[str, str]:
    """Loads sessionStorage values from JSON and writes them into the page."""
    path = Path(file_path)
    with path.open("r", encoding="utf-8") as handle:
        data: dict[str, Any] = json.load(handle)

    log_step(logger, f"Restoring sessionStorage from {path}")
    page.evaluate(
        """(entries) => {
            sessionStorage.clear();
            for (const [key, value] of Object.entries(entries)) {
                sessionStorage.setItem(key, String(value));
            }
        }""",
        data,
    )
    return {str(key): str(value) for key, value in data.items()}


def validate_session_storage(page: Page, expected: dict[str, str]) -> bool:
    """
    Validates that current sessionStorage contains all expected key/value pairs.
    Returns True when every expected entry matches exactly.
    """
    actual = read_all_session_storage(page)
    log_step(logger, "Validating sessionStorage against expected data")
    for key, value in expected.items():
        if actual.get(key) != value:
            log_data(
                logger,
                {
                    "mismatch_key": key,
                    "expected": value,
                    "actual": actual.get(key),
                },
            )
            return False
    return True
