from app import *
class LoginModel(QObject):
    ip_changed = pyqtSignal(str)
    user_changed = pyqtSignal(str)
    password_changed = pyqtSignal(str)
    enable_button_changed = pyqtSignal(bool)
    @property
    def ip(self):
        return self._ip
    @ip.setter
    def ip(self, value):
        self._ip = value
        self.ip_changed.emit(value)
    @property
    def user(self):
        return self._user
    @user.setter
    def user(self, value):
        self._user = value
        self.user_changed.emit(value)
    @property
    def password(self):
        return self._password
    @password.setter
    def password(self, value):
        self._password = value
        self.password_changed.emit(value)
    @property
    def enable_button(self):
        return self._enable_button
    @enable_button.setter
    def enable_button(self, value):
        self._enable_button = value
        self.enable_button_changed.emit(value) 
    @property
    def is_ip(self):
        return self._is_ip
    @is_ip.setter
    def is_ip(self, value):
        self._is_ip = value
    @property
    def is_user(self):
        return self._is_user
    @is_user.setter
    def is_user(self, value):
        self._is_user = value
    @property
    def is_password(self):
        return self._is_password
    @is_password.setter
    def is_password(self, value):
        self._is_password = value
    def __init__(self):
        super().__init__()
        self._ip = ""
        self._user = ""
        self._password = ""
        self._enable_button = False
        self._is_ip = False
        self._is_user = False
        self._is_password = False