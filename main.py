import flet as ft

from ui.home import EgeTrackerApp


async def main(page: ft.Page):
    app = EgeTrackerApp(page)
    await app.build()


if __name__ == "__main__":
    ft.run(main)
