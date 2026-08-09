import flet as ft

from ui.charts import build_progress_section
from ui.theme import (
    BRAND_CARD,
    BRAND_CYAN,
    BRAND_CYAN_SOFT,
    BRAND_MUTED,
    BRAND_SILVER,
    BRAND_SURFACE_2,
    CARD_BORDER,
    section_title,
)


def build_history_content(
    subject_tests: list[dict],
    on_edit,
    on_delete,
):
    controls = [
        build_progress_section(subject_tests),
        section_title(
            "История пробников",
            "Все результаты выбранного предмета в одном месте.",
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
                border=ft.Border.all(1, ft.Colors.with_opacity(0.18, BRAND_CYAN)),
            )
        )
        return controls

    for number, test in enumerate(subject_tests, start=1):
        controls.append(
            ft.Container(
                content=ft.Row(
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
                            border=ft.Border.all(1, ft.Colors.with_opacity(0.25, BRAND_CYAN)),
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    str(test["date"]),
                                    color=BRAND_SILVER,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text("Дата пробника", size=11, color=BRAND_MUTED),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ft.Text(
                            value=f"{test['score']} баллов",
                            weight=ft.FontWeight.BOLD,
                            color=BRAND_CYAN_SOFT,
                            size=16,
                        ),
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
                    spacing=10,
                ),
                padding=12,
                border_radius=16,
                bgcolor=BRAND_CARD,
                border=ft.Border.all(1, ft.Colors.with_opacity(0.13, BRAND_CYAN)),
            )
        )

    return controls
