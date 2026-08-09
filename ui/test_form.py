import flet as ft

from ui.theme import (
    BRAND_CYAN,
    BRAND_MUTED,
    BRAND_SILVER,
    CARD_BORDER,
    CARD_GRADIENT,
    primary_button,
    secondary_button,
    section_title,
)


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
                section_title(
                    "Новый пробник",
                    "Добавь результат — он сразу попадёт в историю и график.",
                ),
                subject_input,
                date_input,
                score_input,
                ft.Row(
                    controls=[
                        primary_button("Сохранить", ft.Icons.SAVE, on_save),
                        secondary_button("Закрыть", ft.Icons.CLOSE, on_close),
                    ],
                    wrap=True,
                ),
            ],
            spacing=14,
        ),
        padding=22,
        border_radius=20,
        border=ft.Border.all(1, CARD_BORDER),
        gradient=CARD_GRADIENT,
        visible=False,
    )


def create_edit_form(
    edit_title,
    edit_date_input,
    edit_score_input,
    on_save,
    on_close,
):
    edit_title.color = BRAND_SILVER
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            width=4,
                            height=24,
                            bgcolor=BRAND_CYAN,
                            border_radius=8,
                        ),
                        edit_title,
                    ],
                    spacing=10,
                ),
                ft.Text(
                    "Исправь дату или количество баллов.",
                    size=13,
                    color=BRAND_MUTED,
                ),
                edit_date_input,
                edit_score_input,
                ft.Row(
                    controls=[
                        primary_button(
                            "Сохранить изменения",
                            ft.Icons.SAVE,
                            on_save,
                        ),
                        secondary_button("Отмена", ft.Icons.CLOSE, on_close),
                    ],
                    wrap=True,
                ),
            ],
            spacing=14,
        ),
        padding=22,
        border_radius=20,
        border=ft.Border.all(1, CARD_BORDER),
        gradient=CARD_GRADIENT,
        visible=False,
    )
