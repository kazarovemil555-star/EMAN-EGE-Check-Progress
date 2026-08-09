import flet as ft

from config import APP_NAME, SUBJECTS
from data import (
    create_test,
    delete_test,
    ensure_test_ids,
    find_test_by_id,
    get_subject_tests,
    update_test,
    validate_date,
)
from storage import load_subject_names, load_tests, save_subject_names, save_tests
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

        self.subject_status_texts = {}
        self.subject_title_texts = {}
        self.subject_cards_by_index = {}
        self.current_history_subject = None
        self.editing_test_id = None
        self.editing_subject_index = None

        self.status_text = ft.Text(value="", size=14, weight=ft.FontWeight.BOLD)
        self.status_container = ft.Container(
            content=self.status_text,
            padding=ft.Padding.symmetric(horizontal=14, vertical=10),
            border_radius=12,
            bgcolor=BRAND_SURFACE_2,
            border=ft.Border.all(1, ft.Colors.with_opacity(0.20, BRAND_CYAN)),
            visible=False,
        )

        self.subject_input = ft.Dropdown(
            label="Предмет",
            options=[],
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
            height=None,
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

        self.edit_date_input = ft.TextField(label="Новая дата")
        self.edit_score_input = ft.TextField(
            label="Новые баллы",
            keyboard_type=ft.KeyboardType.NUMBER,
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
                                padding=ft.Padding.symmetric(horizontal=10, vertical=6),
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
        self.page.theme = ft.Theme(color_scheme_seed=BRAND_CYAN)
        self.page.bgcolor = BRAND_BG
        self.page.padding = 20
        self.page.scroll = ft.ScrollMode.AUTO

        self.tests = await load_tests(self.storage)
        self.subjects = await load_subject_names(self.storage, SUBJECTS)
        self.refresh_subject_dropdown()

        if ensure_test_ids(self.tests):
            await save_tests(self.storage, self.tests)

        subject_cards = self.create_subject_cards()

        brand_header = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Image(
                                    src="logo_eman.png",
                                    width=84,
                                    height=84,
                                    fit=ft.BoxFit.CONTAIN,
                                ),
                                width=94,
                                height=94,
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Container(
                                        content=ft.Text(
                                            "EMAN PERFORMANCE SYSTEM",
                                            size=11,
                                            weight=ft.FontWeight.BOLD,
                                            color=BRAND_CYAN,
                                        ),
                                        padding=ft.Padding.symmetric(
                                            horizontal=10,
                                            vertical=5,
                                        ),
                                        border_radius=10,
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
                                        size=30,
                                        weight=ft.FontWeight.BOLD,
                                        color=BRAND_SILVER,
                                    ),
                                ],
                                spacing=7,
                            ),
                        ],
                        spacing=16,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Text(
                        "Твой прогресс — в цифрах, динамике и результате.",
                        size=15,
                        color=BRAND_CYAN_SOFT,
                    ),
                    ft.Text(
                        "Добавляй пробники, отслеживай рост и смотри историю по каждому предмету.",
                        size=12,
                        color=BRAND_MUTED,
                    ),
                ],
                spacing=8,
            ),
            padding=20,
            border_radius=22,
            gradient=HEADER_GRADIENT,
            border=ft.Border.all(1, CARD_BORDER),
        )

        add_test_button = primary_button(
            "Добавить пробник",
            ft.Icons.ADD,
            self.add_test_click,
        )

        action_bar = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
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
                    add_test_button,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=14,
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
                    ft.Text("EMAN", color=BRAND_CYAN, weight=ft.FontWeight.BOLD),
                    ft.Text("•", color=BRAND_MUTED),
                    ft.Text("Education Progress Technology", color=BRAND_MUTED, size=12),
                ],
                spacing=8,
            ),
            padding=ft.Padding.only(top=10, bottom=8),
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

    def create_subject_cards(self):
        subject_cards = []

        for index, subject in enumerate(self.subjects, start=1):
            subject_status = ft.Text(
                value="Пробников пока нет",
                size=13,
                color=BRAND_MUTED,
            )

            self.subject_status_texts[subject] = subject_status

            card = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text(
                                f"{index:02d}",
                                size=15,
                                weight=ft.FontWeight.BOLD,
                                color=BRAND_CYAN,
                            ),
                            width=48,
                            height=48,
                            alignment=ft.Alignment.CENTER,
                            border_radius=14,
                            bgcolor=ft.Colors.with_opacity(0.10, BRAND_CYAN),
                            border=ft.Border.all(1, ft.Colors.with_opacity(0.28, BRAND_CYAN)),
                        ),
                        ft.Container(
                            width=4,
                            height=58,
                            bgcolor=BRAND_CYAN,
                            border_radius=8,
                        ),
                        ft.Column(
                            controls=[
                                self._create_subject_title(index - 1, subject),
                                subject_status,
                            ],
                            spacing=7,
                            expand=True,
                        ),
                        *(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    tooltip="Переименовать предмет",
                                    data=index - 1,
                                    on_click=self.rename_subject_click,
                                    icon_color=BRAND_CYAN_SOFT,
                                )
                            ]
                            if index in (3, 4)
                            else []
                        ),
                        ft.Icon(
                            ft.Icons.CHEVRON_RIGHT,
                            color=BRAND_CYAN_SOFT,
                            size=28,
                        ),
                    ],
                    spacing=14,
                ),
                width=float("inf"),
                padding=18,
                border_radius=18,
                bgcolor=BRAND_CARD,
                border=ft.Border.all(1, ft.Colors.with_opacity(0.18, BRAND_CYAN)),
                ink=True,
                ink_color=ft.Colors.with_opacity(0.08, BRAND_CYAN),
                data=subject,
                on_click=self.subject_card_click,
            )

            self.subject_cards_by_index[index - 1] = card
            subject_cards.append(card)

        return subject_cards

    def _create_subject_title(self, index, subject):
        title = ft.Text(
            value=subject,
            size=20,
            weight=ft.FontWeight.BOLD,
            color=BRAND_SILVER,
        )
        self.subject_title_texts[index] = title
        return title

    def refresh_subject_dropdown(self):
        self.subject_input.options = [
            ft.DropdownOption(key=subject, text=subject)
            for subject in self.subjects
        ]

    def update_all_subject_cards(self):
        for subject in self.subjects:
            self.update_subject_card(subject)

    def update_subject_card(self, subject):
        subject_tests = get_subject_tests(self.tests, subject)

        if not subject_tests:
            self.subject_status_texts[subject].value = "Пробников пока нет"
            self.subject_status_texts[subject].color = BRAND_MUTED
            return

        last_test = subject_tests[-1]

        self.subject_status_texts[subject].value = (
            f"Последний: {last_test['score']} баллов  •  "
            f"{last_test['date']}  •  "
            f"Всего: {len(subject_tests)}"
        )
        self.subject_status_texts[subject].color = BRAND_CYAN_SOFT

    def rename_subject_click(self, e):
        index = e.control.data

        if index not in (2, 3):
            return

        self.editing_subject_index = index
        self.subject_name_title.value = f"Название предмета {index + 1}"
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

        new_name = (self.subject_name_input.value or "").strip()

        if not new_name:
            self.set_status("Название предмета не может быть пустым.", "#FF7D89")
            self.page.update()
            return

        if len(new_name) > 40:
            self.set_status("Название слишком длинное.", "#FF7D89")
            self.page.update()
            return

        if new_name in self.subjects and new_name != self.subjects[index]:
            self.set_status("Такой предмет уже есть.", "#FF7D89")
            self.page.update()
            return

        old_name = self.subjects[index]

        if new_name == old_name:
            self.subject_name_form.visible = False
            self.editing_subject_index = None
            self.page.update()
            return

        # Переносим старые пробники на новое название предмета.
        changed_tests = False
        for test in self.tests:
            if test.get("subject") == old_name:
                test["subject"] = new_name
                changed_tests = True

        self.subjects[index] = new_name

        status_control = self.subject_status_texts.pop(old_name, None)
        if status_control is not None:
            self.subject_status_texts[new_name] = status_control

        title_control = self.subject_title_texts.get(index)
        if title_control is not None:
            title_control.value = new_name

        card = self.subject_cards_by_index.get(index)
        if card is not None:
            card.data = new_name

        self.refresh_subject_dropdown()
        await save_subject_names(self.storage, self.subjects)

        if changed_tests:
            await save_tests(self.storage, self.tests)

        if self.current_history_subject == old_name:
            self.current_history_subject = new_name
            if self.history_panel.visible:
                self.show_history(new_name)

        self.update_subject_card(new_name)
        self.subject_name_form.visible = False
        self.editing_subject_index = None
        self.set_status(f"Предмет переименован: {new_name}.", BRAND_SUCCESS)
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
        self.clear_status()
        self.page.update()

    def close_form_click(self, e):
        self.test_form.visible = False
        self.page.update()

    async def save_test_click(self, e):
        subject = self.subject_input.value
        date = (self.date_input.value or "").strip()
        score_text = (self.score_input.value or "").strip()

        if not subject or not date or not score_text:
            self.set_status("Заполни все поля.", "#FF7D89")
            self.page.update()
            return

        if not validate_date(date):
            self.set_status("Дата должна быть в формате ДД.ММ.ГГГГ.", "#FF7D89")
            self.page.update()
            return

        try:
            score = int(score_text)
        except ValueError:
            self.set_status("Баллы должны быть целым числом.", "#FF7D89")
            self.page.update()
            return

        if score < 0 or score > 100:
            self.set_status("Баллы должны быть от 0 до 100.", "#FF7D89")
            self.page.update()
            return

        self.tests.append(create_test(subject, date, score))
        await save_tests(self.storage, self.tests)

        self.update_subject_card(subject)
        self.set_status("Пробник успешно добавлен.", BRAND_SUCCESS)

        self.subject_input.value = None
        self.date_input.value = ""
        self.score_input.value = ""
        self.test_form.visible = False

        if self.current_history_subject == subject and self.history_panel.visible:
            self.show_history(subject)

        self.page.update()

    def subject_card_click(self, e):
        self.show_history(e.control.data)
        self.page.update()

    def show_history(self, subject):
        self.current_history_subject = subject
        self.history_title.value = f"История: {subject}"

        subject_tests = get_subject_tests(self.tests, subject)
        self.history_content.controls = build_history_content(
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
        test_to_edit = find_test_by_id(self.tests, test_id)

        if test_to_edit is None:
            return

        self.editing_test_id = test_id
        self.edit_title.value = f"Редактирование: {test_to_edit['subject']}"
        self.edit_date_input.value = str(test_to_edit["date"])
        self.edit_score_input.value = str(test_to_edit["score"])

        self.test_form.visible = False
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

        test_to_edit = find_test_by_id(self.tests, self.editing_test_id)

        if test_to_edit is None:
            self.editing_test_id = None
            self.edit_form.visible = False
            self.page.update()
            return

        new_date = (self.edit_date_input.value or "").strip()
        new_score_text = (self.edit_score_input.value or "").strip()

        if not new_date or not new_score_text:
            self.set_status("Заполни дату и баллы.", "#FF7D89")
            self.page.update()
            return

        if not validate_date(new_date):
            self.set_status("Дата должна быть в формате ДД.ММ.ГГГГ.", "#FF7D89")
            self.page.update()
            return

        try:
            new_score = int(new_score_text)
        except ValueError:
            self.set_status("Баллы должны быть целым числом.", "#FF7D89")
            self.page.update()
            return

        if new_score < 0 or new_score > 100:
            self.set_status("Баллы должны быть от 0 до 100.", "#FF7D89")
            self.page.update()
            return

        subject = test_to_edit["subject"]
        update_test(test_to_edit, new_date, new_score)
        await save_tests(self.storage, self.tests)

        self.update_subject_card(subject)
        self.edit_form.visible = False
        self.editing_test_id = None
        self.set_status("Пробник изменён.", BRAND_SUCCESS)

        if self.current_history_subject is not None:
            self.show_history(self.current_history_subject)

        self.page.update()

    async def delete_test_click(self, e):
        test_id = e.control.data
        test_to_delete = find_test_by_id(self.tests, test_id)

        if test_to_delete is None:
            return

        subject = test_to_delete["subject"]
        delete_test(self.tests, test_id)
        await save_tests(self.storage, self.tests)

        self.update_subject_card(subject)
        self.set_status("Пробник удалён.", "#FFB84D")

        if self.current_history_subject is not None:
            self.show_history(self.current_history_subject)

        self.page.update()
