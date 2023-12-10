import sys
from os import path
import typing
import cv2
import threading
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
        self.runcam = False
        self.setGeometry(0, 0, 800, 480)
        self.setMinimumSize(400, 240)
        self.center()
        self.showFullScreen()
        
        self.keyPressEvent = self.handleKeyPress
        
        self.main_ui = uic.loadUi(path.join(path.dirname(__file__), 'resources', 'ui', 'main.ui'))
        self.main_ui.to_scan_btn.clicked.connect(self.showScan)
        self.main_ui.scan_skip_btn.clicked.connect(self.showResult)
        
        
        self.sel_ui = uic.loadUi(path.join(path.dirname(__file__), 'resources', 'ui', 'select.ui'))
        self.sel_ui.to_back_btn.clicked.connect(self.showMain)
        self.sel_ui.acne_scan_btn.clicked.connect(self.showAcneScan)
        self.sel_ui.cancer_scan_btn.clicked.connect(self.showCancerScan)
        
        
        self.acne_ui = uic.loadUi(path.join(path.dirname(__file__), 'resources', 'ui', 'acne.ui'))
        self.acne_ui.to_back_btn.clicked.connect(self.showScan)
        self.acne_ui.acne_progress_bar.setValue(0) 
        #self.acne_ui.acne_media = QGraphicsView()
        
        
        
        self.result_ui = uic.loadUi(path.join(path.dirname(__file__), 'resources', 'ui', 'result.ui'))
        self.result_ui.to_back_btn.clicked.connect(self.showMain)
        
        
        self.stacked = QStackedWidget()
        self.stacked.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.stacked.addWidget(self.main_ui)
        self.stacked.addWidget(self.sel_ui)
        self.stacked.addWidget(self.acne_ui)
        self.stacked.addWidget(self.result_ui)
        
        self.stacked.setCurrentIndex(0)
        self.setLayout(QGridLayout())
        self.layout().addWidget(self.stacked)
        
        self.show()
    
    def showMain(self):
        self.stacked.setCurrentIndex(0)
    
    def showResult(self):
        self.stacked.setCurrentIndex(3)
        print("Results")
    
    def showScan(self):
        self.runcam = False
        self.stacked.setCurrentIndex(1)
        print("Scan")
    
    def camera(self):
        cap = cv2.VideoCapture(0)
        ow = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        oh = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        #self.acne_ui.acne_media.resize(int(width), int(height))
        #self.acne_ui.acne_media: QLabel = self.acne_ui.acne_media
        
        while self.runcam:
            ret, img = cap.read()
            
            if ret:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                size = self.acne_ui.acne_media.size()
                w = size.width()
                h = size.height()
                if ow > oh:
                    h = int(w * oh / ow)
                else:
                    w = int(h * ow / oh)
                img = cv2.resize(img, (w, h))
                
                h, w, c = img.shape
                qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(qImg)
                self.acne_ui.acne_media.setPixmap(pixmap)
            else:
                print('cant read frame')
                break
        cap.release()
        self.acne_ui.acne_media.clear()
        
    def showAcneScan(self):
        self.runcam = True
        self.camth = threading.Thread(target=self.camera)
        self.camth.start()
        self.stacked.setCurrentIndex(2)
        
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
    app.exec_()
    window.runcam = False
    sys.exit(0)