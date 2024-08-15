from app import *
class LoginController(QObject):
    def __init__(self, login_model):
        super().__init__()
        self._login_model = login_model
    @pyqtSlot(str)
    def change_call_camera_ip(self, value):
        self._login_model.ip = value
        self._login_model.is_ip = True if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",value) else False
        self.check_final_validation()
    @pyqtSlot(str)
    def change_call_camera_user(self, value):
        self._login_model.user = value
        self._login_model.is_user = True if len(value) > 1 else False
        self.check_final_validation()
    @pyqtSlot(str)
    def change_call_camera_password(self, value):
        self._login_model.password = value
        self._login_model.is_password = True if len(value) > 1 else False
        self.check_final_validation()
    def check_final_validation(self):
        self._login_model.enable_button = True if self._login_model.user and self._login_model.is_ip and self._login_model.is_password else False