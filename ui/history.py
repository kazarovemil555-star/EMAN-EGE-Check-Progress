import flet as ft

from ui.charts import build_progress_section


ITEM_COLOR = ft.Colors.BLUE_GREY_800


def build_history_content(
    subject_tests: list[dict],
    on_edit,
    on_delete,
):
    controls = [
        build_progress_section(subject_tests),
        ft.Divider(),
        ft.Text(
            "История пробников",
            size=18,
            weight=ft.FontWeight.BOLD,
        ),
    ]

    if not subject_tests:
        controls.append(
            ft.Text(
                "Пробников пока нет.",
                color=ft.Colors.GREY_400,
            )
        )
        return controls

    for number, test in enumerate(subject_tests, start=1):
        controls.append(
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(
                            value=f"{number}. {test['date']}",
                            expand=True,
                        ),
                        ft.Text(
                            value=f"{test['score']} баллов",
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            tooltip="Редактировать пробник",
                            data=test["id"],
                            on_click=on_edit,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE,
                            tooltip="Удалить пробник",
                            data=test["id"],
                            on_click=on_delete,
                        ),
                    ],
                ),
                padding=12,
                border_radius=12,
                bgcolor=ITEM_COLOR,
            )
        )

    return controls
