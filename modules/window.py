from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)
from .app import app

WIDTH_WINDOW = 1024
HEIGHT_WINDOW = 800
SQUARE_SIZE = 40

main_window = QMainWindow()
main_window.setWindowTitle("Weather app")
main_window.setStyleSheet("background-color: #2b2d30;")

# Центрування вікна на екрані
primary_screen = app.primaryScreen()
screen_size = primary_screen.size()
width_screen = screen_size.width()
height_screen = screen_size.height()

main_window.setGeometry(
    (width_screen // 2) - (WIDTH_WINDOW // 2),
    (height_screen // 2) - (HEIGHT_WINDOW // 2),
    WIDTH_WINDOW,
    HEIGHT_WINDOW,
)

central = QWidget(parent=main_window)
main_window.setCentralWidget(central)

main_layout = QVBoxLayout(central)
main_layout.setContentsMargins(0, 0, 0, 0)
main_layout.setSpacing(0)

# Список створених фреймів
frames: list[QFrame] = []


def update_counter():
    counter_label.setText(f"Всього фреймів: {len(frames)}")


def clear_frames():
    for sq in frames:
        sq.deleteLater()
    frames.clear()
    update_counter()


class CanvasArea(QFrame):
    def init(self, parent=None):
        super().init(parent)
        self.setStyleSheet("background-color: #e8eef2; border: none;")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position().toPoint()
            # Центруємо квадрат відносно курсора та не виходимо за межі полотна
            x = max(0, min(pos.x() - SQUARE_SIZE // 2, self.width() - SQUARE_SIZE))
            y = max(0, min(pos.y() - SQUARE_SIZE // 2, self.height() - SQUARE_SIZE))

            square = QFrame(self)
            square.setFixedSize(SQUARE_SIZE, SQUARE_SIZE)
            square.setStyleSheet("background-color: #0b84d8; border: none;")
            square.move(x, y)
            square.show()

            frames.append(square)
            update_counter()
        super().mousePressEvent(event)


def handle_key_press(event):
    if event.key() == Qt.Key.Key_Escape:
        clear_frames()
    QMainWindow.keyPressEvent(main_window, event)


main_window.keyPressEvent = handle_key_press

# 1. Світле полотно для додавання фреймів
canvas = CanvasArea()
main_layout.addWidget(canvas, stretch=1)

# 2. Нижня інформаційна панель
bottom_bar = QFrame()
bottom_bar.setStyleSheet("background-color: #2b2d30; border: none;")

bottom_layout = QVBoxLayout(bottom_bar)
bottom_layout.setContentsMargins(15, 10, 15, 12)
bottom_layout.setSpacing(6)

hint_label = QLabel("Ліва кнопка миші - додати фрейм, Escape: очистити")
hint_label.setStyleSheet("color: #e6e6e6; font-size: 13px;")

counter_label = QLabel("Всього фреймів: 0")
counter_label.setStyleSheet("color: #e6e6e6; font-size: 13px;")

bottom_layout.addWidget(hint_label)
bottom_layout.addWidget(counter_label)

main_layout.addWidget(bottom_bar)

# Показуємо вікно
main_window.show()