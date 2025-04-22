import flet as ft
import asyncio
from datetime import datetime

def main(page: ft.Page):
    page.title = "Placar de Vôlei com Sets"
    page.window_min_width = 600
    page.window_min_height = 350
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.scroll = "auto"
    page.bgcolor = "#121212"

    start_time = None
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

    now_text = ft.Text("Agora: --/--/---- --:--:--", size=16, color="white")
    start_time_text = ft.Text("Início: --:--:--", size=16, color="white")
    duration_text = ft.Text("Duração: 00:00:00", size=16, color="white")

    team_a_name = ft.TextField(
        value="Time Azul", text_align="center", text_size=30,
        color="white", bgcolor="#1E88E5", border_color="transparent"
    )
    score_a = ft.Text("0", size=120, color="white", weight="bold", text_align="center")
    sets_a = ft.Text("Sets: 0", size=20, color="white")
    sets_a_value = 0
    add_a = ft.IconButton(icon="add_circle", icon_size=50)
    remove_a = ft.IconButton(icon="remove_circle", icon_size=50)
    add_set_a = ft.IconButton(icon="add_box", icon_size=30, icon_color="#1565C0")
    remove_set_a = ft.IconButton(icon="indeterminate_check_box", icon_size=30, icon_color="#1565C0")

    team_b_name = ft.TextField(
        value="Time Vermelho", text_align="center", text_size=30,
        color="white", bgcolor="#E53935", border_color="transparent"
    )
    score_b = ft.Text("0", size=120, color="white", weight="bold", text_align="center")
    sets_b = ft.Text("Sets: 0", size=20, color="white")
    sets_b_value = 0
    add_b = ft.IconButton(icon="add_circle", icon_size=50, icon_color="#FA8072")
    remove_b = ft.IconButton(icon="remove_circle", icon_size=50, icon_color="#FA8072")
    add_set_b = ft.IconButton(icon="add_box", icon_size=30, icon_color="#EF5350")
    remove_set_b = ft.IconButton(icon="indeterminate_check_box", icon_size=30, icon_color="#EF5350")

    async def update_time():
        while True:
            now = datetime.now()
            dia_semana = dias_semana[now.weekday()]
            now_text.value = f"Agora: {dia_semana} - {now.strftime('%d/%m/%Y %H:%M:%S')}"
            if start_time:
                dur = datetime.now() - start_time
                duration_text.value = f"Duração: {str(dur).split('.')[0]}"
            page.update()
            await asyncio.sleep(1)

    page.run_task(update_time)

    def add_point(score):
        def action(e):
            nonlocal start_time
            if start_time is None:
                start_time = datetime.now()
                start_time_text.value = f"Início: {start_time.strftime('%H:%M:%S')}"
            score.value = str(int(score.value) + 1)
            page.update()
        return action

    def remove_point(score):
        def action(e):
            score.value = str(max(0, int(score.value) - 1))
            page.update()
        return action

    def add_set(sets_label, is_team_a=True):
        def action(e):
            nonlocal sets_a_value, sets_b_value
            if is_team_a:
                sets_a_value += 1
                sets_label.value = f"Sets: {sets_a_value}"
            else:
                sets_b_value += 1
                sets_label.value = f"Sets: {sets_b_value}"
            page.update()
        return action

    def remove_set(sets_label, is_team_a=True):
        def action(e):
            nonlocal sets_a_value, sets_b_value
            if is_team_a and sets_a_value > 0:
                sets_a_value -= 1
                sets_label.value = f"Sets: {sets_a_value}"
            elif not is_team_a and sets_b_value > 0:
                sets_b_value -= 1
                sets_label.value = f"Sets: {sets_b_value}"
            page.update()
        return action

    def reset_all(e):
        nonlocal start_time, sets_a_value, sets_b_value
        score_a.value = "0"
        score_b.value = "0"
        sets_a_value = 0
        sets_b_value = 0
        sets_a.value = "Sets: 0"
        sets_b.value = "Sets: 0"
        start_time = None
        start_time_text.value = "Início: --:--:--"
        duration_text.value = "Duração: 00:00:00"
        page.update()

    add_a.on_click = add_point(score_a)
    remove_a.on_click = remove_point(score_a)
    add_b.on_click = add_point(score_b)
    remove_b.on_click = remove_point(score_b)
    add_set_a.on_click = add_set(sets_a, True)
    remove_set_a.on_click = remove_set(sets_a, True)
    add_set_b.on_click = add_set(sets_b, False)
    remove_set_b.on_click = remove_set(sets_b, False)

    left_column = ft.Container(
        bgcolor="#1E88E5",
        border_radius=10,
        padding=10,
        expand=True,
        content=ft.Column([
            team_a_name,
            ft.Container(score_a, alignment=ft.alignment.center, expand=True),
            ft.Row([add_a, remove_a], alignment="center", spacing=50),
            ft.Row([sets_a, add_set_a, remove_set_a], alignment="center", spacing=10),
        ], spacing=10, expand=True)
    )

    right_column = ft.Container(
        bgcolor="#E53935",
        border_radius=10,
        padding=10,
        expand=True,
        content=ft.Column([
            team_b_name,
            ft.Container(score_b, alignment=ft.alignment.center, expand=True),
            ft.Row([add_b, remove_b], alignment="center", spacing=50),
            ft.Row([sets_b, add_set_b, remove_set_b], alignment="center", spacing=10),
        ], spacing=10, expand=True)
    )

    placar_layout = ft.Row(
        [left_column, right_column],
        expand=True,
        spacing=20,
        vertical_alignment="center",
    )

    infos_layout = ft.ResponsiveRow([
        ft.Container(
            ft.ElevatedButton(
                "Zerar Valores", on_click=reset_all,
                bgcolor="#333333", color="white",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6)),
                height=45
            ),
            col={"xs": 12, "sm": 6, "md": 3},
            alignment=ft.alignment.center
        ),
        ft.Container(now_text, col={"xs": 12, "sm": 6, "md": 3}, alignment=ft.alignment.center),
        ft.Container(start_time_text, col={"xs": 12, "sm": 6, "md": 3}, alignment=ft.alignment.center),
        ft.Container(duration_text, col={"xs": 12, "sm": 6, "md": 3}, alignment=ft.alignment.center),
    ], spacing=10)

    page.add(
        ft.Column(
            [
                ft.Container(placar_layout, expand=True),
                infos_layout
            ],
            expand=True,
            spacing=15,
        )
    )

ft.app(target=main)
