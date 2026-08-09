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
from storage import load_tests, save_tests
from ui.history import build_history_content
from ui.test_form import create_edit_form, create_test_form


class EgeTrackerApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.storage = ft.SharedPreferences()
        self.tests: list[dict] = []

        self.subject_status_texts = {}
        self.current_history_subject = None
        self.editing_test_id = None

        self.status_text = ft.Text(value="", size=14)

        self.subject_input = ft.Dropdown(
            label="Предмет",
            options=[
                ft.DropdownOption(key=subject, text=subject)
                for subject in SUBJECTS
            ],
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
            size=20,
            weight=ft.FontWeight.BOLD,
        )

        self.history_content = ft.Column(
            controls=[],
            spacing=10,
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
                    self.history_title,
                    self.history_content,
                    ft.Button(
                        content="Закрыть историю",
                        icon=ft.Icons.CLOSE,
                        on_click=self.close_history_click,
                    ),
                ],
                spacing=12,
            ),
            width=float("inf"),
            padding=20,
            border_radius=16,
            bgcolor=ft.Colors.BLUE_GREY_900,
            visible=False,
        )

    async def build(self):
        self.page.title = APP_NAME
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 24
        self.page.scroll = ft.ScrollMode.AUTO

        self.tests = await load_tests(self.storage)

        if ensure_test_ids(self.tests):
            await save_tests(self.storage, self.tests)

        subject_cards = self.create_subject_cards()

        title = ft.Text(
            value=APP_NAME,
            size=30,
            weight=ft.FontWeight.BOLD,
        )

        subtitle = ft.Text(
            value="Отслеживание результатов пробных экзаменов",
            size=16,
            color=ft.Colors.GREY_400,
        )

        add_test_button = ft.Button(
            content="Добавить пробник",
            icon=ft.Icons.ADD,
            on_click=self.add_test_click,
        )

        self.page.add(
            ft.SafeArea(
                content=ft.Column(
                    controls=[
                        title,
                        subtitle,
                        add_test_button,
                        self.test_form,
                        self.edit_form,
                        self.status_text,
                        self.history_panel,
                        ft.Divider(),
                        ft.Column(
                            controls=subject_cards,
                            spacing=12,
                        ),
                    ],
                    spacing=12,
                )
            )
        )

        self.update_all_subject_cards()
        self.page.update()

    def create_subject_cards(self):
        subject_cards = []

        for subject in SUBJECTS:
            subject_status = ft.Text(
                value="Пробников пока нет",
                size=14,
                color=ft.Colors.GREY_400,
            )

            self.subject_status_texts[subject] = subject_status

            card = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            value=subject,
                            size=20,
                            weight=ft.FontWeight.BOLD,
                        ),
                        subject_status,
                    ],
                    spacing=8,
                ),
                width=float("inf"),
                padding=20,
                border_radius=16,
                bgcolor=ft.Colors.BLUE_GREY_900,
                data=subject,
                on_click=self.subject_card_click,
            )

            subject_cards.append(card)

        return subject_cards

    def update_all_subject_cards(self):
        for subject in SUBJECTS:
            self.update_subject_card(subject)

    def update_subject_card(self, subject):
        subject_tests = get_subject_tests(self.tests, subject)

        if not subject_tests:
            self.subject_status_texts[subject].value = "Пробников пока нет"
            self.subject_status_texts[subject].color = ft.Colors.GREY_400
            return

        last_test = subject_tests[-1]

        self.subject_status_texts[subject].value = (
            f"Последний результат: {last_test['score']} баллов\n"
            f"Дата: {last_test['date']}\n"
            f"Всего пробников: {len(subject_tests)}"
        )
        self.subject_status_texts[subject].color = ft.Colors.GREY_300

    def set_status(self, text, color):
        self.status_text.value = text
        self.status_text.color = color

    def clear_status(self):
        self.status_text.value = ""

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
            self.set_status("Заполни все поля.", ft.Colors.RED_300)
            self.page.update()
            return

        if not validate_date(date):
            self.set_status("Дата должна быть в формате ДД.ММ.ГГГГ.", ft.Colors.RED_300)
            self.page.update()
            return

        try:
            score = int(score_text)
        except ValueError:
            self.set_status("Баллы должны быть целым числом.", ft.Colors.RED_300)
            self.page.update()
            return

        if score < 0 or score > 100:
            self.set_status("Баллы должны быть от 0 до 100.", ft.Colors.RED_300)
            self.page.update()
            return

        self.tests.append(create_test(subject, date, score))
        await save_tests(self.storage, self.tests)

        self.update_subject_card(subject)
        self.set_status("Пробник успешно добавлен.", ft.Colors.GREEN_300)

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
            self.set_status("Заполни дату и баллы.", ft.Colors.RED_300)
            self.page.update()
            return

        if not validate_date(new_date):
            self.set_status("Дата должна быть в формате ДД.ММ.ГГГГ.", ft.Colors.RED_300)
            self.page.update()
            return

        try:
            new_score = int(new_score_text)
        except ValueError:
            self.set_status("Баллы должны быть целым числом.", ft.Colors.RED_300)
            self.page.update()
            return

        if new_score < 0 or new_score > 100:
            self.set_status("Баллы должны быть от 0 до 100.", ft.Colors.RED_300)
            self.page.update()
            return

        subject = test_to_edit["subject"]
        update_test(test_to_edit, new_date, new_score)
        await save_tests(self.storage, self.tests)

        self.update_subject_card(subject)
        self.edit_form.visible = False
        self.editing_test_id = None
        self.set_status("Пробник изменён.", ft.Colors.GREEN_300)

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
        self.set_status("Пробник удалён.", ft.Colors.ORANGE_300)

        if self.current_history_subject is not None:
            self.show_history(self.current_history_subject)

        self.page.update()
