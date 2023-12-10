import sys
from os import path
import typing
from PyQt5 import (
    QtGui,
    uic,
)
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QToolTip,
    QPushButton,
    QToolButton,
    QMessageBox,
    QVBoxLayout,
    QSizePolicy,
    QWidget,
    QHBoxLayout,
    QLabel,
    QDesktopWidget,
    QGridLayout,
    QLineEdit,
    QStackedWidget,
    QGraphicsView,
    QGraphicsScene,
)
from PyQt5.QtGui import (
    QIcon,
    QFont,
    QKeyEvent,
    QCloseEvent,
)
from PyQt5.QtCore import (
    QCoreApplication,
    QPoint,
    Qt,
    QSize,
)

class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setGeometry(0, 0, 800, 480)
        self.setMinimumSize(400, 240)
        self.center()
        self.showFullScreen()
        
        self.keyPressEvent = self.handleKeyPress
        
        self.main_ui = uic.loadUi(path.join(path.dirname(__file__), 'resources', 'ui', 'main.ui'))
        self.main_ui.to_scan_btn.clicked.connect(self.showScan)
        self.main_ui.scan_skip_btn.clicked.connect(self.showResult)
        
        
        self.sel_ui = uic.loadUi(path.join(path.dirname(__file__), 'resources', 'ui', 'select.ui'))
        
        
        self.acne_ui = uic.loadUi(path.join(path.dirname(__file__), 'resources', 'ui', 'acne.ui'))
        self.acne_ui.acne_progress_bar.setValue(0) 
        #self.acne_ui.acne_media = QGraphicsView()
        self.acne_ui.acne_media.setScene(QGraphicsScene())
        self.acne_ui.acne_media.scene().addPixmap(QtGui.QPixmap(path.join(path.dirname(__file__), 'resources', 'images', 'acne.png')))
        #self.acne_ui.acne_media.fitInView(self.acne_ui.acne_media.scene().sceneRect(), Qt.KeepAspectRatio)
        self.acne_ui.acne_media.setRenderHint(QtGui.QPainter.Antialiasing)
        self.acne_ui.acne_media.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        self.acne_ui.acne_media.setRenderHint(QtGui.QPainter.TextAntialiasing)
        
        
        self.result_ui = uic.loadUi(path.join(path.dirname(__file__), 'resources', 'ui', 'result.ui'))
        
        
        self.stacked = QStackedWidget()
        self.stacked.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.stacked.addWidget(self.main_ui)
        self.stacked.addWidget(self.sel_ui)
        self.stacked.addWidget(self.acne_ui)
        self.stacked.addWidget(self.result_ui)
        
        self.stacked.setCurrentIndex(0)
        self.setLayout(QGridLayout())
        self.layout().addWidget(self.stacked)
        
        
        self.sel_ui.acne_scan_btn.clicked.connect(self.showAcneScan)
        self.sel_ui.cancer_scan_btn.clicked.connect(self.showCancerScan)
        
        self.show()
    
    def showResult(self):
        self.stacked.setCurrentIndex(3)
        print("Results")
    
    def showScan(self):
        self.stacked.setCurrentIndex(1)
        print("Scan")
        
    def showAcneScan(self):
        self.stacked.setCurrentIndex(2)
        print("Acne Scan")
        
    def showCancerScan(self):
        print("Cancer Scan")
    
    def handleKeyPress(self, event: QKeyEvent):
        if event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        elif event.key() == Qt.Key_Escape:
            msg = QMessageBox()
            msg.setWindowTitle("Quit")
            msg.setText("Are you sure you want to quit?")
            msg.setIcon(QMessageBox.Question)
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.setDefaultButton(QMessageBox.Yes)
            msg.setEscapeButton(QMessageBox.No)
            msg.buttonClicked.connect(self.quit)
            msg.exec_()
        else:
            super().keyPressEvent(event)
            
    def quit(self, button):
        if button.text() == "&Yes":
            QCoreApplication.instance().quit()
    
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(path.join(path.dirname(__file__), 'resources', 'images', 'web.png')))
    window = MainWindow()
    window.setWindowTitle("Skin Cancer Detection")
    sys.exit(app.exec_())