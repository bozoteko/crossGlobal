import sys
import json
from PyQt5 import QtWidgets, QtCore, QtGui
from crosshair import Crosshair

class CrosshairPreview(QtWidgets.QWidget):
    def __init__(self, crosshair_widget, parent=None):
        super().__init__(parent)
        self.crosshair = crosshair_widget
        self.setFixedSize(200, 200)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        self.crosshair.drawCrosshair(painter, self.rect().center())

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, crosshair_widget, tray_icon, parent=None):
        super().__init__(parent)
        self.crosshair = crosshair_widget
        self.tray_icon = tray_icon

        self.createWidgets()
        self.createLayout()

        self.setWindowTitle("crossGlobal Settings")
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)  # Remove the "?" from title bar

        # Initialize shortcut with Alt+X to toggle visibility
        self.toggleShortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.ALT + QtCore.Qt.Key_X), self)
        self.toggleShortcut.activated.connect(self.toggleVisibility)

        # Connect tray icon activation to show the settings dialog
        self.tray_icon.activated.connect(self.onTrayIconActivated)

        # Create context menu for tray icon
        self.createTrayIconMenu()

        # Load settings
        self.loadSettings()

    def createWidgets(self):
        self.crosshairSizeSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.crosshairSizeSlider.setMinimum(8)
        self.crosshairSizeSlider.setMaximum(64)
        self.crosshairSizeSlider.setValue(self.crosshair.ws)
        self.crosshairSizeSlider.setTickInterval(4)
        self.crosshairSizeSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.crosshairSizeSlider.valueChanged.connect(self.updatePreview)

        self.crosshairWidthSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.crosshairWidthSlider.setMinimum(1)
        self.crosshairWidthSlider.setMaximum(10)
        self.crosshairWidthSlider.setValue(self.crosshair.crosshairWidth)
        self.crosshairWidthSlider.setTickInterval(1)
        self.crosshairWidthSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.crosshairWidthSlider.valueChanged.connect(self.updatePreview)

        self.crossLengthSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.crossLengthSlider.setMinimum(1)
        self.crossLengthSlider.setMaximum(20)
        self.crossLengthSlider.setValue(self.crosshair.crossLength)
        self.crossLengthSlider.setTickInterval(1)
        self.crossLengthSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.crossLengthSlider.valueChanged.connect(self.updatePreview)

        self.xLengthSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.xLengthSlider.setMinimum(1)
        self.xLengthSlider.setMaximum(20)
        self.xLengthSlider.setValue(self.crosshair.xLength)
        self.xLengthSlider.setTickInterval(1)
        self.xLengthSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.xLengthSlider.valueChanged.connect(self.updatePreview)

        self.colorButton = QtWidgets.QPushButton("Choose Color")
        self.colorButton.clicked.connect(self.chooseColor)

        self.toggleOutlineCheckbox = QtWidgets.QCheckBox("Show Outline")
        self.toggleOutlineCheckbox.setChecked(self.crosshair.showOutline)
        self.toggleOutlineCheckbox.stateChanged.connect(self.updatePreview)

        self.styleComboBox = QtWidgets.QComboBox()
        self.styleComboBox.addItems(["Cross", "X", "Dot", "Custom Image"])
        self.styleComboBox.setCurrentText("Cross")
        self.styleComboBox.currentIndexChanged.connect(self.updatePreview)

        self.customImageButton = QtWidgets.QPushButton("Choose Image")
        self.customImageButton.clicked.connect(self.chooseImage)
        self.customImageButton.setEnabled(False)

        self.toggleCrosshairButton = QtWidgets.QPushButton("Toggle Crosshair")
        self.toggleCrosshairButton.clicked.connect(self.toggleCrosshair)

        self.applyButton = QtWidgets.QPushButton("Apply")
        self.applyButton.clicked.connect(self.applyChanges)
        self.saveButton = QtWidgets.QPushButton("Save Settings")
        self.saveButton.clicked.connect(self.saveSettings)
        self.closeButton = QtWidgets.QPushButton("Close")
        self.closeButton.clicked.connect(self.close)

        self.preview = CrosshairPreview(self.crosshair)

    def createLayout(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(QtWidgets.QLabel("Crosshair Size"))
        self.layout.addWidget(self.crosshairSizeSlider)
        self.layout.addWidget(QtWidgets.QLabel("Crosshair Width"))
        self.layout.addWidget(self.crosshairWidthSlider)
        self.layout.addWidget(QtWidgets.QLabel("Cross Length"))
        self.layout.addWidget(self.crossLengthSlider)
        self.layout.addWidget(QtWidgets.QLabel("X Length"))
        self.layout.addWidget(self.xLengthSlider)
        self.layout.addWidget(self.colorButton)
        self.layout.addWidget(self.toggleOutlineCheckbox)
        self.layout.addWidget(QtWidgets.QLabel("Crosshair Style"))
        self.layout.addWidget(self.styleComboBox)
        self.layout.addWidget(self.customImageButton)
        self.layout.addWidget(self.preview)
        self.layout.addWidget(self.toggleCrosshairButton)
        self.layout.addWidget(self.applyButton)
        self.layout.addWidget(self.saveButton)
        self.layout.addWidget(self.closeButton)

        self.setLayout(self.layout)

    def createTrayIconMenu(self):
        self.tray_menu = QtWidgets.QMenu()
        show_action = self.tray_menu.addAction("Show Settings")
        show_action.triggered.connect(self.show)
        quit_action = self.tray_menu.addAction("Quit")
        quit_action.triggered.connect(QtWidgets.qApp.quit)
        self.tray_icon.setContextMenu(self.tray_menu)

    def updatePreview(self):
        style = self.styleComboBox.currentText().lower()
        if style == "custom image":
            self.customImageButton.setEnabled(True)
        else:
            self.customImageButton.setEnabled(False)

        self.crosshair.setCrosshairSize(self.crosshairSizeSlider.value())
        self.crosshair.setCrosshairWidth(self.crosshairWidthSlider.value())
        self.crosshair.setCrossLength(self.crossLengthSlider.value())
        self.crosshair.setXLength(self.xLengthSlider.value())
        self.crosshair.toggleOutline(self.toggleOutlineCheckbox.isChecked())
        self.crosshair.setCrosshairStyle(style)
        self.preview.update()

    def chooseColor(self):
        color = QtWidgets.QColorDialog.getColor(self.crosshair.crosshairColor, self, "Choose Color")
        if color.isValid():
            self.crosshair.setCrosshairColor(color)
            self.updatePreview()

    def chooseImage(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Choose Custom Crosshair Image", "", "Images (*.png *.xpm *.jpg)", options=options)
        if fileName:
            self.crosshair.setCustomImage(fileName)
            self.updatePreview()

    def toggleCrosshair(self):
        self.crosshair.toggleVisibility()

    def applyChanges(self):
        self.crosshair.setCrosshairSize(self.crosshairSizeSlider.value())
        self.crosshair.setCrosshairWidth(self.crosshairWidthSlider.value())
        self.crosshair.setCrossLength(self.crossLengthSlider.value())
        self.crosshair.setXLength(self.xLengthSlider.value())
        self.crosshair.toggleOutline(self.toggleOutlineCheckbox.isChecked())
        self.crosshair.setCrosshairColor(self.crosshair.crosshairColor)
        self.crosshair.setCrosshairStyle(self.styleComboBox.currentText().lower())
        self.crosshair.setCustomImage(self.crosshair.customImagePath)

    def saveSettings(self):
        settings = {
            'size': self.crosshairSizeSlider.value(),
            'width': self.crosshairWidthSlider.value(),
            'cross_length': self.crossLengthSlider.value(),
            'x_length': self.xLengthSlider.value(),
            'color': self.crosshair.crosshairColor.name(),
            'show_outline': self.toggleOutlineCheckbox.isChecked(),
            'style': self.styleComboBox.currentText().lower(),
            'custom_image': self.crosshair.customImagePath
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

    def loadSettings(self):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.crosshairSizeSlider.setValue(settings.get('size', 24))
                self.crosshairWidthSlider.setValue(settings.get('width', 1))
                self.crossLengthSlider.setValue(settings.get('cross_length', 10))
                self.xLengthSlider.setValue(settings.get('x_length', 10))
                self.crosshair.setCrosshairColor(QtGui.QColor(settings.get('color', '#FFFFFF')))
                self.toggleOutlineCheckbox.setChecked(settings.get('show_outline', False))
                self.styleComboBox.setCurrentText(settings.get('style', 'cross').capitalize())
                self.crosshair.setCustomImage(settings.get('custom_image', ''))
                self.updatePreview()
        except FileNotFoundError:
            pass

    def toggleVisibility(self):
        if self.isVisible():
            self.hide()
            self.tray_icon.show()
        else:
            self.show()
            self.tray_icon.hide()

    def keyPressEvent(self, event):
        if event.modifiers() == QtCore.Qt.AltModifier and event.key() == QtCore.Qt.Key_X:
            self.toggleVisibility()
        elif event.key() == QtCore.Qt.Key_Escape:
            self.hide()
        else:
            event.ignore()

    def onTrayIconActivated(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.toggleVisibility()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    crosshairWidget = Crosshair(initialSize=24)

    # Create the tray icon
    trayIcon = QtWidgets.QSystemTrayIcon(QtGui.QIcon("icon.png"), parent=app)
    trayIcon.setToolTip("CrossGlobal")

    # Create settings dialog
    settingsDialog = SettingsDialog(crosshairWidget, trayIcon)
    settingsDialog.show()

    sys.exit(app.exec_())
