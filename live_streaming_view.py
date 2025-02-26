from app import *
class LiveStreamingView(QMainWindow):
    def __init__(self, data={}):
        super(LiveStreamingView, self).__init__()
        self.data = data
        self.view_type = data['view_type']
        self.unlimited_recording = data['unlimited_recording']
        self.setupUi(self) 
    def setupUi(self, MainWindow):
        MainWindow.resize(AVAILABLE_WIDTH, (AVAILABLE_HEIGHT - AVAILABLE_HEIGHT // 10))
        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.layout = QHBoxLayout(self.centralwidget)
        self.scrollArea = QScrollArea(self.centralwidget) # Besiar mohem
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.layout.addWidget(self.scrollArea)
        from live_streaming_ui import LiveStreamingUI
        from live_streaming_fps_bw_ui import LiveStreamingFpsBwUI
        self._ui_streaming = LiveStreamingUI()
        self._ui_bw = LiveStreamingFpsBwUI(graph_type='bw')
        self._ui_fps = LiveStreamingFpsBwUI(graph_type='fps')
        # print(self.unlimited_recording)
        match self.view_type:
            case 'stream':
                # ziriha hame ba ham hast va badesh unlimited recording filteresh mikone
                # self._ui_streaming.setMinimumWidth(WIDTH_GRID_ITEM_VIEW_LIVE)
                # self._ui_streaming.setMinimumHeight(HEIGHT_GRID_ITEM_VIEW_LIVE - (HEIGHT_GRID_ITEM_VIEW_LIVE // 8))
                # self._ui_fps.setMinimumWidth(WIDTH_GRID_ITEM_VIEW_LIVE)
                # self._ui_fps.setMinimumHeight(HEIGHT_GRID_ITEM_VIEW_LIVE - (HEIGHT_GRID_ITEM_VIEW_LIVE // 8))
                # self._ui_bw.setMinimumWidth(WIDTH_GRID_ITEM_VIEW_LIVE)
                # self._ui_bw.setMinimumHeight(HEIGHT_GRID_ITEM_VIEW_LIVE - (HEIGHT_GRID_ITEM_VIEW_LIVE // 8))
                # self.gridLayout.addWidget(self._ui_streaming, 0, 0)
                # self.gridLayout.addWidget(self._ui_fps, 0, 1)
                # self.gridLayout.addWidget(self._ui_bw, 0, 2)
                if(self.unlimited_recording == False):
                    self._ui_fps.setMinimumWidth(WIDTH_GRID_ITEM_VIEW_LIVE)
                    self._ui_fps.setMinimumHeight(HEIGHT_GRID_ITEM_VIEW_LIVE - (HEIGHT_GRID_ITEM_VIEW_LIVE // 8))
                    self._ui_bw.setMinimumWidth(WIDTH_GRID_ITEM_VIEW_LIVE)
                    self._ui_bw.setMinimumHeight(HEIGHT_GRID_ITEM_VIEW_LIVE - (HEIGHT_GRID_ITEM_VIEW_LIVE // 8))
                    self.gridLayout.addWidget(self._ui_fps, 0, 0)
                    self.gridLayout.addWidget(self._ui_bw, 0, 1)
                elif (self.unlimited_recording == True):
                    self._ui_streaming.setMinimumWidth(WIDTH_GRID_ITEM_VIEW_LIVE)
                    self._ui_streaming.setMinimumHeight(HEIGHT_GRID_ITEM_VIEW_LIVE - (HEIGHT_GRID_ITEM_VIEW_LIVE // 8))
                    self.gridLayout.addWidget(self._ui_streaming, 0, 0)

            case 'hist':
                from live_streaming_hist_con_ui import LiveStreamingHistConUi
                self._ui_gray_con = LiveStreamingHistConUi(hist_type='g')
                self._ui_rgb = LiveStreamingHistConUi(hist_type='r')
                self._ui_gray_con.setMinimumWidth(WIDTH_GRID_ITEM_VIEW_LIVE)
                self._ui_gray_con.setMinimumHeight(HEIGHT_GRID_ITEM_VIEW_LIVE - (HEIGHT_GRID_ITEM_VIEW_LIVE // 8))
                self._ui_rgb.setMinimumWidth(WIDTH_GRID_ITEM_VIEW_LIVE)
                self._ui_rgb.setMinimumHeight(HEIGHT_GRID_ITEM_VIEW_LIVE - (HEIGHT_GRID_ITEM_VIEW_LIVE // 8))
                self.gridLayout.addWidget(self._ui_gray_con, 0, 0)
                self.gridLayout.addWidget(self._ui_rgb, 0, 1)
            case 'dead':
                from live_streaming_dead_pixels_ui import LiveStreamingDeadPixelsUI
                self._ui_dead = LiveStreamingDeadPixelsUI()
                self._ui_dead.setMinimumWidth(WIDTH_GRID_ITEM_VIEW_LIVE)
                self._ui_dead.setMinimumHeight(HEIGHT_GRID_ITEM_VIEW_LIVE - (HEIGHT_GRID_ITEM_VIEW_LIVE // 8))
                self.gridLayout.addWidget(self._ui_dead, 0, 0)
        self.threading()
    def threading(self):
        from live_streaming_manager import LiveStreamingManager
        self._camera_manager = LiveStreamingManager(data=self.data)
        match self.view_type:
            case 'stream':
                self._camera_manager.streaming_changed.connect(self._ui_streaming.on_streaming)
                self._camera_manager.basic_info_once_changed.connect(self._ui_streaming.on_basic_info_once)
                self._camera_manager.basic_info_just_sys_second_changed.connect(self._ui_streaming.on_basic_info_just_sys_second)
                self._camera_manager.basic_info_changed.connect(self._ui_fps.on_basic_info)
                self._camera_manager.basic_info_changed.connect(self._ui_bw.on_basic_info)
            case 'hist':
                self._camera_manager.streaming_changed.connect(self._ui_gray_con.on_streaming)
                self._camera_manager.basic_info_just_sys_second_changed.connect(self._ui_gray_con.on_basic_info_just_sys_second)
                self._camera_manager.streaming_changed.connect(self._ui_rgb.on_streaming)
            case 'dead':
                self._camera_manager.streaming_changed.connect(self._ui_dead.on_streaming)
                self._camera_manager.basic_info_once_changed.connect(self._ui_dead.on_basic_info_once)
                self._camera_manager.basic_info_just_sys_second_changed.connect(self._ui_dead.on_basic_info_just_sys_second)
        self._camera_manager.start()
    def deleteStreamingView(self):
        self.scrollArea.setParent(None)
        self.scrollAreaWidgetContents.setParent(None)
        self.gridLayout.setParent(None)
        self.scrollArea.deleteLater()
        self.scrollAreaWidgetContents.deleteLater()
        self.gridLayout.deleteLater()
        del self