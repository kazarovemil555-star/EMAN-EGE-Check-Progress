import flet as ft


BRAND_BG = "#050A0F"
BRAND_BG_2 = "#07131D"
BRAND_SURFACE = "#0A1721"
BRAND_SURFACE_2 = "#0D202D"
BRAND_CARD = "#102735"
BRAND_CARD_HOVER = "#133142"
BRAND_CYAN = "#16D8FF"
BRAND_CYAN_SOFT = "#7BEAFF"
BRAND_SILVER = "#E4EDF2"
BRAND_MUTED = "#91A8B5"
BRAND_LINE = "#294655"
BRAND_DANGER = "#FF6B7A"
BRAND_WARNING = "#FFB84D"
BRAND_SUCCESS = "#61E6B7"

CARD_BORDER = ft.Colors.with_opacity(0.34, BRAND_CYAN)
SOFT_CYAN = ft.Colors.with_opacity(0.12, BRAND_CYAN)
SOFT_SILVER = ft.Colors.with_opacity(0.10, BRAND_SILVER)

HEADER_GRADIENT = ft.LinearGradient(
    begin=ft.Alignment.TOP_LEFT,
    end=ft.Alignment.BOTTOM_RIGHT,
    colors=[BRAND_BG_2, "#0B2635", BRAND_BG_2],
    stops=[0.0, 0.55, 1.0],
)

CARD_GRADIENT = ft.LinearGradient(
    begin=ft.Alignment.TOP_LEFT,
    end=ft.Alignment.BOTTOM_RIGHT,
    colors=[BRAND_SURFACE_2, BRAND_CARD],
)

CHART_GRADIENT = ft.LinearGradient(
    begin=ft.Alignment.TOP_LEFT,
    end=ft.Alignment.BOTTOM_RIGHT,
    colors=["#07141E", "#0B2330"],
)


def primary_button(text, icon, on_click):
    return ft.Button(
        content=text,
        icon=icon,
        on_click=on_click,
        bgcolor=BRAND_CYAN,
        color=BRAND_BG,
        icon_color=BRAND_BG,
        elevation=0,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
    )


def secondary_button(text, icon, on_click):
    return ft.Button(
        content=text,
        icon=icon,
        on_click=on_click,
        bgcolor=BRAND_SURFACE_2,
        color=BRAND_SILVER,
        icon_color=BRAND_CYAN_SOFT,
        elevation=0,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            side=ft.BorderSide(1, CARD_BORDER),
        ),
    )


def section_title(text: str, subtitle: str | None = None):
    controls = [
        ft.Row(
            controls=[
                ft.Container(
                    width=4,
                    height=24,
                    bgcolor=BRAND_CYAN,
                    border_radius=8,
                ),
                ft.Text(
                    text,
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=BRAND_SILVER,
                ),
            ],
            spacing=10,
        )
    ]
    if subtitle:
        controls.append(ft.Text(subtitle, size=13, color=BRAND_MUTED))
    return ft.Column(controls=controls, spacing=4)
