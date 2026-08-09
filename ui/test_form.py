import flet as ft


CARD_COLOR = ft.Colors.BLUE_GREY_900


def create_test_form(
    subject_input,
    date_input,
    score_input,
    on_save,
    on_close,
):
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    value="Новый пробник",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),
                subject_input,
                date_input,
                score_input,
                ft.Row(
                    controls=[
                        ft.Button(
                            content="Сохранить",
                            icon=ft.Icons.SAVE,
                            on_click=on_save,
                        ),
                        ft.Button(
                            content="Закрыть",
                            icon=ft.Icons.CLOSE,
                            on_click=on_close,
                        ),
                    ],
                    wrap=True,
                ),
            ],
            spacing=12,
        ),
        padding=20,
        border_radius=16,
        bgcolor=CARD_COLOR,
        visible=False,
    )


def create_edit_form(
    edit_title,
    edit_date_input,
    edit_score_input,
    on_save,
    on_close,
):
    return ft.Container(
        content=ft.Column(
            controls=[
                edit_title,
                edit_date_input,
                edit_score_input,
                ft.Row(
                    controls=[
                        ft.Button(
                            content="Сохранить изменения",
                            icon=ft.Icons.SAVE,
                            on_click=on_save,
                        ),
                        ft.Button(
                            content="Отмена",
                            icon=ft.Icons.CLOSE,
                            on_click=on_close,
                        ),
                    ],
                    wrap=True,
                ),
            ],
            spacing=12,
        ),
        padding=20,
        border_radius=16,
        bgcolor=CARD_COLOR,
        visible=False,
    )
