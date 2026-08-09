from datetime import datetime
from uuid import uuid4


DATE_FORMAT = "%d.%m.%Y"


def ensure_test_ids(tests: list[dict]) -> bool:
    changed = False

    for test in tests:
        if not test.get("id"):
            test["id"] = uuid4().hex
            changed = True

    return changed


def create_test(subject: str, date: str, score: int) -> dict:
    return {
        "id": uuid4().hex,
        "subject": subject,
        "date": date,
        "score": score,
    }


def find_test_by_id(tests: list[dict], test_id: str) -> dict | None:
    for test in tests:
        if test.get("id") == test_id:
            return test

    return None


def update_test(test: dict, date: str, score: int) -> None:
    test["date"] = date
    test["score"] = score


def delete_test(tests: list[dict], test_id: str) -> None:
    tests[:] = [test for test in tests if test.get("id") != test_id]


def _date_key(test: dict):
    try:
        return datetime.strptime(str(test.get("date", "")), DATE_FORMAT)
    except ValueError:
        return datetime.min


def get_subject_tests(tests: list[dict], subject: str) -> list[dict]:
    subject_tests = [
        test
        for test in tests
        if test.get("subject") == subject
    ]

    return sorted(subject_tests, key=_date_key)


def validate_date(date_text: str) -> bool:
    try:
        datetime.strptime(date_text, DATE_FORMAT)
        return True
    except ValueError:
        return False


def calculate_statistics(subject_tests: list[dict]) -> dict:
    if not subject_tests:
        return {
            "average": None,
            "best": None,
            "change": None,
        }

    scores = [int(test["score"]) for test in subject_tests]

    return {
        "average": round(sum(scores) / len(scores), 1),
        "best": max(scores),
        "change": scores[-1] - scores[0],
    }
