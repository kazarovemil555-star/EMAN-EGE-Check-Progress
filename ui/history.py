import flet as ft

from data import basic_math_grade, is_basic_math
from ui.charts import build_progress_section
from ui.theme import (
    BRAND_CARD,
    BRAND_CYAN,
    BRAND_CYAN_SOFT,
    BRAND_MUTED,
    BRAND_SILVER,
    BRAND_SURFACE_2,
    section_title,
)


def _result_control(subject: str, score: int):
    if is_basic_math(subject):
        grade = basic_math_grade(score)

        return ft.Column(
            controls=[
                ft.Text(
                    f"{score} баллов",
                    weight=ft.FontWeight.BOLD,
                    color=BRAND_CYAN_SOFT,
                    size=16,
                ),
                ft.Container(
                    content=ft.Text(
                        f"Оценка {grade}",
                        size=11,
                        weight=ft.FontWeight.BOLD,
                        color=BRAND_SILVER,
                    ),
                    padding=ft.Padding.symmetric(
                        horizontal=9,
                        vertical=4,
                    ),
                    border_radius=8,
                    bgcolor=ft.Colors.with_opacity(0.12, BRAND_CYAN),
                ),
            ],
            spacing=5,
        )

    return ft.Text(
        f"{score} баллов",
        weight=ft.FontWeight.BOLD,
        color=BRAND_CYAN_SOFT,
        size=16,
    )


def build_history_content(
    subject: str,
    subject_tests: list[dict],
    on_edit,
    on_delete,
):
    controls = [
        build_progress_section(subject, subject_tests),
        section_title(
            "История пробников",
            (
                "В базовой математике рядом с баллом автоматически показывается оценка."
                if is_basic_math(subject)
                else "Все результаты выбранного предмета в одном месте."
            ),
        ),
    ]

    if not subject_tests:
        controls.append(
            ft.Container(
                content=ft.Text(
                    "Пробников пока нет.",
                    color=BRAND_MUTED,
                ),
                padding=16,
                border_radius=14,
                bgcolor=BRAND_SURFACE_2,
                border=ft.Border.all(
                    1,
                    ft.Colors.with_opacity(0.18, BRAND_CYAN),
                ),
            )
        )
        return controls

    for number, test in enumerate(subject_tests, start=1):
        score = int(test["score"])

        controls.append(
            ft.Container(
                content=ft.ResponsiveRow(
                    controls=[
                        ft.Container(
                            content=ft.Text(
                                f"{number:02d}",
                                size=13,
                                weight=ft.FontWeight.BOLD,
                                color=BRAND_CYAN,
                            ),
                            width=42,
                            height=42,
                            alignment=ft.Alignment.CENTER,
                            border_radius=12,
                            bgcolor=ft.Colors.with_opacity(0.11, BRAND_CYAN),
                            border=ft.Border.all(
                                1,
                                ft.Colors.with_opacity(0.25, BRAND_CYAN),
                            ),
                            col={"xs": 2, "sm": 1},
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        str(test["date"]),
                                        color=BRAND_SILVER,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(
                                        "Дата пробника",
                                        size=11,
                                        color=BRAND_MUTED,
                                    ),
                                ],
                                spacing=2,
                            ),
                            col={"xs": 10, "sm": 5},
                        ),
                        ft.Container(
                            content=_result_control(subject, score),
                            col={"xs": 8, "sm": 3},
                        ),
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        icon_color=BRAND_CYAN_SOFT,
                                        tooltip="Редактировать пробник",
                                        data=test["id"],
                                        on_click=on_edit,
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINE,
                                        icon_color=BRAND_MUTED,
                                        tooltip="Удалить пробник",
                                        data=test["id"],
                                        on_click=on_delete,
                                    ),
                                ],
                                spacing=2,
                                alignment=ft.MainAxisAlignment.END,
                            ),
                            col={"xs": 4, "sm": 3},
                        ),
                    ],
                    spacing=8,
                    run_spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=12,
                border_radius=16,
                bgcolor=BRAND_CARD,
                border=ft.Border.all(
                    1,
                    ft.Colors.with_opacity(0.13, BRAND_CYAN),
                ),
            )
        )

    return controls
