import flet as ft

from config import (
    APP_NAME,
    BASIC_MATH_NAME,
    MATH_MODE_BASIC,
    MATH_MODE_PROFILE,
    PROFILE_MATH_NAME,
    SUBJECTS,
)
from data import (
    basic_math_grade,
    create_test,
    delete_test,
    ensure_test_ids,
    find_test_by_id,
    format_result,
    get_subject_tests,
    is_basic_math,
    score_max_for_subject,
    score_range_text,
    update_test,
    validate_date,
)
from storage import (
    load_math_mode,
    load_subject_names,
    load_tests,
    save_math_mode,
    save_subject_names,
    save_tests,
)
from ui.history import build_history_content
from ui.test_form import create_edit_form, create_test_form
from ui.theme import (
    BRAND_BG,
    BRAND_CARD,
    BRAND_CYAN,
    BRAND_CYAN_SOFT,
    BRAND_MUTED,
    BRAND_SILVER,
    BRAND_SUCCESS,
    BRAND_SURFACE,
    BRAND_SURFACE_2,
    CARD_BORDER,
    HEADER_GRADIENT,
    SOFT_CYAN,
    primary_button,
    secondary_button,
    section_title,
)


class EgeTrackerApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.storage = ft.SharedPreferences()

        self.tests: list[dict] = []
        self.subjects = list(SUBJECTS)
        self.math_mode = MATH_MODE_PROFILE

        self.subject_status_texts = {}
        self.subject_title_texts = {}
        self.subject_cards_by_index = {}

        self.current_history_subject = None
        self.editing_test_id = None
        self.editing_subject_index = None

        self.status_text = ft.Text(
            value="",
            size=14,
            weight=ft.FontWeight.BOLD,
        )
        self.status_container = ft.Container(
            content=self.status_text,
            padding=ft.Padding.symmetric(
                horizontal=14,
                vertical=10,
            ),
            border_radius=12,
            bgcolor=BRAND_SURFACE_2,
            border=ft.Border.all(
                1,
                ft.Colors.with_opacity(0.20, BRAND_CYAN),
            ),
            visible=False,
        )

        self.subject_input = ft.Dropdown(
            label="Предмет",
            options=[],
            on_select=self.subject_selected,
        )

        self.date_input = ft.TextField(
            label="Дата пробника",
            hint_text="Например: 09.08.2026",
        )

        self.score_input = ft.TextField(
            label="Баллы",
            hint_text="От 0 до 100",
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        self.edit_title = ft.Text(
            value="Редактирование пробника",
            size=20,
            weight=ft.FontWeight.BOLD,
        )

        self.edit_date_input = ft.TextField(
            label="Новая дата",
        )

        self.edit_score_input = ft.TextField(
            label="Новые баллы",
            hint_text="От 0 до 100",
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        self.math_selector = ft.SegmentedButton(
            selected=[MATH_MODE_PROFILE],
            allow_empty_selection=False,
            allow_multiple_selection=False,
            show_selected_icon=False,
            on_change=self.math_mode_changed,
            segments=[
                ft.Segment(
                    value=MATH_MODE_PROFILE,
                    label="Профильная",
                    icon=ft.Icon(ft.Icons.TRENDING_UP),
                ),
                ft.Segment(
                    value=MATH_MODE_BASIC,
                    label="Базовая",
                    icon=ft.Icon(ft.Icons.SCHOOL_OUTLINED),
                ),
            ],
        )

        self.math_mode_note = ft.Text(
            "Профильная математика: шкала 0–100.",
            size=11,
            color=BRAND_MUTED,
        )

        self.subject_name_title = ft.Text(
            value="Название предмета",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=BRAND_SILVER,
        )

        self.subject_name_input = ft.TextField(
            label="Новое название",
            hint_text="Например: Физика",
            max_length=40,
        )

        self.subject_name_form = ft.Container(
            content=ft.Column(
                controls=[
                    self.subject_name_title,
                    ft.Text(
                        "Можно переименовывать только Предмет 3 и Предмет 4.",
                        size=12,
                        color=BRAND_MUTED,
                    ),
                    self.subject_name_input,
                    ft.Row(
                        controls=[
                            primary_button(
                                "Сохранить название",
                                ft.Icons.SAVE,
                                self.save_subject_name_click,
                            ),
                            secondary_button(
                                "Отмена",
                                ft.Icons.CLOSE,
                                self.close_subject_name_click,
                            ),
                        ],
                        wrap=True,
                        spacing=10,
                    ),
                ],
                spacing=12,
            ),
            padding=20,
            border_radius=18,
            bgcolor=BRAND_SURFACE,
            border=ft.Border.all(1, CARD_BORDER),
            visible=False,
        )

        self.history_title = ft.Text(
            value="История пробников",
            size=22,
            weight=ft.FontWeight.BOLD,
            color=BRAND_SILVER,
        )

        self.history_content = ft.Column(
            controls=[],
            spacing=14,
        )

        self.test_form = create_test_form(
            self.subject_input,
            self.date_input,
            self.score_input,
            self.save_test_click,
            self.close_form_click,
        )

        self.edit_form = create_edit_form(
            self.edit_title,
            self.edit_date_input,
            self.edit_score_input,
            self.save_edit_click,
            self.close_edit_click,
        )

        self.history_panel = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Text(
                                    "EMAN / ANALYTICS",
                                    size=11,
                                    weight=ft.FontWeight.BOLD,
                                    color=BRAND_CYAN,
                                ),
                                padding=ft.Padding.symmetric(
                                    horizontal=10,
                                    vertical=6,
                                ),
                                border_radius=10,
                                bgcolor=SOFT_CYAN,
                            ),
                            self.history_title,
                        ],
                        spacing=12,
                        wrap=True,
                    ),
                    self.history_content,
                    secondary_button(
                        "Закрыть историю",
                        ft.Icons.CLOSE,
                        self.close_history_click,
                    ),
                ],
                spacing=16,
            ),
            width=float("inf"),
            padding=22,
            border_radius=22,
            bgcolor=BRAND_SURFACE,
            border=ft.Border.all(1, CARD_BORDER),
            visible=False,
        )

    async def build(self):
        self.page.title = APP_NAME
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.theme = ft.Theme(
            color_scheme_seed=BRAND_CYAN,
        )
        self.page.bgcolor = BRAND_BG
        self.page.padding = 12
        self.page.scroll = ft.ScrollMode.AUTO

        self.tests = await load_tests(self.storage)

        self.subjects = await load_subject_names(
            self.storage,
            SUBJECTS,
        )

        self.math_mode = await load_math_mode(self.storage)
        self.subjects[1] = self.current_math_subject()

        self.math_selector.selected = [self.math_mode]
        self.update_math_mode_note()
        self.refresh_subject_dropdown()

        if ensure_test_ids(self.tests):
            await save_tests(self.storage, self.tests)

        subject_cards = self.create_subject_cards()

        brand_header = self.build_brand_header()

        add_test_button = primary_button(
            "Добавить пробник",
            ft.Icons.ADD,
            self.add_test_click,
        )

        action_bar = ft.Container(
            content=ft.ResponsiveRow(
                controls=[
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "Панель результатов",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=BRAND_SILVER,
                                ),
                                ft.Text(
                                    "Сохраняй новые результаты — карточки и графики обновятся автоматически.",
                                    size=12,
                                    color=BRAND_MUTED,
                                ),
                            ],
                            spacing=3,
                        ),
                        col={"xs": 12, "md": 5},
                    ),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "Режим математики",
                                    size=12,
                                    weight=ft.FontWeight.BOLD,
                                    color=BRAND_CYAN_SOFT,
                                ),
                                self.math_selector,
                                self.math_mode_note,
                            ],
                            spacing=6,
                        ),
                        col={"xs": 12, "md": 5},
                    ),
                    ft.Container(
                        content=add_test_button,
                        alignment=ft.Alignment.CENTER_RIGHT,
                        col={"xs": 12, "md": 2},
                    ),
                ],
                spacing=12,
                run_spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=16,
            border_radius=18,
            bgcolor=BRAND_SURFACE,
            border=ft.Border.all(
                1,
                ft.Colors.with_opacity(0.18, BRAND_CYAN),
            ),
        )

        subjects_header = section_title(
            "Предметы",
            "Нажми на карточку предмета, чтобы открыть график и историю пробников.",
        )

        footer = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(
                        "EMAN",
                        color=BRAND_CYAN,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text("•", color=BRAND_MUTED),
                    ft.Text(
                        "Education Progress Technology",
                        color=BRAND_MUTED,
                        size=12,
                    ),
                ],
                spacing=8,
                wrap=True,
            ),
            padding=ft.Padding.only(
                top=10,
                bottom=8,
            ),
        )

        self.page.add(
            ft.SafeArea(
                content=ft.Column(
                    controls=[
                        brand_header,
                        action_bar,
                        self.test_form,
                        self.edit_form,
                        self.subject_name_form,
                        self.status_container,
                        self.history_panel,
                        subjects_header,
                        ft.Column(
                            controls=subject_cards,
                            spacing=12,
                        ),
                        footer,
                    ],
                    spacing=12,
                )
            )
        )

        self.update_all_subject_cards()
        self.page.update()

    def build_brand_header(self):
        identity = ft.Container(
            content=ft.ResponsiveRow(
                controls=[
                    ft.Container(
                        content=ft.Image(
                            src="logo_eman.png",
                            width=82,
                            height=82,
                            fit=ft.BoxFit.CONTAIN,
                        ),
                        alignment=ft.Alignment.CENTER,
                        col={"xs": 3, "sm": 2},
                    ),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Container(
                                    content=ft.Text(
                                        "EMAN PERFORMANCE SYSTEM",
                                        size=10,
                                        weight=ft.FontWeight.BOLD,
                                        color=BRAND_CYAN,
                                    ),
                                    padding=ft.Padding.symmetric(
                                        horizontal=9,
                                        vertical=5,
                                    ),
                                    border_radius=9,
                                    bgcolor=ft.Colors.with_opacity(
                                        0.10,
                                        BRAND_CYAN,
                                    ),
                                    border=ft.Border.all(
                                        1,
                                        ft.Colors.with_opacity(
                                            0.20,
                                            BRAND_CYAN,
                                        ),
                                    ),
                                ),
                                ft.Text(
                                    APP_NAME,
                                    size=28,
                                    weight=ft.FontWeight.BOLD,
                                    color=BRAND_SILVER,
                                ),
                            ],
                            spacing=7,
                        ),
                        col={"xs": 9, "sm": 10},
                    ),
                    ft.Container(
                        content=ft.Text(
                            "Твой прогресс — в цифрах, динамике и результате.",
                            size=15,
                            color=BRAND_CYAN_SOFT,
                        ),
                        col={"xs": 12},
                    ),
                    ft.Container(
                        content=ft.Text(
                            "Добавляй пробники, отслеживай рост и смотри историю по каждому предмету.",
                            size=12,
                            color=BRAND_MUTED,
                        ),
                        col={"xs": 12},
                    ),
                ],
                spacing=8,
                run_spacing=7,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            col={"xs": 12, "lg": 8},
        )

        # Декоративный блок заполняет пустое место на широких экранах
        # и полностью исчезает на телефоне/планшете.
        performance_visual = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.INSIGHTS,
                                color=BRAND_CYAN,
                                size=24,
                            ),
                            ft.Text(
                                "PERFORMANCE GRID",
                                color=BRAND_CYAN_SOFT,
                                size=11,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        spacing=8,
                    ),
                    ft.Row(
                        controls=[
                            self._visual_step("01", "TRACK"),
                            self._visual_step("02", "ANALYZE"),
                            self._visual_step("03", "GROW"),
                        ],
                        spacing=8,
                    ),
                    ft.Text(
                        "TRACK  →  ANALYZE  →  GROW",
                        size=10,
                        color=BRAND_MUTED,
                    ),
                ],
                spacing=10,
            ),
            padding=16,
            border_radius=16,
            bgcolor=ft.Colors.with_opacity(0.08, BRAND_CYAN),
            border=ft.Border.all(
                1,
                ft.Colors.with_opacity(0.18, BRAND_CYAN),
            ),
            col={"xs": 0, "lg": 4},
        )

        return ft.Container(
            content=ft.ResponsiveRow(
                controls=[
                    identity,
                    performance_visual,
                ],
                spacing=16,
                run_spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            border_radius=22,
            gradient=HEADER_GRADIENT,
            border=ft.Border.all(1, CARD_BORDER),
        )

    def _visual_step(self, number: str, label: str):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        number,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=BRAND_CYAN,
                    ),
                    ft.Text(
                        label,
                        size=9,
                        color=BRAND_SILVER,
                    ),
                ],
                spacing=1,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=68,
            padding=8,
            border_radius=12,
            bgcolor=ft.Colors.with_opacity(0.08, BRAND_CYAN),
        )

    def current_math_subject(self) -> str:
        if self.math_mode == MATH_MODE_BASIC:
            return BASIC_MATH_NAME

        return PROFILE_MATH_NAME

    def update_math_mode_note(self):
        if self.math_mode == MATH_MODE_BASIC:
            self.math_mode_note.value = (
                "Базовая: 0–21 балл. Оценка определяется автоматически."
            )
        else:
            self.math_mode_note.value = (
                "Профильная: шкала результатов 0–100."
            )

    async def math_mode_changed(self, e):
        selected = list(e.control.selected)

        if not selected:
            return

        new_mode = selected[0]

        if new_mode not in (
            MATH_MODE_PROFILE,
            MATH_MODE_BASIC,
        ):
            return

        old_subject = self.subjects[1]
        self.math_mode = new_mode
        new_subject = self.current_math_subject()

        if old_subject == new_subject:
            return

        self.subjects[1] = new_subject

        status_control = self.subject_status_texts.pop(
            old_subject,
            None,
        )
        if status_control is not None:
            self.subject_status_texts[new_subject] = status_control

        title_control = self.subject_title_texts.get(1)
        if title_control is not None:
            title_control.value = new_subject

        card = self.subject_cards_by_index.get(1)
        if card is not None:
            card.data = new_subject

        self.subject_input.value = None
        self.refresh_subject_dropdown()
        self.update_score_input_for_subject(None)
        self.update_math_mode_note()

        await save_math_mode(
            self.storage,
            self.math_mode,
        )

        self.update_subject_card(new_subject)

        if self.current_history_subject == old_subject:
            self.show_history(new_subject)

        self.set_status(
            f"Выбрана {new_subject.lower()}.",
            BRAND_SUCCESS,
        )
        self.page.update()

    def create_subject_cards(self):
        subject_cards = []

        for index, subject in enumerate(
            self.subjects,
            start=1,
        ):
            subject_status = ft.Text(
                value="Пробников пока нет",
                size=12,
                color=BRAND_MUTED,
                max_lines=2,
            )

            self.subject_status_texts[subject] = subject_status

            edit_button = (
                ft.IconButton(
                    icon=ft.Icons.EDIT,
                    tooltip="Переименовать предмет",
                    data=index - 1,
                    on_click=self.rename_subject_click,
                    icon_color=BRAND_CYAN_SOFT,
                    icon_size=20,
                )
                if index in (3, 4)
                else None
            )

            row_controls = [
                ft.Container(
                    content=ft.Text(
                        f"{index:02d}",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=BRAND_CYAN,
                    ),
                    width=42,
                    height=42,
                    alignment=ft.Alignment.CENTER,
                    border_radius=12,
                    bgcolor=ft.Colors.with_opacity(
                        0.10,
                        BRAND_CYAN,
                    ),
                    border=ft.Border.all(
                        1,
                        ft.Colors.with_opacity(
                            0.28,
                            BRAND_CYAN,
                        ),
                    ),
                ),
                ft.Container(
                    width=3,
                    height=48,
                    bgcolor=BRAND_CYAN,
                    border_radius=8,
                ),
                ft.Column(
                    controls=[
                        self._create_subject_title(
                            index - 1,
                            subject,
                        ),
                        subject_status,
                    ],
                    spacing=4,
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ]

            if edit_button is not None:
                row_controls.append(edit_button)

            row_controls.append(
                ft.Icon(
                    ft.Icons.CHEVRON_RIGHT,
                    color=BRAND_CYAN_SOFT,
                    size=24,
                )
            )

            card = ft.Container(
                content=ft.Row(
                    controls=row_controls,
                    spacing=10,
                    wrap=False,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                width=float("inf"),
                height=86,
                padding=ft.Padding.symmetric(
                    horizontal=14,
                    vertical=10,
                ),
                border_radius=16,
                bgcolor=BRAND_CARD,
                border=ft.Border.all(
                    1,
                    ft.Colors.with_opacity(
                        0.18,
                        BRAND_CYAN,
                    ),
                ),
                ink=True,
                ink_color=ft.Colors.with_opacity(
                    0.08,
                    BRAND_CYAN,
                ),
                data=subject,
                on_click=self.subject_card_click,
            )

            self.subject_cards_by_index[index - 1] = card
            subject_cards.append(card)

        return subject_cards

    def _create_subject_title(
        self,
        index: int,
        subject: str,
    ):
        title = ft.Text(
            value=subject,
            size=18,
            weight=ft.FontWeight.BOLD,
            color=BRAND_SILVER,
            max_lines=1,
        )

        self.subject_title_texts[index] = title
        return title

    def refresh_subject_dropdown(self):
        self.subject_input.options = [
            ft.DropdownOption(
                key=subject,
                text=subject,
            )
            for subject in self.subjects
        ]

    def subject_selected(self, e):
        self.update_score_input_for_subject(
            e.control.value,
        )
        self.page.update()

    def update_score_input_for_subject(
        self,
        subject: str | None,
    ):
        if not subject:
            self.score_input.label = "Баллы"
            self.score_input.hint_text = "Выбери предмет"
            return

        self.score_input.label = (
            f"Баллы (0–{score_max_for_subject(subject)})"
        )
        self.score_input.hint_text = score_range_text(subject)

    def update_edit_score_input(
        self,
        subject: str,
    ):
        maximum = score_max_for_subject(subject)
        self.edit_score_input.label = (
            f"Новые баллы (0–{maximum})"
        )
        self.edit_score_input.hint_text = (
            f"От 0 до {maximum}"
        )

    def update_all_subject_cards(self):
        for subject in self.subjects:
            self.update_subject_card(subject)

    def update_subject_card(self, subject):
        subject_tests = get_subject_tests(
            self.tests,
            subject,
        )

        if not subject_tests:
            self.subject_status_texts[subject].value = (
                "Пробников пока нет"
            )
            self.subject_status_texts[subject].color = BRAND_MUTED
            return

        last_test = subject_tests[-1]
        last_score = int(last_test["score"])

        self.subject_status_texts[subject].value = (
            f"Последний: {format_result(subject, last_score)}  •  "
            f"{last_test['date']}  •  "
            f"Всего: {len(subject_tests)}"
        )
        self.subject_status_texts[subject].color = BRAND_CYAN_SOFT

    def rename_subject_click(self, e):
        index = e.control.data

        if index not in (2, 3):
            return

        self.editing_subject_index = index
        self.subject_name_title.value = (
            f"Название предмета {index + 1}"
        )
        self.subject_name_input.value = self.subjects[index]

        self.subject_name_form.visible = True
        self.test_form.visible = False
        self.edit_form.visible = False
        self.clear_status()
        self.page.update()

    def close_subject_name_click(self, e):
        self.subject_name_form.visible = False
        self.editing_subject_index = None
        self.page.update()

    async def save_subject_name_click(self, e):
        index = self.editing_subject_index

        if index not in (2, 3):
            return

        new_name = (
            self.subject_name_input.value or ""
        ).strip()

        if not new_name:
            self.set_status(
                "Название предмета не может быть пустым.",
                "#FF7D89",
            )
            self.page.update()
            return

        if len(new_name) > 40:
            self.set_status(
                "Название слишком длинное.",
                "#FF7D89",
            )
            self.page.update()
            return

        if (
            new_name in self.subjects
            and new_name != self.subjects[index]
        ):
            self.set_status(
                "Такой предмет уже есть.",
                "#FF7D89",
            )
            self.page.update()
            return

        old_name = self.subjects[index]

        if new_name == old_name:
            self.subject_name_form.visible = False
            self.editing_subject_index = None
            self.page.update()
            return

        changed_tests = False

        for test in self.tests:
            if test.get("subject") == old_name:
                test["subject"] = new_name
                changed_tests = True

        self.subjects[index] = new_name

        status_control = self.subject_status_texts.pop(
            old_name,
            None,
        )
        if status_control is not None:
            self.subject_status_texts[new_name] = status_control

        title_control = self.subject_title_texts.get(index)
        if title_control is not None:
            title_control.value = new_name

        card = self.subject_cards_by_index.get(index)
        if card is not None:
            card.data = new_name

        self.refresh_subject_dropdown()

        await save_subject_names(
            self.storage,
            self.subjects,
        )

        if changed_tests:
            await save_tests(
                self.storage,
                self.tests,
            )

        if self.current_history_subject == old_name:
            self.current_history_subject = new_name

            if self.history_panel.visible:
                self.show_history(new_name)

        self.update_subject_card(new_name)

        self.subject_name_form.visible = False
        self.editing_subject_index = None

        self.set_status(
            f"Предмет переименован: {new_name}.",
            BRAND_SUCCESS,
        )
        self.page.update()

    def set_status(self, text, color):
        self.status_text.value = text
        self.status_text.color = color
        self.status_container.visible = True

    def clear_status(self):
        self.status_text.value = ""
        self.status_container.visible = False

    def add_test_click(self, e):
        self.test_form.visible = True
        self.edit_form.visible = False
        self.subject_name_form.visible = False
        self.clear_status()

        self.subject_input.value = None
        self.update_score_input_for_subject(None)

        self.page.update()

    def close_form_click(self, e):
        self.test_form.visible = False
        self.page.update()

    async def save_test_click(self, e):
        subject = self.subject_input.value
        date = (self.date_input.value or "").strip()
        score_text = (self.score_input.value or "").strip()

        if not subject or not date or not score_text:
            self.set_status(
                "Заполни все поля.",
                "#FF7D89",
            )
            self.page.update()
            return

        if not validate_date(date):
            self.set_status(
                "Дата должна быть в формате ДД.ММ.ГГГГ.",
                "#FF7D89",
            )
            self.page.update()
            return

        try:
            score = int(score_text)
        except ValueError:
            self.set_status(
                "Баллы должны быть целым числом.",
                "#FF7D89",
            )
            self.page.update()
            return

        maximum = score_max_for_subject(subject)

        if score < 0 or score > maximum:
            self.set_status(
                f"Баллы должны быть от 0 до {maximum}.",
                "#FF7D89",
            )
            self.page.update()
            return

        self.tests.append(
            create_test(
                subject,
                date,
                score,
            )
        )

        await save_tests(
            self.storage,
            self.tests,
        )

        self.update_subject_card(subject)

        if is_basic_math(subject):
            grade = basic_math_grade(score)
            message = (
                f"Пробник добавлен: {score} баллов, оценка {grade}."
            )
        else:
            message = "Пробник успешно добавлен."

        self.set_status(
            message,
            BRAND_SUCCESS,
        )

        self.subject_input.value = None
        self.date_input.value = ""
        self.score_input.value = ""
        self.update_score_input_for_subject(None)

        self.test_form.visible = False

        if (
            self.current_history_subject == subject
            and self.history_panel.visible
        ):
            self.show_history(subject)

        self.page.update()

    def subject_card_click(self, e):
        self.show_history(e.control.data)
        self.page.update()

    def show_history(self, subject):
        self.current_history_subject = subject
        self.history_title.value = f"История: {subject}"

        subject_tests = get_subject_tests(
            self.tests,
            subject,
        )

        self.history_content.controls = build_history_content(
            subject,
            subject_tests,
            self.edit_test_click,
            self.delete_test_click,
        )

        self.history_panel.visible = True

    def close_history_click(self, e):
        self.history_panel.visible = False
        self.edit_form.visible = False
        self.editing_test_id = None
        self.page.update()

    def edit_test_click(self, e):
        test_id = e.control.data
        test_to_edit = find_test_by_id(
            self.tests,
            test_id,
        )

        if test_to_edit is None:
            return

        self.editing_test_id = test_id
        subject = str(test_to_edit["subject"])

        self.edit_title.value = (
            f"Редактирование: {subject}"
        )

        self.edit_date_input.value = str(
            test_to_edit["date"]
        )
        self.edit_score_input.value = str(
            test_to_edit["score"]
        )

        self.update_edit_score_input(subject)

        self.test_form.visible = False
        self.subject_name_form.visible = False
        self.edit_form.visible = True
        self.clear_status()
        self.page.update()

    def close_edit_click(self, e):
        self.edit_form.visible = False
        self.editing_test_id = None
        self.page.update()

    async def save_edit_click(self, e):
        if self.editing_test_id is None:
            return

        test_to_edit = find_test_by_id(
            self.tests,
            self.editing_test_id,
        )

        if test_to_edit is None:
            self.editing_test_id = None
            self.edit_form.visible = False
            self.page.update()
            return

        subject = str(test_to_edit["subject"])

        new_date = (
            self.edit_date_input.value or ""
        ).strip()
        new_score_text = (
            self.edit_score_input.value or ""
        ).strip()

        if not new_date or not new_score_text:
            self.set_status(
                "Заполни дату и баллы.",
                "#FF7D89",
            )
            self.page.update()
            return

        if not validate_date(new_date):
            self.set_status(
                "Дата должна быть в формате ДД.ММ.ГГГГ.",
                "#FF7D89",
            )
            self.page.update()
            return

        try:
            new_score = int(new_score_text)
        except ValueError:
            self.set_status(
                "Баллы должны быть целым числом.",
                "#FF7D89",
            )
            self.page.update()
            return

        maximum = score_max_for_subject(subject)

        if new_score < 0 or new_score > maximum:
            self.set_status(
                f"Баллы должны быть от 0 до {maximum}.",
                "#FF7D89",
            )
            self.page.update()
            return

        update_test(
            test_to_edit,
            new_date,
            new_score,
        )

        await save_tests(
            self.storage,
            self.tests,
        )

        self.update_subject_card(subject)

        self.edit_form.visible = False
        self.editing_test_id = None

        if is_basic_math(subject):
            grade = basic_math_grade(new_score)
            message = (
                f"Пробник изменён: {new_score} баллов, оценка {grade}."
            )
        else:
            message = "Пробник изменён."

        self.set_status(
            message,
            BRAND_SUCCESS,
        )

        if self.current_history_subject is not None:
            self.show_history(
                self.current_history_subject,
            )

        self.page.update()

    async def delete_test_click(self, e):
        test_id = e.control.data
        test_to_delete = find_test_by_id(
            self.tests,
            test_id,
        )

        if test_to_delete is None:
            return

        subject = str(test_to_delete["subject"])

        delete_test(
            self.tests,
            test_id,
        )

        await save_tests(
            self.storage,
            self.tests,
        )

        self.update_subject_card(subject)

        self.set_status(
            "Пробник удалён.",
            "#FFB84D",
        )

        if self.current_history_subject is not None:
            self.show_history(
                self.current_history_subject,
            )

        self.page.update()
