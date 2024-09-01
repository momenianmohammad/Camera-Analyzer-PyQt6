
from app import *
class LiveStreamingUI(QWidget):
    enable_menu_changed = pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._recording_time = 60
        self._start_recording_from_sec = 0
        self._fps_once = 0
        self._res_w_once = 0
        self._res_h_once = 0
        self._is_recording_btn = False
        self.flag_recording = False
        self._codec_str = ""
        self._sys_sec = 0
        self.reverse_timer = ENABLE_MENU_DELAY * 2
        self.flag_recording_on_enable_menu = True   
    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.verticalLayoutWidget = QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, WIDTH_GRID_ITEM_VIEW_LIVE , HEIGHT_GRID_ITEM_VIEW_LIVE - (HEIGHT_GRID_ITEM_VIEW_LIVE // 4)))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblCamera = QLabel(self.verticalLayoutWidget)
        self.lblCamera.setText("")
        self.lblCamera.setPixmap(QPixmap(self.resource_path("waiting.png")))
        self.lblCamera.setScaledContents(True)
        self.lblCamera.setObjectName("lblCamera")
        self.verticalLayout.addWidget(self.lblCamera)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnRecord = QPushButton(self.verticalLayoutWidget)
        self.btnRecord.setObjectName("btnRecord")
        self.horizontalLayout.addWidget(self.btnRecord)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)
    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", APP_NAME))
        self.btnRecord.setText(_translate("Form", "Record stream (Close another windows or softwares before starting)."))
        self.btnRecord.setEnabled(False)
        self.btnRecord.clicked.connect(self.btn_start_stop_recording_clicked)
    @pyqtSlot(np.ndarray)
    def on_streaming(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.recording(cv_img = cv_img)
        self.lblCamera.setPixmap(qt_img)
    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(int(self._res_w_once), int(self._res_h_once), Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(p)
    @pyqtSlot(int)
    def on_basic_info_just_sys_second(self, sys_second):
        if self.flag_recording_on_enable_menu == True and self._is_recording_btn == False:
            if sys_second == ENABLE_MENU_DELAY // 3:
                self.enable_menu_changed.emit(True)
        else: 
            self.enable_menu_changed.emit(False)
        self._start_recording_from_sec = sys_second
        if (sys_second > RUN_TIME_THREAD_LIMITATION):
            self.btnRecord.setEnabled(False)
            self.btnRecord.setVisible(False)
        if self._is_recording_btn:
            self._sys_sec = self._sys_sec + 1
            self.reverse_timer = self.reverse_timer - 1
            self.btnRecord.setEnabled(False)
            message = str(self._sys_sec) + " (s) is being record." if self._sys_sec < ENABLE_MENU_DELAY else str(self.reverse_timer) + " (s) wait for another record. " + "Video saved in: "  + self._dir + self._file_name
            self.btnRecord.setText(message)
            if self._sys_sec == ENABLE_MENU_DELAY:
                self.out.release()
            elif self._sys_sec == ENABLE_MENU_DELAY * 2:
                self.enable_menu_changed.emit(True)
                self.reverse_timer = ENABLE_MENU_DELAY * 2
                self._sys_sec = 0
                self._is_recording_btn = False
                self.flag_recording = False
                self.flag_recording_on_enable_menu = True
                self.btnRecord.setEnabled(True)
                self.btnRecord.setText("Record stream (Close another windows or softwares before starting).")



                
    @pyqtSlot(list)
    def on_basic_info_once(self, data):
        codec = data[0]
        self._codec_str = chr(codec&0xff) + chr((codec>>8)&0xff) + chr((codec>>16)&0xff) + chr((codec>>24)&0xff)
        self._fps_once = data[1]
        self._res_w_once = data[2]
        self._res_h_once = data[3]
        self.btnRecord.setEnabled(True)
    def btn_start_stop_recording_clicked(self):
        self.flag_recording_on_enable_menu = False
        self._is_recording_btn = not self._is_recording_btn
        self.flag_recording = not self.flag_recording
        match self._codec_str:
            case "h264": 
                self.fourcc = cv2.VideoWriter_fourcc(*'XVID') 
                date = datetime.today().strftime('%Y-%m-%d')
                hour = datetime.today().strftime('%H-%M-%S')
                self._dir = WORK_SPACE_DIR + str(date) + "/"
                self._file_name = str(hour) + "-from-" + str(self._start_recording_from_sec) + "-to-" + str(self._start_recording_from_sec+self._recording_time) + ".avi"
                if not os.path.exists(self._dir):
                    os.makedirs(self._dir)
                self.out = cv2.VideoWriter(self._dir + self._file_name, self.fourcc, float(self._fps_once), (int(self._res_w_once), int(self._res_h_once)))
            case "hevc":
                self.fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                date = datetime.today().strftime('%Y-%m-%d')
                hour = datetime.today().strftime('%H-%M-%S')
                self._dir = WORK_SPACE_DIR + str(date) + "/"
                self._file_name = str(hour) + "-from-" + str(self._start_recording_from_sec) + "-to-" + str(self._start_recording_from_sec+self._recording_time) + ".mp4"
                if not os.path.exists(self._dir):
                    os.makedirs(self._dir)
                self.out = cv2.VideoWriter(self._dir + self._file_name, self.fourcc, self._fps_once, (int(self._res_w_once), int(self._res_h_once)))
            case _:
                self.fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                date = datetime.today().strftime('%Y-%m-%d')
                hour = datetime.today().strftime('%H-%M-%S')
                self._dir = WORK_SPACE_DIR + str(date) + "/" + str(int(self._fps_once)) + "fps-" + str(int(self._res_w_once)) + "x" + str(int(self._res_h_once)) + "res-h265/"
                self._file_name = str(hour) + "-from-" + str(self._start_recording_from_sec) + "-to-" + str(self._start_recording_from_sec+self._recording_time) + ".mp4"
                if not os.path.exists(self._dir):
                    os.makedirs(self._dir)
                self.out = cv2.VideoWriter(self._dir + self._file_name, self.fourcc, self._fps_once, (int(self._res_w_once), int(self._res_h_once)))
    def recording(self, cv_img):
        if self.flag_recording:
            rgb_image = cv2.cvtColor(cv_img, 1)
            self.out.write(rgb_image)

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)