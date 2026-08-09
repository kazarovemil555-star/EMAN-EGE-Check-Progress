import json

import flet as ft

from config import STORAGE_KEY


async def load_tests(storage: ft.SharedPreferences) -> list[dict]:
    saved_tests = await storage.get(STORAGE_KEY)

    if not saved_tests:
        return []

    try:
        tests = json.loads(saved_tests)
    except (json.JSONDecodeError, TypeError):
        return []

    if not isinstance(tests, list):
        return []

    return [test for test in tests if isinstance(test, dict)]


async def save_tests(storage: ft.SharedPreferences, tests: list[dict]) -> None:
    tests_json = json.dumps(tests, ensure_ascii=False)
    await storage.set(STORAGE_KEY, tests_json)
