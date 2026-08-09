from datetime import datetime
from uuid import uuid4

from config import BASIC_MATH_NAME


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
    tests[:] = [
        test
        for test in tests
        if test.get("id") != test_id
    ]


def _date_key(test: dict):
    try:
        return datetime.strptime(
            str(test.get("date", "")),
            DATE_FORMAT,
        )
    except ValueError:
        return datetime.min


def get_subject_tests(
    tests: list[dict],
    subject: str,
) -> list[dict]:
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


def is_basic_math(subject: str) -> bool:
    return subject == BASIC_MATH_NAME


def score_max_for_subject(subject: str) -> int:
    return 21 if is_basic_math(subject) else 100


def score_range_text(subject: str) -> str:
    maximum = score_max_for_subject(subject)
    return f"От 0 до {maximum}"


def basic_math_grade(score: int) -> int | None:
    score = int(score)

    if 0 <= score <= 6:
        return 2
    if 7 <= score <= 11:
        return 3
    if 12 <= score <= 16:
        return 4
    if 17 <= score <= 21:
        return 5

    return None


def format_result(subject: str, score: int) -> str:
    score = int(score)

    if is_basic_math(subject):
        grade = basic_math_grade(score)
        if grade is not None:
            return f"{score} баллов • оценка {grade}"

    return f"{score} баллов"


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
