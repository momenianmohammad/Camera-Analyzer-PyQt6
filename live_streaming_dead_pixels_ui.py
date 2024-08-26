from app import *
class LiveStreamingDeadPixelsUI(QMainWindow):
    enable_menu_changed = pyqtSignal(bool)
    def __init__(self):
        super(LiveStreamingDeadPixelsUI, self).__init__()
        self.setupUi(self)
        self.initialzeValues()
    def initialzeValues(self):
        self._fps_once = 0
        self._res_w_once = 0
        self._res_h_once = 0
        self._codec_str = ""
        self._clicked_status = 1
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(AVAILABLE_WIDTH, AVAILABLE_HEIGHT)
        self.centralwidget = QWidget(Form)
        Form.setCentralWidget(self.centralwidget)
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, AVAILABLE_WIDTH, AVAILABLE_HEIGHT))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblCamera = QLabel(self.verticalLayoutWidget)
        self.lblCamera.setScaledContents(True)
        self.lblCamera.setObjectName("lblCamera")
        self.lblCamera.setMinimumSize(AVAILABLE_WIDTH, AVAILABLE_HEIGHT - AVAILABLE_HEIGHT // 4)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblShot1 = QLabel(self.verticalLayoutWidget)
        self.lblShot1.setScaledContents(True)
        self.lblShot1.setObjectName("lblShot1")
        self.lblShot1.setMinimumSize(AVAILABLE_WIDTH // 4, 0)
        self.lblMsgDeadPixelsStatus = QLabel(self.verticalLayoutWidget)
        self.lblMsgDeadPixelsStatus.setScaledContents(True)
        self.lblMsgDeadPixelsStatus.setObjectName("lblMsgDeadPixelsStatus")
        self.lblMsgDeadPixelsStatus.setMinimumSize(AVAILABLE_WIDTH // 2, 0)
        self.lblShot2 = QLabel(self.verticalLayoutWidget)
        self.lblShot2.setScaledContents(True)
        self.lblShot2.setObjectName("lblShot2")
        self.lblShot2.setMinimumSize(AVAILABLE_WIDTH // 4, 0)
        self.horizontalLayout.addWidget(self.lblShot1)
        self.horizontalLayout.addWidget(self.lblShot2)
        self.horizontalLayout.addWidget(self.lblMsgDeadPixelsStatus)
        self.btnAction = QPushButton(self.verticalLayoutWidget)
        self.btnAction.setObjectName("btnAction")
        self.btnAction.setMinimumSize(AVAILABLE_WIDTH, AVAILABLE_HEIGHT // 32)
        self.btnAction.setEnabled(False)
        self.btnAction.setVisible(False)
        self.btnAction.setHidden(True)
        self.btnAction.clicked.connect(self.actionClick)
        self.verticalLayout.addWidget(self.lblCamera)
        self.verticalLayout.addWidget(self.btnAction)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)
    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", APP_NAME))
        self.lblMsgDeadPixelsStatus.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
    def actionClick(self):
        self.lblCamera.setMinimumSize(AVAILABLE_WIDTH, AVAILABLE_HEIGHT // 2)
        self.lblMsgDeadPixelsStatus.setMinimumSize(AVAILABLE_WIDTH // 2, AVAILABLE_HEIGHT // 4)
        self.lblShot1.setMinimumSize(AVAILABLE_WIDTH // 4, AVAILABLE_HEIGHT // 4)
        self.lblShot2.setMinimumSize(AVAILABLE_WIDTH // 4, AVAILABLE_HEIGHT // 4)
        shot1 = []
        shot2 = []
        match self._clicked_status:
            case 1:
                self.btnAction.setText("Second Shot. Please completly change the situation of camera.")
                shot1 = self._last_frame
                qt_img = self.convert_cv_qt_last_frame(self._last_frame)
                self.lblShot1.setPixmap(qt_img)
            case 2:
                self.btnAction.setText("Calculate Dead Pixels")
                qt_img = self.convert_cv_qt_last_frame(self._last_frame)
                self.lblShot2.setPixmap(qt_img)
                shot2 = self._last_frame
            case 3:
                shot1_res = np.count_nonzero(shot1==0)
                shot2_res = np.count_nonzero(shot2==0)
                self.btnAction.setHidden(True)
                self.btnAction.setVisible(False)
                self.btnAction.setEnabled(False)
                self.lblMsgDeadPixelsStatus.setText("Number of Dead Pixels are: " + str(shot1_res + shot2_res))
            case _:
                return
        self._clicked_status = self._clicked_status + 1
    @pyqtSlot(int)
    def on_basic_info_just_sys_second(self, sys_second):
        if sys_second == ENABLE_MENU_DELAY // 3:
            self.enable_menu_changed.emit(True) 
    @pyqtSlot(list)
    def on_basic_info_once(self, data):             
        codec = data[0]
        self._codec_str = chr(codec&0xff) + chr((codec>>8)&0xff) + chr((codec>>16)&0xff) + chr((codec>>24)&0xff)
        self._fps_once = data[1]
        self._res_w_once = data[2]
        self._res_h_once = data[3]
        self.btnAction.setEnabled(True)
        self.btnAction.setVisible(True)
        self.btnAction.setHidden(False)
        self.btnAction.setText("First Shot")
    @pyqtSlot(np.ndarray)
    def on_streaming(self, cv_img):
        self._last_frame = cv_img
        qt_img = self.convert_cv_qt(cv_img)
        self.lblCamera.setPixmap(qt_img)
    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(int(self._res_w_once), int(self._res_h_once), Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(p)
    def convert_cv_qt_last_frame(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(int(self._res_w_once), int(self._res_h_once), Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(p)