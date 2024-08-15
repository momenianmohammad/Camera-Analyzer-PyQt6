from app import *
class MainView(QMainWindow):
    def __init__(self, login_view = True, parent=None):
        super(MainView, self).__init__(parent)
        self.initializeVaribles()
        if login_view:
            self.startLoginWindow()
            self.runShowAlertThreadingStop()
    def initializeVaribles(self):
        self._camera_essential_data = {}
        from main_ui import MainUI
        from login_view import LoginView
        from login_model import LoginModel
        from login_controller import LoginController
        self._ui = MainUI()
        login_model = LoginModel()
        login_controller = LoginController(login_model)
        self._ui_login = LoginView(login_model, login_controller)
        self.flag_clicked_on_ui_i_and_p_frames_wdr_grid = False
    def startMainWindow(self):
        self._ui.setupUi(self)
        self.disableMenu(disable=False)
        self._ui.action_1_Stream.triggered.connect(self.action_1_Stream_Click)
        self._ui.action_2_Streams.triggered.connect(self.action_2_Streams_Click)
        self._ui.action_3_Streams.triggered.connect(self.action_3_Streams_Click)
        self._ui.action_Histogram_Contrast.triggered.connect(self.action_Histogram_Contrast_Click)
        self._ui.actionDead_Pixels_Detector.triggered.connect(self.action_Dead_Pixels_Detector_Click)
        self._ui.actionAttach_a_Video.triggered.connect(self.action_Attach_a_Video_Click)
    def startLoginWindow(self):
        self._ui_login.setupUi(self)
        self.threadingLogin()
    def startLiveStreamingGridWindow(self, data = {}):
        from live_streaming_grid_view import LiveStreamingGridView # bayad ui va view joda shan
        self._ui_live_streaming_grid = LiveStreamingGridView(data)
        self._ui_live_streaming_grid.setupUi(self)
        self._ui_live_streaming_grid._goal_menu_activator.enable_menu_changed.connect(self.on_enable_menu)
    def startIAndPFramesWDRGridWindow(self, data={}):
        from i_and_p_frame_wdr_grid_view import IAndPFrameWDRGridView
        self._ui_i_and_p_frames_wdr_grid = IAndPFrameWDRGridView(data=data)
        self._ui_i_and_p_frames_wdr_grid.setupUi(self)
        self._ui_i_and_p_frames_wdr_grid.enable_menu_changed.connect(self.on_enable_menu)        
    def threadingLogin(self):
        self._ui_login.is_connected.connect(self.on_is_connected)
        self._ui_login.camera_essential_data.connect(self.on_camera_essential_data)
    def disableMenu(self, disable = True):
        if disable:
            self._ui.menubar.setVisible(False)
            self._ui.menubar.setHidden(True)
            self._ui.menubar.setEnabled(False)
        else:
            self._ui.menubar.setVisible(True)
            self._ui.menubar.setHidden(False)
            self._ui.menubar.setEnabled(True)
    @pyqtSlot(bool)
    def on_enable_menu(self, value):
        if value == True:
            self.disableMenu(False)
        else:
            self.disableMenu(True)
    def stopThreadingOnWindowChanged(self, delete_offline_view = True):
        self.disableMenu(True)
        if delete_offline_view == True:
            if self.flag_clicked_on_ui_i_and_p_frames_wdr_grid == True:
                self._ui_live_streaming_grid.deleteGridView()
                self._ui_i_and_p_frames_wdr_grid.deleteIAndPAndWdrView()
        else: 
            self._ui_live_streaming_grid.deleteGridView()
    def openIAndPFramesWDRGridWindow(self):
        files_limit = 'Videos (*.avi *.mp4)'
        fileName = QFileDialog.getOpenFileName(self, 'OpenFile', WORK_SPACE_DIR, files_limit)
        if fileName[0] != "":
            data = {
                "path" : fileName[0]
            }
            self.startIAndPFramesWDRGridWindow(data=data)
            self.stopThreadingOnWindowChanged(delete_offline_view=False)
            self.flag_clicked_on_ui_i_and_p_frames_wdr_grid = True
    def action_1_Stream_Click(self, s):
        self.stopThreadingOnWindowChanged()
        ls_data={
            'type_brand_streams': self._camera_essential_data['type_brand_streams'], # ['usb', '',1]
            'user_info': self._camera_essential_data['user_info'],
            'profiles': [[25, 1920, 1080,'h264', 0]], # akhari compression, mitooni baghie ro ham bezani beshe additional
            'connection_test': False,
            'view_type': 'stream'
            }
        self.startLiveStreamingGridWindow(data=ls_data)
    def action_2_Streams_Click(self, s):
        self.stopThreadingOnWindowChanged()
        ls_data={
            'type_brand_streams': self._camera_essential_data['type_brand_streams'], # ['usb', '',1]
            'user_info': self._camera_essential_data['user_info'],
            'profiles': [[12, 1280, 720,'h265', 50], [12, 1280, 720,'h265', 50]], # akhari compression, mitooni baghie ro ham bezani beshe additional
            'connection_test': False,
            'view_type': 'stream'
            }
        self.startLiveStreamingGridWindow(data=ls_data)
    def action_3_Streams_Click(self, s):
        self.stopThreadingOnWindowChanged()
        ls_data={
            'type_brand_streams': self._camera_essential_data['type_brand_streams'], # ['usb', '',1]
            'user_info': self._camera_essential_data['user_info'],
            'profiles': [[8, 640, 480,'h265', 75], [8, 640, 480,'h265', 75] ,[8, 640, 480,'h265', 75]], # akhari compression, mitooni baghie ro ham bezani beshe additional
            'connection_test': False,
            'view_type': 'stream'
            }
        self.startLiveStreamingGridWindow(data=ls_data)    
    def action_Histogram_Contrast_Click(self, s):
        self.stopThreadingOnWindowChanged()
        hc_data={
            'type_brand_streams': self._camera_essential_data['type_brand_streams'], # ['usb', '',1]
            'user_info': self._camera_essential_data['user_info'],
            'profiles': [[2, 160, 120,'h265', 100]], # akhari compression, mitooni baghie ro ham bezani beshe additional
            'connection_test': False,
            'view_type': 'hist'
            }
        self.startLiveStreamingGridWindow(data=hc_data)
    def action_Dead_Pixels_Detector_Click(self, s):
        self.stopThreadingOnWindowChanged()
        ls_data={
            'type_brand_streams': self._camera_essential_data['type_brand_streams'], # ['usb', '',1]
            'user_info': self._camera_essential_data['user_info'],
            'profiles': [[12, 640, 480,'h265', 50]], # akhari compression, mitooni baghie ro ham bezani beshe additional
            'connection_test': False,
            'view_type': 'dead'
            }
        self.startLiveStreamingGridWindow(data=ls_data)
    def action_Attach_a_Video_Click(self, s):
        self.openIAndPFramesWDRGridWindow()
    @pyqtSlot(dict)
    def on_camera_essential_data(self, data):
        if len(data) > 0:
            self._camera_essential_data = data
            ls_data={
                'type_brand_streams': self._camera_essential_data['type_brand_streams'], # ['usb', '',1]
                'user_info': self._camera_essential_data['user_info'],
                'profiles': [[25, 1920, 1080,'h264', 0]], # akhari compression, mitooni baghie ro ham bezani beshe additional
                'connection_test': False,
                'view_type': 'stream'
                }
            self.startMainWindow()
            self.startLiveStreamingGridWindow(data=ls_data)
    @pyqtSlot(list)
    def on_is_connected(self, data):
        if len(data) > 0:
            match data[0]:
                case True:  
                    pass
                case False:
                    self._ui_login.return_to_login()
            self._ui_login.deleteLoginLayout()
    def runShowAlertThreadingStop(self):
        QTimer.singleShot(RUN_TIME_DIALOGUE_STOP_THREAD, self.showAlertThreadingStop)
    def showAlertThreadingStop(self):     
        button = QMessageBox.question(self, "Memory is over", "Click YES to use stored data or NO to exit. You can RE-OPEN the software to new analyse.")
        if button == QMessageBox.Yes:
            pass
        else:
            app = QApplication(sys.argv)
            sys.exit(app.exec())