import sys,os,re,cv2,numpy as np,time,pyqtgraph as pg,subprocess,matplotlib.pyplot as plt,itertools
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime
from PyQt6.QtGui import QFont,QAction,QImage,QPixmap,QPixmapCache
from PyQt6.QtWidgets import QApplication,QWidget,QMenuBar,QMenu,QStatusBar,QMessageBox,QMainWindow,QFileDialog,QFrame,QLabel,QComboBox,QLineEdit,QPushButton,QHBoxLayout,QVBoxLayout,QScrollArea,QGridLayout
from PyQt6.QtCore import pyqtSignal,pyqtSlot,Qt,QRect,QCoreApplication,QMetaObject,QTimer,QObject,QThread
app = QApplication(sys.argv)
screen = app.primaryScreen()
size = screen.size()
rect = screen.availableGeometry()
AVAILABLE_WIDTH = rect.width()
AVAILABLE_HEIGHT = rect.height()
WIDTH_GRID_ITEM_VIEW = ((AVAILABLE_WIDTH - AVAILABLE_WIDTH // 10)// 2) + AVAILABLE_WIDTH // 1000
HEIGHT_GRID_ITEM_VIEW = ((AVAILABLE_HEIGHT - AVAILABLE_HEIGHT // 10) // 2) + AVAILABLE_HEIGHT // 10
WIDTH_GRID_ITEM_VIEW_LIVE = ((AVAILABLE_WIDTH - AVAILABLE_WIDTH // 10)) + AVAILABLE_WIDTH // 1000
HEIGHT_GRID_ITEM_VIEW_LIVE = ((AVAILABLE_HEIGHT - AVAILABLE_HEIGHT // 10)) + AVAILABLE_HEIGHT // 10
RUN_TIME_THREAD_LIMITATION = 3600
RUN_TIME_DIALOGUE_STOP_THREAD = RUN_TIME_THREAD_LIMITATION * 1000
WORK_SPACE_DIR = "C:/ZZ-IROST-CAMERA-ANALYZER/"
I_AND_P_FRAMES_DIR = WORK_SPACE_DIR + "I-AND-P-FRAMES/"
ENABLE_MENU_DELAY = 20
MIN_SHOW_FRAME = 200
MAX_SHOW_FRAME = MIN_SHOW_FRAME * 10
RESCALE_SIZE_FOR_WDR = 4
APP_NAME = "IROST Camera Analyzer"
custom_font = QFont("Calibri", 14)
app.setFont(custom_font, "QLabel")
app.setFont(custom_font, "QPushButton")
app.setFont(custom_font, "QComboBox")
app.setFont(custom_font, "QComboBox")
app.setFont(custom_font, "QLineEdit")
app.setFont(custom_font, "QMenu")
class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
    def showLoginView(self):
        from login_model import LoginModel
        from login_controller import LoginController
        from login_view import LoginView
        login_model = LoginModel()
        login_controller = LoginController(login_model)
        login_view = LoginView(login_model, login_controller)
        login_view.show()
    def makeWorkSpaceDirectory(self):
        if not os.path.exists(WORK_SPACE_DIR):
            os.makedirs(WORK_SPACE_DIR)
        if not os.path.exists(I_AND_P_FRAMES_DIR):
            os.makedirs(I_AND_P_FRAMES_DIR)
if __name__ == '__main__':   
    app = App(sys.argv)
    app.makeWorkSpaceDirectory()
    from main_view import MainView
    main_view = MainView()
    main_view.show()
    sys.exit(app.exec())