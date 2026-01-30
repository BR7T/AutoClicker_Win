from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtGui import QGuiApplication
import sys
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QGuiApplication

class Overlay(QWidget):
    def __init__(self , positions):
        super().__init__()
        self.positions = positions

        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.Tool
        ) 
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        virtual = QGuiApplication.primaryScreen().virtualGeometry()
        self.setGeometry(virtual)
    # --------------

    
    def paintEvent(self , event):
        print(self.positions)
        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)

        painter.setBrush(QColor(255,255,255))

        radius = 8

        for idx,(x,y) in enumerate(self.positions , start=1):
            vx = x - self.geometry().x()
            vy = y - self.geometry().y()
            painter.drawEllipse(vx - radius , vy - radius , radius * 2 , radius * 2)

            painter.setPen(Qt.black)
            painter.drawText(
                vx - 3 ,
                vy + 4,
                str(idx)
            )

    

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QTimer


from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QCursor

class MouseLabel(QLabel):
    def __init__(self, state):
        super().__init__()

        self.State = state

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.Tool |
            Qt.WindowStaysOnTopHint
        )

        self.setAttribute(Qt.WA_TranslucentBackground , False)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        # 🎨 Estilo moderno (glass / HUD)
        self.setStyleSheet("""
            QLabel {
                background-color: rgba(20,20,20,220);
                border: 1px solid rgba(255,255,255,40);
                color: #F1F1F1;
                padding: 12px 14px;
                border-radius: 14px;
                font-size: 16px;
                font-family: Segoe UI;
            }
        """)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(16)  # ~60 FPS (mais suave, menos custo)

        self.show()

    def update_position(self):
        pos = QCursor.pos()

        status = "🟢 ATIVO" if self.State.running else "⚪ PARADO"

        self.setText(
            f"<b>🖱 AutoClicker</b><br>"
            f"<hr style='border:0;border-top:1px solid rgba(255,255,255,40);'>"
            f"📍 <b>X:</b> {pos.x()} &nbsp;&nbsp; <b>Y:</b> {pos.y()}<br>"
            f"⏱ <b>Delay:</b> {round(self.State.click_delay, 2)} s<br>"
            f"🔁 <b>Status:</b> {status}<br><br>"
            f"<span style='color:#AAAAAA;'>"
            f"Ctrl + Clique → adicionar ponto<br>"
            f"Shift Direito → iniciar<br>"
            f"Esc → parar</span>"
        )

        self.adjustSize()
        if self.State.running:
            higherX = max(x for x, _ in self.State.position)
            middleY = sum(y for _, y in self.State.position) // len(self.State.position)

            screen = QGuiApplication.screenAt(QPoint(higherX, middleY))
            if screen:
                geo = screen.availableGeometry()
                x = min(higherX + 20, geo.right() - self.width())
                y = max(geo.top(), middleY - self.height() // 2)
                self.move(x, y)
        else:
            self.move(pos.x() + 18, pos.y() + 18)