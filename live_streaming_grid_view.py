from app import *
class LiveStreamingGridView(QWidget):
    def __init__(self, data={}, parent = None):
        super(LiveStreamingGridView, self).__init__(parent)
        if data is None:
            self.deleteGridView()
        self.initializeValues(data=data)
    def initializeValues(self, data):
        self.layoutMap = {}
        self.buttonMap = {}
        self.is_clicked_on_item = False
        if 'type_brand_streams' in data and 'user_info' in data and 'profiles' in data and 'connection_test' in data:
            self.data = data
    def setupUi(self, MainWindow):
        MainWindow.resize(AVAILABLE_WIDTH, AVAILABLE_HEIGHT - AVAILABLE_HEIGHT // 10)
        self.centralwidget = QWidget(MainWindow) # Besiar mohem
        MainWindow.setCentralWidget(self.centralwidget) # Besiar mohem
        self.layout = QHBoxLayout(self.centralwidget) # Besiar mohem
        self.scrollArea = QScrollArea(self.centralwidget) # Besiar mohem
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.layout.addWidget(self.scrollArea)
        self.showMain(self.data)
    def deleteGridView(self):
        try:
            self._live_manager.stop()
            self.scrollArea.setParent(None)
            self.scrollAreaWidgetContents.setParent(None)
            self.gridLayout.setParent(None)
            self.scrollArea.deleteLater()
            self.scrollAreaWidgetContents.deleteLater()
            self.gridLayout.deleteLater()
            self._live_view.deleteStreamingView()
            del self
        except:
            pass
    def showMain(self, data = {}):
        col = len(data['profiles'])
        view_type = data['view_type']
        for i in range(0, col):
            match view_type:
                case 'stream':
                    lsv_data={
                    'type_brand_streams': data['type_brand_streams'], # ['usb', '',1]
                    'user_info': data['user_info'],
                    'profile': data['profiles'][i],
                    'connection_test': False,
                    'view_type': 'stream'
                    }
                case 'hist':
                    lsv_data={
                    'type_brand_streams': data['type_brand_streams'], # ['usb', '',1]
                    'user_info': data['user_info'],
                    'profile': data['profiles'][i],
                    'connection_test': False,
                    'view_type': 'hist'
                    }
                case 'dead':
                    lsv_data={
                    'type_brand_streams': data['type_brand_streams'], # ['usb', '',1]
                    'user_info': data['user_info'],
                    'profile': data['profiles'][i],
                    'connection_test': False,
                    'view_type': 'dead'
                    }
            from live_streaming_view import LiveStreamingView
            lsv = LiveStreamingView(data=lsv_data)
            self._live_manager = lsv._camera_manager
            self._live_view = lsv            
            if i > 0:
                lsv._ui_streaming.btnRecord.setHidden(True)
                lsv._ui_streaming.btnRecord.setVisible(False)
                lsv._ui_streaming.btnRecord.setEnabled(False)
            lsv.setMinimumSize(WIDTH_GRID_ITEM_VIEW_LIVE , HEIGHT_GRID_ITEM_VIEW_LIVE - (HEIGHT_GRID_ITEM_VIEW_LIVE // 4))
            self.gridLayout.addWidget(lsv, i, 0)
            match view_type:
                case 'stream':
                    self._goal_menu_activator = lsv._ui_streaming
                case 'hist':
                    self._goal_menu_activator = lsv._ui_gray_con
                case 'dead':
                    self._goal_menu_activator = lsv._ui_dead
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
                current_item.widget()._ui.verticalLayoutWidget.setGeometry(QRect(0, 0, AVAILABLE_WIDTH - 200, AVAILABLE_HEIGHT - 200))                
            for i in range(0, len(self.gridLayout)):
                item = self.gridLayout.itemAt(i)
                if isinstance(item.widget(), QWidget) and i !=current_item_index:
                    item.widget().hide()
        else:
            self.is_clicked_on_item = not self.is_clicked_on_item
            if isinstance(current_item.widget(), QWidget):
                current_item.widget()._ui.verticalLayoutWidget.setGeometry(QRect(0, 0, WIDTH_GRID_ITEM_VIEW, HEIGHT_GRID_ITEM_VIEW))
            for i in range(0, len(self.gridLayout)):
                item = self.gridLayout.itemAt(i)
                if isinstance(item.widget(), QWidget) and i !=current_item_index:
                    item.widget().show()