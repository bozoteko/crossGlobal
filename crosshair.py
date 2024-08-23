import sys
from PyQt5 import QtWidgets, QtCore, QtGui

class Crosshair(QtWidgets.QWidget):
    def __init__(self, parent=None, initialSize=24):
        super().__init__(parent)
        self.ws = initialSize
        self.crosshairStyle = 'cross'
        self.crosshairWidth = 2
        self.crosshairColor = QtGui.QColor(255, 255, 255)  # Default color is white
        self.showOutline = True
        self.pen = QtGui.QPen(self.crosshairColor)
        self.pen.setWidth(self.crosshairWidth)
        self.visible = True
        self.crossLength = 10
        self.xLength = 10
        self.customImagePath = None  # Path to custom image
        self.customImage = None  # QPixmap for custom image
        self.setWindowFlags(
            QtCore.Qt.Tool |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.WindowTransparentForInput
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.centerOnScreen()

    def centerOnScreen(self):
        self.resize(self.ws + 1, self.ws + 1)
        screenRect = QtWidgets.QApplication.desktop().screen().rect()
        self.move(screenRect.center() - self.rect().center())

    def setCrosshairSize(self, size):
        self.ws = size
        self.centerOnScreen()

    def setCrosshairWidth(self, width):
        self.crosshairWidth = width
        self.pen.setWidth(self.crosshairWidth)
        self.update()

    def setCrosshairColor(self, color):
        self.crosshairColor = color
        self.pen.setColor(self.crosshairColor)
        self.update()

    def toggleOutline(self, state):
        self.showOutline = state
        self.update()

    def setCrosshairStyle(self, style):
        self.crosshairStyle = style
        self.update()

    def setCrossLength(self, length):
        self.crossLength = length
        self.update()

    def setXLength(self, length):
        self.xLength = length
        self.update()

    def setCustomImage(self, imagePath):
        self.customImagePath = imagePath
        if imagePath:
            self.customImage = QtGui.QPixmap(imagePath)
        else:
            self.customImage = None
        self.update()

    def toggleVisibility(self):
        self.visible = not self.visible
        self.setVisible(self.visible)

    def drawCrosshair(self, painter, center):
        ws = self.ws
        res = int(ws / 2)
        red = self.crossLength if self.crosshairStyle == 'cross' else self.xLength
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # Draw custom image if set
        if self.customImage and self.crosshairStyle == 'custom image':
            painter.drawPixmap(center.x() - self.customImage.width() // 2, center.y() - self.customImage.height() // 2, self.customImage)
            return

        # Draw crosshair based on selected style
        painter.setPen(self.pen)
        if self.crosshairStyle == 'cross':
            painter.drawLine(center.x(), center.y() - red, center.x(), center.y() + red)
            painter.drawLine(center.x() - red, center.y(), center.x() + red, center.y())
        
        elif self.crosshairStyle == 'x':
            painter.drawLine(center.x() - red, center.y() - red, center.x() + red, center.y() + red)
            painter.drawLine(center.x() - red, center.y() + red, center.x() + red, center.y() - red)

        elif self.crosshairStyle == 'dot':
            painter.drawPoint(center)

        # Draw outline around crosshair
        if self.showOutline:
            outlineColor = QtGui.QColor(0, 0, 0, 100)
            outlinePen = QtGui.QPen(outlineColor, 2, QtCore.Qt.SolidLine)
            painter.setPen(outlinePen)
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.drawEllipse(QtCore.QRectF(center.x() - res + 0.5, center.y() - res + 0.5, ws - 1, ws - 1))

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        self.drawCrosshair(painter, self.rect().center())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    crosshairWidget = Crosshair(initialSize=24)
    crosshairWidget.show()

    sys.exit(app.exec_())
