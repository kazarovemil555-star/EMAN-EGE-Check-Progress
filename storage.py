import json

import flet as ft

from config import STORAGE_KEY, SUBJECT_NAMES_KEY


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


async def load_subject_names(
    storage: ft.SharedPreferences,
    defaults: list[str],
) -> list[str]:
    saved_subjects = await storage.get(SUBJECT_NAMES_KEY)

    if not saved_subjects:
        return list(defaults)

    try:
        subjects = json.loads(saved_subjects)
    except (json.JSONDecodeError, TypeError):
        return list(defaults)

    if not isinstance(subjects, list) or len(subjects) != len(defaults):
        return list(defaults)

    result = list(defaults)

    # Первые два предмета фиксированы.
    result[0] = defaults[0]
    result[1] = defaults[1]

    # Третий и четвёртый пользователь может переименовать.
    for index in (2, 3):
        value = subjects[index]
        if isinstance(value, str) and value.strip():
            result[index] = value.strip()

    return result


async def save_subject_names(
    storage: ft.SharedPreferences,
    subjects: list[str],
) -> None:
    await storage.set(
        SUBJECT_NAMES_KEY,
        json.dumps(subjects, ensure_ascii=False),
    )
