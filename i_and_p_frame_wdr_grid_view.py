from app import *
class IAndPFrameWDRGridView(QWidget):
    enable_menu_changed = pyqtSignal(bool)
    layoutMap = {}
    buttonMap = {}
    is_clicked_on_item = False
    def __init__(self, data={}, parent = None):
        super(IAndPFrameWDRGridView, self).__init__(parent)
        self.initializeValues(data=data)
        self.threading()
    def initializeValues(self, data):
        self.i_qt_img_list = []
        self.i_frame_list = []
        self.index_i_frame = 0
        self.data = data
        self.previous_basic_info_video = ''
        self._is_right_video = False
        self._clicked_frame_controller_status = 1
    def threading(self):
        if self.data is not None:
            from i_and_p_frame_wdr_manager import IAndPFrameWDRManager
            self._offline_manager = IAndPFrameWDRManager(data=self.data)
            self._offline_manager.basic_info_video_changed.connect(self.on_basic_info_video)
            self._offline_manager.count_of_frames_changed.connect(self.on_count_of_frames)  
            self._offline_manager.frame_recieved_changed.connect(self.on_frame_recieved)        
            self._offline_manager.is_save_i_frames_changed.connect(self.on_is_save_i_frames)
            self._offline_manager.is_save_p_frames_changed.connect(self.on_is_save_p_frames)
            self._offline_manager.status_save_i_frames_changed.connect(self.on_status_save_i_frames)
            self._offline_manager.status_save_p_frames_changed.connect(self.on_status_save_p_frames)
            self._offline_manager.start()
    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(160, 120, Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(p)
    @pyqtSlot(dict)
    def on_basic_info_video(self, data):
        if 'stop' in data:
            self.enable_menu_changed.emit(True)
        if 'count_of_frames' in data and 'basic_info' in data:
            self.btnVideoInformation.setText("Waiting to get basic information")
            basic_info = data['basic_info']
            count_of_frames = data['count_of_frames']
            self.previous_basic_info_video = basic_info + "total-frames=" + str(count_of_frames)

    @pyqtSlot(int, int)
    def on_count_of_frames(self, count_of_i_frames, count_of_p_frames):
        if count_of_i_frames > 0 and count_of_p_frames > 0:
            self.count_of_i_frames_str = "i-frames=" + str(count_of_i_frames)
            self.count_of_p_frames_str = "p-frames=" + str(count_of_p_frames)
    @pyqtSlot(list)
    def on_frame_recieved(self, frames):
        for frame in frames:
                frame = cv2.resize(frame,(320, 240), cv2.INTER_CUBIC)
                self.i_frame_list.append(frame)
                qt_img = self.convert_cv_qt(frame)
                self.i_qt_img_list.append(qt_img)
        
        self.btnVideoInformation.setText("Click to Show Video Information")
        self.btnVideoInformation.setFlat(False)
        self.btnVideoInformation.setEnabled(True)
        self.lblSaveFrames.setText("Waiting to save I and P frames")
    @pyqtSlot(str)
    def on_status_save_i_frames(self, value):
        self.lblSaveFrames.setText("Do not close the App. I frames are saving right now: " + value)
    @pyqtSlot(str)
    def on_status_save_p_frames(self, value):
        self.lblSaveFrames.setText("Do not close the App. P frames are saving right now: " + value)
    @pyqtSlot(bool)
    def on_is_save_i_frames(self, value):
        if value:
            self.lblSaveFrames.setText("Do not close the App. All I frames are saved. waiting to save P frames.")
    @pyqtSlot(bool)
    def on_is_save_p_frames(self, value):
        if value:
            self.enable_menu_changed.emit(True)
            self.lblSaveFrames.setText("Finished. All P frames are saved too.")
            self.lblSaveFrames.setMinimumSize(AVAILABLE_WIDTH // 6, HEIGHT_GRID_ITEM_VIEW // 18)
            self.disableBtnShowIFrames(disable=False)
    def setupUi(self, MainWindow):
        MainWindow.resize(AVAILABLE_WIDTH, AVAILABLE_HEIGHT - AVAILABLE_HEIGHT // 10)
        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.layout = QVBoxLayout(self.centralwidget)
        self.hLayout = QHBoxLayout()
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.btnVideoInformation = QPushButton()
        self.btnVideoInformation.setMinimumSize(AVAILABLE_WIDTH // 6, HEIGHT_GRID_ITEM_VIEW // 18)    
        self.btnVideoInformation.setText("Error! Your file is invalid.")
        self.btnVideoInformation.setEnabled(False)
        self.btnVideoInformation.setFlat(True)
        self.btnVideoInformation.clicked.connect(self.showVideoInformation)
        self.lblSaveFrames = QLabel()
        self.lblSaveFrames.setMinimumSize(AVAILABLE_WIDTH, HEIGHT_GRID_ITEM_VIEW // 18)
        self.lblSaveFrames.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.btnShowIFrames = QPushButton("Click to show I Frames")
        self.btnShowIFrames.setMinimumSize(WIDTH_GRID_ITEM_VIEW // 6, HEIGHT_GRID_ITEM_VIEW // 18)
        self.btnShowIFrames.setFont(custom_font)
        self.btnShowIFrames.clicked.connect(self.showAndSaveFrames)
        self.disableBtnShowIFrames()
        self.hLayout.addWidget(self.btnVideoInformation,alignment=Qt.AlignmentFlag.AlignLeft)
        self.hLayout.addWidget(self.lblSaveFrames)
        self.hLayout.addWidget(self.btnShowIFrames,alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addLayout(self.hLayout)
        self.layout.addWidget(self.scrollArea)
    def showVideoInformation(self):
        print("click")
        dlg = QMessageBox(self)
        dlg.setMinimumSize(WIDTH_GRID_ITEM_VIEW, HEIGHT_GRID_ITEM_VIEW // 5)
        dlg.setWindowTitle("Video Information")
        dlg.setText(self.previous_basic_info_video + "\n" + "\n" + self.count_of_i_frames_str + "\n" + self.count_of_p_frames_str + "\n" + "\n" +  "video path:" + "\n" + self.data["path"] + "\n"  + "\n" + "save folder:" +"\n"+ I_AND_P_FRAMES_DIR)
        dlg.exec()
    def disableBtnShowIFrames(self, disable = True):
        self.btnShowIFrames.setEnabled(False)
        self.btnShowIFrames.setVisible(False)
        self.btnShowIFrames.setHidden(True)
        if disable == False:
            self.btnShowIFrames.setEnabled(True)
            self.btnShowIFrames.setVisible(True)
            self.btnShowIFrames.setHidden(False)
    def showAndSaveFrames(self):
        self.disableBtnShowIFrames()
        self.showIFrameList()    
    def showIFrameList(self, col = 60, row = 5):
        if (len(self.i_qt_img_list) > col * row):
            return
        else:
            for i in range(col):
                for j in range(row):
                    if self.index_i_frame < len(self.i_qt_img_list):
                        from i_and_p_frame_wdr_ui import IAndPFrameWDRUI
                        data = {
                            'frame': self.i_frame_list[self.index_i_frame]
                        }
                        self._offline_ui = IAndPFrameWDRUI(data=data)
                        self._offline_ui.lblCamera.setPixmap(self.i_qt_img_list[self.index_i_frame])
                        self._offline_ui.btnFullsc.setText(str(self.index_i_frame))
                        self.saveButton(self._offline_ui.btnFullsc)
                        self.saveLayout(self._offline_ui, "ou")
                        self._offline_ui.btnFullsc.clicked.connect(self.swichFullScreen)
                        self._offline_ui.btnHist.clicked.connect(self._offline_ui.histoViewer)
                        self._offline_ui.setMinimumSize(AVAILABLE_WIDTH // 4,AVAILABLE_HEIGHT // 4)
                        self.gridLayout.addWidget(self._offline_ui, i, j)
                        self.index_i_frame = self.index_i_frame + 1
                    else:
                        return 
    def saveButton(self,obj):
        self.buttonMap[obj.text()] = obj
    def saveLayout(self,obj, text):
         self.layoutMap[text] = obj       
    def swichFullScreen(self):  
        current_item_index = int(self.sender().text())
        current_item = self.gridLayout.itemAt(current_item_index)
        if not self.is_clicked_on_item:
            self.is_clicked_on_item = not self.is_clicked_on_item
            if isinstance(current_item.widget(), QWidget):
                current_item.widget().verticalLayoutWidget.setGeometry(QRect(0, 0, AVAILABLE_WIDTH, AVAILABLE_HEIGHT - AVAILABLE_HEIGHT // 3))
                current_item.widget().lblWdr.setVisible(True)
                current_item.widget().lblContrast.setVisible(True)
                current_item.widget().lblContrast.setVisible(True)
                current_item.widget().btnHist.setVisible(True)                
            for i in range(0, len(self.gridLayout)):
                item = self.gridLayout.itemAt(i)
                if isinstance(item.widget(), QWidget) and i !=current_item_index:
                    item.widget().hide()
        else:
            self.is_clicked_on_item = not self.is_clicked_on_item
            if isinstance(current_item.widget(), QWidget):
                current_item.widget().verticalLayoutWidget.setGeometry(QRect(0, 0,AVAILABLE_WIDTH // 4,AVAILABLE_HEIGHT // 4))
                current_item.widget().lblWdr.setVisible(False)
                current_item.widget().lblContrast.setVisible(False)
                current_item.widget().btnHist.setVisible(False)
            for i in range(0, len(self.gridLayout)):
                item = self.gridLayout.itemAt(i)
                if isinstance(item.widget(), QWidget) and i !=current_item_index:
                    item.widget().show()
    def deleteIAndPAndWdrView(self):
        try:
            self._offline_manager.stop()
            self.scrollArea.setParent(None)
            self.scrollAreaWidgetContents.setParent(None)
            self.gridLayout.setParent(None)
            self.scrollArea.deleteLater()
            self.scrollAreaWidgetContents.deleteLater()
            self.gridLayout.deleteLater()
            del self
        except:
            pass