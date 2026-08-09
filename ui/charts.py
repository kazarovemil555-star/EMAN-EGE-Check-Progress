import math

import flet as ft
import flet_charts as fch

from data import (
    basic_math_grade,
    calculate_statistics,
    format_result,
    is_basic_math,
)
from ui.theme import (
    BRAND_BG,
    BRAND_CARD,
    BRAND_CYAN,
    BRAND_CYAN_SOFT,
    BRAND_MUTED,
    BRAND_SILVER,
    CARD_BORDER,
    CHART_GRADIENT,
    section_title,
)


GRID_COLOR = ft.Colors.with_opacity(0.20, BRAND_SILVER)
VERTICAL_GRID_COLOR = ft.Colors.with_opacity(0.07, BRAND_SILVER)
THRESHOLD_COLOR = ft.Colors.with_opacity(0.38, BRAND_CYAN_SOFT)


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
                ft.Text(
                    title,
                    size=11,
                    color=BRAND_MUTED,
                ),
                ft.Text(
                    value,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=BRAND_SILVER,
                ),
            ],
            spacing=2,
        ),
        padding=ft.Padding.symmetric(
            horizontal=14,
            vertical=10,
        ),
        border_radius=12,
        bgcolor=ft.Colors.with_opacity(0.08, BRAND_CYAN),
        border=ft.Border.all(
            1,
            ft.Colors.with_opacity(0.20, BRAND_CYAN),
        ),
    )


def _grade_chip(grade: int, score_range: str):
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(
                        str(grade),
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=BRAND_BG,
                    ),
                    width=34,
                    height=34,
                    alignment=ft.Alignment.CENTER,
                    border_radius=10,
                    bgcolor=BRAND_CYAN,
                ),
                ft.Column(
                    controls=[
                        ft.Text(
                            f"Оценка {grade}",
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color=BRAND_SILVER,
                        ),
                        ft.Text(
                            score_range,
                            size=11,
                            color=BRAND_MUTED,
                        ),
                    ],
                    spacing=1,
                ),
            ],
            spacing=8,
        ),
        padding=10,
        border_radius=12,
        bgcolor=ft.Colors.with_opacity(0.07, BRAND_CYAN),
        border=ft.Border.all(
            1,
            ft.Colors.with_opacity(0.16, BRAND_CYAN),
        ),
    )


def _basic_grade_scale():
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Шкала базовой математики",
                    size=13,
                    weight=ft.FontWeight.BOLD,
                    color=BRAND_CYAN_SOFT,
                ),
                ft.ResponsiveRow(
                    controls=[
                        ft.Container(
                            content=_grade_chip(2, "0–6 баллов"),
                            col={"xs": 6, "md": 3},
                        ),
                        ft.Container(
                            content=_grade_chip(3, "7–11 баллов"),
                            col={"xs": 6, "md": 3},
                        ),
                        ft.Container(
                            content=_grade_chip(4, "12–16 баллов"),
                            col={"xs": 6, "md": 3},
                        ),
                        ft.Container(
                            content=_grade_chip(5, "17–21 балл"),
                            col={"xs": 6, "md": 3},
                        ),
                    ],
                    spacing=8,
                    run_spacing=8,
                ),
            ],
            spacing=8,
        ),
        padding=12,
        border_radius=14,
        bgcolor=ft.Colors.with_opacity(0.22, BRAND_BG),
        border=ft.Border.all(
            1,
            ft.Colors.with_opacity(0.16, BRAND_CYAN),
        ),
    )


def _threshold_series(max_x: float):
    series = []

    # Начало диапазонов оценок 3, 4 и 5.
    for value in (7, 12, 17):
        p1 = fch.LineChartDataPoint(0, value)
        p2 = fch.LineChartDataPoint(max_x, value)
        p1.show_tooltip = False
        p2.show_tooltip = False

        series.append(
            fch.LineChartData(
                points=[p1, p2],
                stroke_width=1,
                curved=False,
                dash_pattern=[5, 6],
                color=THRESHOLD_COLOR,
                point=False,
            )
        )

    return series


def _make_result_points(
    subject: str,
    subject_tests: list[dict],
):
    points = []

    for index, test in enumerate(subject_tests, start=1):
        score = int(test["score"])
        point = fch.LineChartDataPoint(index, score)
        point.tooltip = fch.LineChartDataPointTooltip(
            text=format_result(subject, score),
        )
        points.append(point)

    return points


def build_progress_section(
    subject: str,
    subject_tests: list[dict],
):
    basic = is_basic_math(subject)

    if not subject_tests:
        empty_controls = [
            section_title("График прогресса"),
        ]

        if basic:
            empty_controls.append(_basic_grade_scale())

        empty_controls.append(
            ft.Container(
                content=ft.Text(
                    "Добавь первый пробник — здесь появится динамика результатов.",
                    color=BRAND_MUTED,
                ),
                padding=18,
                border_radius=14,
                bgcolor=ft.Colors.with_opacity(0.06, BRAND_CYAN),
                border=ft.Border.all(
                    1,
                    ft.Colors.with_opacity(0.14, BRAND_CYAN),
                ),
            )
        )

        return ft.Container(
            content=ft.Column(
                controls=empty_controls,
                spacing=12,
            ),
            padding=20,
            border_radius=20,
            border=ft.Border.all(1, CARD_BORDER),
            gradient=CHART_GRADIENT,
        )

    max_x = max(2, len(subject_tests) + 1)
    points = _make_result_points(subject, subject_tests)

    result_line = fch.LineChartData(
        points=points,
        stroke_width=4,
        curved=False,
        rounded_stroke_cap=True,
        color=BRAND_CYAN,
        point=True,
    )

    if basic:
        data_series = _threshold_series(max_x) + [result_line]
        max_y = 21
        grid_interval = 3
        left_values = (0, 3, 6, 9, 12, 15, 18, 21)

        right_axis = fch.ChartAxis(
            label_size=76,
            labels=[
                fch.ChartAxisLabel(
                    value=3,
                    label=ft.Text(
                        "оценка 2",
                        size=10,
                        color=BRAND_MUTED,
                    ),
                ),
                fch.ChartAxisLabel(
                    value=9,
                    label=ft.Text(
                        "оценка 3",
                        size=10,
                        color=BRAND_MUTED,
                    ),
                ),
                fch.ChartAxisLabel(
                    value=14,
                    label=ft.Text(
                        "оценка 4",
                        size=10,
                        color=BRAND_MUTED,
                    ),
                ),
                fch.ChartAxisLabel(
                    value=19,
                    label=ft.Text(
                        "оценка 5",
                        size=10,
                        color=BRAND_CYAN_SOFT,
                    ),
                ),
            ],
        )
    else:
        data_series = [result_line]
        max_y = 100
        grid_interval = 20
        left_values = (0, 20, 40, 60, 80, 100)
        right_axis = None

    chart = fch.LineChart(
        data_series=data_series,
        min_x=0,
        max_x=max_x,
        min_y=0,
        max_y=max_y,
        height=310,
        interactive=True,
        bgcolor=ft.Colors.TRANSPARENT,
        border=ft.Border.only(
            top=ft.BorderSide(1, GRID_COLOR),
            bottom=ft.BorderSide(1, GRID_COLOR),
        ),
        horizontal_grid_lines=fch.ChartGridLines(
            interval=grid_interval,
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
                    label=ft.Text(
                        str(value),
                        size=11,
                        color=BRAND_MUTED,
                    ),
                )
                for value in left_values
            ],
        ),
        right_axis=right_axis,
        bottom_axis=fch.ChartAxis(
            label_size=34,
            labels=_bottom_axis_labels(subject_tests),
        ),
        tooltip=fch.LineChartTooltip(
            bgcolor=ft.Colors.with_opacity(0.94, BRAND_CARD),
            fit_inside_horizontally=True,
            fit_inside_vertically=True,
        ),
    )

    stats = calculate_statistics(subject_tests)
    change = stats["change"]
    change_text = f"{change:+d}" if change is not None else "—"

    stat_controls = [
        _stat_chip("Средний", str(stats["average"])),
        _stat_chip("Лучший", str(stats["best"])),
        _stat_chip("Изменение", change_text),
    ]

    if basic:
        last_score = int(subject_tests[-1]["score"])
        last_grade = basic_math_grade(last_score)
        stat_controls.append(
            _stat_chip(
                "Текущая оценка",
                str(last_grade) if last_grade is not None else "—",
            )
        )

    controls = [
        section_title(
            "График прогресса",
            (
                "Баллы 0–21 и соответствующая школьная оценка."
                if basic
                else "Динамика баллов по сохранённым пробникам."
            ),
        ),
    ]

    if basic:
        controls.append(_basic_grade_scale())

    controls.extend(
        [
            ft.Row(
                controls=stat_controls,
                spacing=10,
                wrap=True,
            ),
            ft.Container(
                content=chart,
                padding=16,
                border_radius=16,
                bgcolor=ft.Colors.with_opacity(0.35, BRAND_BG),
                border=ft.Border.all(
                    1,
                    ft.Colors.with_opacity(0.18, BRAND_CYAN),
                ),
            ),
        ]
    )

    return ft.Container(
        content=ft.Column(
            controls=controls,
            spacing=14,
        ),
        padding=20,
        border_radius=20,
        border=ft.Border.all(1, CARD_BORDER),
        gradient=CHART_GRADIENT,
    )
