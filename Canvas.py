from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, 
                             QVBoxLayout, QLabel, QPushButton, QHBoxLayout, 
                             QSizePolicy, QTabWidget)
from PyQt6.QtGui import QPainter, QColor, QPen, QPixmap, QKeyEvent
from PyQt6.QtCore import Qt, QTimer, QPoint
from GlobalVariableAccess import *

class Canvas(QWidget):
    # Initalizing class variables
    KEY_CONTROLS = {
        "up": False,
        "down": False,
        "left": False,
        "right": False
    }
    position = [0, 0]

    solar_data_change = True

    drawableWaypoints = []

    def __init__(self, width = 600, height = 400, parent=None):
        super().__init__(parent)

        # defining canvas behavior
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFixedSize(width, height)

        # defining canvas properties
        self.width = width
        self.height = height
        self.CENTER_POINT = [self.width/2, self.height/2]

        # defining the canvas
        self.pixmap = QPixmap(self.width, self.height)
        self.pixmap.fill(QColor("black"))

        # Drawing state
        self.drawing = False
        self.last_point = QPoint()
        self.pen = QPen(QColor("white"), 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)

        # setting fps rate
        self.frames = 30
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(int(1000/30))
    
    @staticmethod
    def drawCircle(x: int, y: int, rad: int, color: str, pixmap):
        painter = QPainter(pixmap)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(color))
        painter.drawEllipse(QPoint(x, y), rad, rad)

    def paintEvent(self, event):
        # All painting on the widget is done here. We simply blit our backing pixmap,
        # then draw any transient overlays.

        # clearing pixmap
        self.pixmap.fill(QColor("black"))

        # set
        painter = QPainter(self)

        # system
        self.draw_current_system_waypoints()

        # blit 
        painter.drawPixmap(0, 0, self.pixmap)

        # text overlay
        painter.setPen(QColor("blue"))
        font = painter.font()
        font.setPointSize(12)
        painter.setFont(font)

        painter.drawText(50, self.height-50, "position: (" + str(self.position[0]) + "," + str(self.position[1]) + ")")  
        painter.end()
    
    def update_current_system_waypoints(self):
        print("hi")
        self.drawableWaypoints = []
        for waypoint in CURRENT_SYSTEM_WAYPOINTS:
            if (Canvas.withinRange(self.width, self.height, [self.position[0], self.position[1]], [waypoint["x"], waypoint["y"]], [10, 10], 25)):
                self.drawableWaypoints.append(waypoint)
        self.solar_data_change = False
    
    def draw_current_system_waypoints(self):
        if (self.solar_data_change):
            self.update_current_system_waypoints()
        for waypoint in self.drawableWaypoints:
            self.draw_waypoint(waypoint)
    
    def draw_waypoint(self, data):
        Canvas.drawCircle(data["x"] + int(self.CENTER_POINT[0] + self.position[0]), data["y"] + int(self.CENTER_POINT[1] + self.position[1]), 5, "white", self.pixmap)
    
    def _tick(self):
        self.detectEvents()
        self.update()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_W or event.key() == Qt.Key.Key_Up:
            self.KEY_CONTROLS["up"] = True
            self.solar_data_change = True
        if event.key() == Qt.Key.Key_S or event.key() == Qt.Key.Key_Down:
            self.KEY_CONTROLS["down"] = True
            self.solar_data_change = True
        if event.key() == Qt.Key.Key_A or event.key() == Qt.Key.Key_Left:
            self.KEY_CONTROLS["left"] = True
            self.solar_data_change = True
        if event.key() == Qt.Key.Key_D or event.key() == Qt.Key.Key_Right:
            self.KEY_CONTROLS["right"] = True
            self.solar_data_change = True
    
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key.Key_W or event.key() == Qt.Key.Key_Up:
            self.KEY_CONTROLS["up"] = False
        if event.key() == Qt.Key.Key_S or event.key() == Qt.Key.Key_Down:
            self.KEY_CONTROLS["down"] = False
        if event.key() == Qt.Key.Key_A or event.key() == Qt.Key.Key_Left:
            self.KEY_CONTROLS["left"] = False
        if event.key() == Qt.Key.Key_D or event.key() == Qt.Key.Key_Right:
            self.KEY_CONTROLS["right"] = False

    def detectEvents(self):
        if self.KEY_CONTROLS["left"]:
            self.position[0] += 5
        elif self.KEY_CONTROLS["right"]:
            self.position[0] -= 5
        if self.KEY_CONTROLS["up"]:
            self.position[1] += 5
        elif self.KEY_CONTROLS["down"]:
            self.position[1] -= 5
    
    @staticmethod
    def withinRange(Cwidth, Cheight, CPosition, position, ObjectDimen, pixelError):
        # the CPosition is the position of the top left corner
        # the position also uses top left corner
        if (position[0] >= CPosition[0] - Cwidth/2 and 
            position[1] >= CPosition[1] - Cheight/2 and 
            position[0] <= CPosition[0] + Cwidth/2 and 
            position[1] <= CPosition[1] + Cheight/2):
            return True # delete and redo
        return False