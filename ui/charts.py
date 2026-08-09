import math

import flet as ft
import flet_charts as fch

from data import calculate_statistics
from ui.theme import (
    BRAND_BG,
    BRAND_CARD,
    BRAND_CYAN,
    BRAND_CYAN_SOFT,
    BRAND_LINE,
    BRAND_MUTED,
    BRAND_SILVER,
    CARD_BORDER,
    CHART_GRADIENT,
    SOFT_CYAN,
    section_title,
)


GRID_COLOR = ft.Colors.with_opacity(0.20, BRAND_SILVER)
VERTICAL_GRID_COLOR = ft.Colors.with_opacity(0.07, BRAND_SILVER)


def _date_label(date_text: str) -> str:
    if len(date_text) >= 5:
        return date_text[:5]
    return date_text


def _bottom_axis_labels(subject_tests: list[dict]) -> list:
    count = len(subject_tests)
    if count == 0:
        return []

    step = max(1, math.ceil(count / 6))
    indexes = list(range(1, count + 1, step))
    if indexes[-1] != count:
        indexes.append(count)

    return [
        fch.ChartAxisLabel(
            value=index,
            label=ft.Text(
                _date_label(str(subject_tests[index - 1]["date"])),
                size=11,
                color=BRAND_MUTED,
            ),
        )
        for index in indexes
    ]


def _stat_chip(title: str, value: str):
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(title, size=11, color=BRAND_MUTED),
                ft.Text(
                    value,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=BRAND_SILVER,
                ),
            ],
            spacing=2,
        ),
        padding=ft.Padding.symmetric(horizontal=14, vertical=10),
        border_radius=12,
        bgcolor=ft.Colors.with_opacity(0.08, BRAND_CYAN),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.20, BRAND_CYAN)),
    )


def build_progress_section(subject_tests: list[dict]):
    if not subject_tests:
        return ft.Container(
            content=ft.Column(
                controls=[
                    section_title("График прогресса"),
                    ft.Container(
                        content=ft.Text(
                            "Добавь первый пробник — здесь появится динамика результатов.",
                            color=BRAND_MUTED,
                        ),
                        padding=18,
                        border_radius=14,
                        bgcolor=ft.Colors.with_opacity(0.06, BRAND_CYAN),
                        border=ft.Border.all(1, ft.Colors.with_opacity(0.14, BRAND_CYAN)),
                    ),
                ],
                spacing=12,
            ),
            padding=20,
            border_radius=20,
            border=ft.Border.all(1, CARD_BORDER),
            gradient=CHART_GRADIENT,
        )

    points = [
        fch.LineChartDataPoint(index, int(test["score"]))
        for index, test in enumerate(subject_tests, start=1)
    ]

    line = fch.LineChartData(
        points=points,
        stroke_width=4,
        curved=False,
        rounded_stroke_cap=True,
        color=BRAND_CYAN,
    )
    line.point = True

    chart = fch.LineChart(
        data_series=[line],
        min_x=0,
        max_x=max(2, len(subject_tests) + 1),
        min_y=0,
        max_y=100,
        height=310,
        interactive=True,
        bgcolor=ft.Colors.TRANSPARENT,
        # Outer borders duplicate the interval grid at 0 and 100 so all
        # horizontal levels are equally visible.
        border=ft.Border.only(
            top=ft.BorderSide(1, GRID_COLOR),
            bottom=ft.BorderSide(1, GRID_COLOR),
        ),
        horizontal_grid_lines=fch.ChartGridLines(
            interval=20,
            color=GRID_COLOR,
            width=1,
        ),
        vertical_grid_lines=fch.ChartGridLines(
            interval=1,
            color=VERTICAL_GRID_COLOR,
            width=1,
        ),
        left_axis=fch.ChartAxis(
            label_size=38,
            labels=[
                fch.ChartAxisLabel(
                    value=value,
                    label=ft.Text(str(value), size=11, color=BRAND_MUTED),
                )
                for value in (0, 20, 40, 60, 80, 100)
            ],
        ),
        bottom_axis=fch.ChartAxis(
            label_size=34,
            labels=_bottom_axis_labels(subject_tests),
        ),
        tooltip=fch.LineChartTooltip(
            bgcolor=ft.Colors.with_opacity(0.94, BRAND_CARD)
        ),
    )

    stats = calculate_statistics(subject_tests)
    change = stats["change"]
    change_text = f"{change:+d}" if change is not None else "—"

    return ft.Container(
        content=ft.Column(
            controls=[
                section_title(
                    "График прогресса",
                    "Динамика баллов по сохранённым пробникам.",
                ),
                ft.Row(
                    controls=[
                        _stat_chip("Средний", str(stats["average"])),
                        _stat_chip("Лучший", str(stats["best"])),
                        _stat_chip("Изменение", change_text),
                    ],
                    spacing=10,
                    wrap=True,
                ),
                ft.Container(
                    content=chart,
                    padding=16,
                    border_radius=16,
                    bgcolor=ft.Colors.with_opacity(0.35, BRAND_BG),
                    border=ft.Border.all(1, ft.Colors.with_opacity(0.18, BRAND_CYAN)),
                ),
            ],
            spacing=14,
        ),
        padding=20,
        border_radius=20,
        border=ft.Border.all(1, CARD_BORDER),
        gradient=CHART_GRADIENT,
    )
