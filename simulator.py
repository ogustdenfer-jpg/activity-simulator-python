import flet as ft
import pyautogui
import psutil
import time
import threading
import random

class ActivitySimulator:
    def __init__(self):
        self.target_window = ""
        self.interval = 45
        self.duration = 480  # в минутах
        self.simulate_typing = True
        self.simulate_scrolling = True
        self.simulate_mouse = True
        self.is_running = False
        self.timer_end = 0
        self.thread = None

    def simulate(self):
        self.timer_end = time.time() + (self.duration * 60)
        while self.is_running:
            if time.time() > self.timer_end:
                self.is_running = False
                break

            # Активировать окно
            for proc in psutil.process_iter(['pid', 'name']):
                if self.target_window.lower() in proc.info['name'].lower():
                    import pygetwindow as gw
                    windows = gw.getWindowsWithTitle(self.target_window)
                    if windows:
                        win = windows[0]
                        win.activate()
                        break

            if self.simulate_scrolling:
                pyautogui.press('pagedown')
                time.sleep(1)
                pyautogui.press('pageup')

            if self.simulate_mouse:
                x = random.randint(200, 800)
                y = random.randint(100, 500)
                pyautogui.moveTo(x, y, duration=0.5)
                pyautogui.click()

            if self.simulate_typing:
                text = ''.join([chr(random.randint(65, 90)) for _ in range(random.randint(5, 15))])
                pyautogui.typewrite(text)
                pyautogui.press('enter')
                for _ in text:
                    pyautogui.press('backspace')

            time.sleep(self.interval)

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self.simulate)
            self.thread.start()

    def pause(self):
        self.is_running = False

    def stop(self):
        self.is_running = False


def main(page: ft.Page):
    page.title = "Симулятор активности"
    page.window_width = 600
    page.window_height = 700
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    simulator = ActivitySimulator()

    # Элементы интерфейса
    window_field = ft.TextField(label="Название окна (например, Word)", value="Word")
    file_field = ft.TextField(label="Файл (необязательно)", value="C:\\path\\to\\file.docx")
    interval_field = ft.TextField(label="Интервал (сек)", value="45")
    duration_field = ft.TextField(label="Длительность (мин)", value="480")

    typing_check = ft.Checkbox(label="Имитировать печать", value=True)
    scrolling_check = ft.Checkbox(label="Имитировать прокрутку", value=True)
    mouse_check = ft.Checkbox(label="Имитировать мышь", value=True)

    status_text = ft.Text("Статус: Ожидание", size=16, weight=ft.FontWeight.BOLD)

    def update_status():
        if simulator.is_running:
            status_text.value = "Статус: Работает"
        else:
            status_text.value = "Статус: Остановлено"
        page.update()

    def start_sim(e):
        simulator.target_window = window_field.value
        simulator.interval = int(interval_field.value)
        simulator.duration = int(duration_field.value)
        simulator.simulate_typing = typing_check.value
        simulator.simulate_scrolling = scrolling_check.value
        simulator.simulate_mouse = mouse_check.value
        simulator.start()
        update_status()

    def pause_sim(e):
        simulator.pause()
        update_status()

    def stop_sim(e):
        simulator.stop()
        update_status()

    page.add(
        ft.Text("Симулятор активности", size=24, weight=ft.FontWeight.BOLD),
        window_field,
        file_field,
        interval_field,
        duration_field,
        typing_check,
        scrolling_check,
        mouse_check,
        ft.Row([
            ft.ElevatedButton("Запустить", on_click=start_sim),
            ft.ElevatedButton("Пауза", on_click=pause_sim),
            ft.ElevatedButton("Стоп", on_click=stop_sim),
        ]),
        status_text
    )


if __name__ == "__main__":
    ft.app(target=main)
