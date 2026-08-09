import math

import flet as ft
import flet_charts as fch

from data import calculate_statistics


GRID_COLOR = ft.Colors.with_opacity(0.18, ft.Colors.ON_SURFACE)
CHART_BORDER_COLOR = ft.Colors.with_opacity(0.28, ft.Colors.ON_SURFACE)
CHART_BG = ft.Colors.with_opacity(0.28, ft.Colors.BLUE_GREY_900)


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
            ),
        )
        for index in indexes
    ]


def build_progress_section(subject_tests: list[dict]):
    if not subject_tests:
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "График прогресса",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        "Для графика пока нет данных.",
                        color=ft.Colors.GREY_400,
                    ),
                ],
                spacing=8,
            ),
            padding=18,
            border_radius=14,
            border=ft.Border.all(1, CHART_BORDER_COLOR),
            bgcolor=CHART_BG,
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
        color=ft.Colors.CYAN,
    )
    line.point = True

    chart = fch.LineChart(
        data_series=[line],
        min_x=0,
        max_x=max(2, len(subject_tests) + 1),
        min_y=0,
        max_y=100,
        height=300,
        interactive=True,
        bgcolor=ft.Colors.TRANSPARENT,
        # Flet clips interval grid lines at the outer bounds, so the top and
        # bottom chart borders intentionally duplicate the 0 and 100 lines.
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
            color=ft.Colors.with_opacity(0.08, ft.Colors.ON_SURFACE),
            width=1,
        ),
        left_axis=fch.ChartAxis(
            label_size=38,
            labels=[
                fch.ChartAxisLabel(value=value, label=ft.Text(str(value), size=11))
                for value in (0, 20, 40, 60, 80, 100)
            ],
        ),
        bottom_axis=fch.ChartAxis(
            label_size=34,
            labels=_bottom_axis_labels(subject_tests),
        ),
        tooltip=fch.LineChartTooltip(
            bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.BLUE_GREY_800)
        ),
    )

    stats = calculate_statistics(subject_tests)
    change = stats["change"]
    change_text = f"{change:+d}" if change is not None else "—"

    stats_text = ft.Text(
        value=(
            f"Средний балл: {stats['average']}   •   "
            f"Лучший: {stats['best']}   •   "
            f"Изменение: {change_text}"
        ),
        size=14,
        color=ft.Colors.GREY_300,
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "График прогресса",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
                stats_text,
                chart,
            ],
            spacing=10,
        ),
        padding=18,
        border_radius=14,
        border=ft.Border.all(1, CHART_BORDER_COLOR),
        bgcolor=CHART_BG,
    )
