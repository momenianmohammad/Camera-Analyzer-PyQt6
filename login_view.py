from app import *
class LoginView(QWidget):
    is_just_offline_view_changed = pyqtSignal(bool)
    is_connected_changed = pyqtSignal(list)
    camera_essential_data_changed = pyqtSignal(dict)
    def __init__(self, login_model, login_controller):
        super(LoginView, self).__init__()
        self._fps_list = []
        self._login_model = login_model
        self._login_controller = login_controller
        self._camera_essential_data = {}
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(AVAILABLE_WIDTH , AVAILABLE_HEIGHT - AVAILABLE_HEIGHT // 10)
        self.widgetMain = QWidget(Form)
        self.widgetMain.setObjectName("widgetMain")
        Form.setCentralWidget(self.widgetMain)
        self.frame = QFrame(Form)
        self.frame.setGeometry(QRect(0, 0, AVAILABLE_WIDTH, AVAILABLE_HEIGHT - AVAILABLE_HEIGHT // 10))
        self.frame.setObjectName("frame")
        widgets_width_pos = (AVAILABLE_WIDTH // 2) - (AVAILABLE_WIDTH // 10)
        widgets_height_pos = (AVAILABLE_HEIGHT // 2) + (AVAILABLE_HEIGHT // 4)
        widgets_width = AVAILABLE_WIDTH // 5
        widgets_height = AVAILABLE_HEIGHT // 20
        self.pushButton_offline_mode = QPushButton(self.frame)
        self.pushButton_offline_mode.setGeometry(QRect(widgets_width_pos, widgets_height_pos - 24*(widgets_height - widgets_height//2), widgets_width, widgets_height))
        self.pushButton_offline_mode.setObjectName("pushButton_offline_mode")
        self.pushButton_offline_mode.clicked.connect(self.mainViewOfflineMode)
        self.labelMsg = QLabel(self.frame)
        self.labelMsg.setGeometry(QRect(widgets_width_pos, widgets_height_pos - 21*(widgets_height - widgets_height//2) , widgets_width, widgets_height))
        self.comboBox_type = QComboBox(self.frame)
        self.comboBox_type.setEnabled(False)
        self.comboBox_type.setGeometry(QRect(widgets_width_pos, widgets_height_pos - 18*(widgets_height - widgets_height//2), widgets_width, widgets_height))
        self.comboBox_type.setEditable(False)
        self.comboBox_type.setObjectName("comboBox_type")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.comboBox_brand = QComboBox(self.frame)
        self.comboBox_brand.setEnabled(False)
        self.comboBox_brand.setGeometry(QRect(widgets_width_pos, widgets_height_pos - 15*(widgets_height - widgets_height//2), widgets_width, widgets_height))
        self.comboBox_brand.setObjectName("comboBox_brand")
        self.comboBox_brand.addItem("")
        self.lineEdit_ip = QLineEdit(self.frame)
        self.lineEdit_ip.setGeometry(QRect(widgets_width_pos, widgets_height_pos - 12*(widgets_height - widgets_height//2), widgets_width , widgets_height))
        self.lineEdit_ip.setObjectName("textEdit_ip_address")
        self.lineEdit_user = QLineEdit(self.frame)
        self.lineEdit_user.setGeometry(QRect(widgets_width_pos, widgets_height_pos - 9*(widgets_height - widgets_height//2), widgets_width, widgets_height))
        self.lineEdit_user.setObjectName("textEdit_user")
        self.lineEdit_password = QLineEdit(self.frame)
        self.lineEdit_password.setGeometry(QRect(widgets_width_pos, widgets_height_pos - 6*(widgets_height - widgets_height//2), widgets_width, widgets_height))
        self.lineEdit_password.setObjectName("textEdit_password")
        self.pushButton_submit = QPushButton(self.frame)
        self.pushButton_submit.setGeometry(QRect(widgets_width_pos, widgets_height_pos - 3*(widgets_height - widgets_height//2), widgets_width, widgets_height))
        self.pushButton_submit.setEnabled(False)
        self.pushButton_submit.setObjectName("pushButton_submit")
        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)
        self.connectWidgets()
    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Login to Camera"))
        self.pushButton_offline_mode.setText(_translate("Form", "Offline Mode"))
        self.pushButton_submit.setText(_translate("Form", "SUBMIT"))
        self.lineEdit_ip.setPlaceholderText(_translate("Form", "IP Address: 192.168.x.x"))
        self.lineEdit_user.setPlaceholderText(_translate("Form", "Username: root"))
        self.lineEdit_password.setPlaceholderText(_translate("Form", "Password"))
        self.comboBox_type.setItemText(0, _translate("Form", "IP CAMERA"))
        self.comboBox_type.setItemText(1, _translate("Form", "PC CAMERA"))
        self.comboBox_brand.setItemText(0, _translate("Form", "AXIS"))
        self.labelMsg.setText(_translate("Form", "Login to camera"))
        self.labelMsg.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
    def connectWidgets(self):
        self.lineEdit_ip.textChanged.connect(self._login_controller.change_call_camera_ip)
        self.lineEdit_user.textChanged.connect(self._login_controller.change_call_camera_user)
        self.lineEdit_password.textChanged.connect(self._login_controller.change_call_camera_password)
        self.pushButton_submit.clicked.connect(lambda: self._login_controller.change_call_camera_ip)
        self.pushButton_submit.clicked.connect(lambda: self._login_controller.change_call_camera_user)
        self.pushButton_submit.clicked.connect(lambda: self._login_controller.change_call_camera_password)
        self.pushButton_submit.clicked.connect(self.call_camera)
        self._login_model.ip_changed.connect(self.on_call_camera_ip)
        self._login_model.user_changed.connect(self.on_call_camera_user)
        self._login_model.password_changed.connect(self.on_call_camera_password)
        self._login_model.enable_button_changed.connect(self.on_enable_button)
    def deleteLoginLayout(self):
        self.comboBox_type.setParent(None)
        self.comboBox_brand.setParent(None)
        self.pushButton_submit.setParent(None)
        self.pushButton_offline_mode.setParent(None)
        self.labelMsg.setParent(None)
        self.lineEdit_ip.setParent(None)
        self.lineEdit_user.setParent(None)
        self.lineEdit_password.setParent(None)
        self.comboBox_type.deleteLater()
        self.comboBox_brand.deleteLater()
        self.pushButton_submit.deleteLater()
        self.lineEdit_ip.deleteLater()
        self.lineEdit_user.deleteLater()
        self.lineEdit_password.deleteLater()
    @pyqtSlot(str)
    def on_call_camera_ip(self, value):
        self.lineEdit_ip.setText(value)

    @pyqtSlot(str)
    def on_call_camera_user(self, value):
        self.lineEdit_user.setText(value)
    @pyqtSlot(str)
    def on_call_camera_password(self, value):
        self.lineEdit_password.setText(value)
    @pyqtSlot(bool)
    def on_enable_button(self, value):
        self.pushButton_submit.setEnabled(value)
    def call_camera(self):
        from live_streaming_manager import LiveStreamingManager
        self.waiting_in_login()
        self._ip = str(self.lineEdit_ip.text())
        self._user = str(self.lineEdit_user.text())
        self._password = str(self.lineEdit_password.text()) 
        self._camera_essential_data = {
                'connection_test': True,
                'user_info':[self._ip, self._user, self._password],
                'type_brand_streams': ['ip', 'axis', 4],
                'profile': [25, 160, 120,'h265', 100], # akhari compression, mitooni baghie ro ham bezani beshe additional
        }
        self._camera_manager = LiveStreamingManager(data=self._camera_essential_data)
        self._camera_manager.is_connected_changed.connect(self.on_is_connected)
        self.camera_essential_data_changed.emit(self._camera_essential_data)
        self._camera_manager.start()
    @pyqtSlot(list)
    def on_is_connected(self, data):
        if len(data) > 0:
            self.is_connected_changed.emit(data)
    def waiting_in_login(self):
        self.lineEdit_user.setEnabled(False)
        self.pushButton_offline_mode.setEnabled(False)
        self.lineEdit_password.setEnabled(False)
        self.lineEdit_ip.setEnabled(False)
        self.pushButton_submit.setEnabled(False)
        self.labelMsg.setText("Waiting...")
    def return_to_login(self):
        self._camera_manager.stop()
        del self._camera_manager
        self.lineEdit_user.setEnabled(True)
        self.lineEdit_password.setEnabled(True)
        self.lineEdit_ip.setEnabled(True)
        self.lineEdit_user.setText("")
        self.lineEdit_password.setText("")
        self.lineEdit_ip.setText("")
        self.pushButton_submit.setEnabled(True)
        self.pushButton_offline_mode.setEnabled(True)
        self.labelMsg.setText("Something went wrong, try again")
    def mainViewOfflineMode(self):
        self.pushButton_offline_mode.setEnabled(False)
        self.is_just_offline_view_changed.emit(True)



