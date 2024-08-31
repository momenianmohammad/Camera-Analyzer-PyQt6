from app import *
class LiveStreamingFpsBwUI(QWidget):
    def __init__(self, graph_type='fps'):
        super().__init__()
        self._graph_type = graph_type
        self._sys_second_list = []
        self._fps_list = []
        self._bw_list = []
        self._avg_fps = []
        self.default_styles = {"color": "#e7e7e7", "font-size": "18px"}
        self.setupUi(self)
    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.verticalLayoutWidget = QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, WIDTH_GRID_ITEM_VIEW_LIVE , HEIGHT_GRID_ITEM_VIEW_LIVE - (HEIGHT_GRID_ITEM_VIEW_LIVE // 4)))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plot = pg.PlotWidget()
        self.verticalLayout.addWidget(self.plot)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)
    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", APP_NAME))
        match self._graph_type:
            case 'fps':
                self.plot.setBackground('#222222')
                styles = {"color": "#e7e7e7", "font-size": "18px"}
                self.plot.setLabel("left", "Frame rate", **styles)
                pen = pg.mkPen(color=(255, 255, 255), width=5)
                self._data_line =  self.plot.plot(self._sys_second_list, self._fps_list, pen=pen, symbol="o", symbolSize=10, symbolBrush="w")
            case 'bw':
                self.plot.setBackground('#e7e7e7')
                styles = {"color": "#222222", "font-size": "18px"}
                self.plot.setLabel("left", "Bandwidth rate", **styles)
                pen = pg.mkPen(color=(48, 48, 48), width=5)
                self._data_line =  self.plot.plot(self._sys_second_list, self._bw_list, pen=pen, symbol="o", symbolSize=10, symbolBrush="#222222")
            case 'hist':
                self.plot.setBackground('#222222')
                styles = {"color": "#e7e7e7", "font-size": "18px"}
                self.plot.setLabel("left", "Frame rate", **styles)
                pen = pg.mkPen(color=(255, 255, 255), width=5)
                self._data_line =  self.plot.plot(self._sys_second_list, self._fps_list, pen=pen, symbol="o", symbolSize=10, symbolBrush="w")
            case _:
                self.plot.setBackground('#222222')
                styles = {"color": "#e7e7e7", "font-size": "18px"}
                self.plot.setLabel("left", "Frame rate", **styles)
                pen = pg.mkPen(color=(255, 255, 255), width=5)
                self._data_line =  self.plot.plot(self._sys_second_list, self._fps_list, pen=pen, symbol="o", symbolSize=10, symbolBrush="w")
    @pyqtSlot(int, list, list, list)
    def on_basic_info(self, sys_second, fps, res_w, res_h):
        if fps > MAX_FPS_RATE:
            random_fps = random.uniform(MAX_FPS_RATE - 3, MAX_FPS_RATE)
            fps = round(random_fps,2)
        fps_calc = sum(fps)/len(fps)
        res_w_calc = sum(res_w)/len(res_w)
        res_h_calc = sum(res_h)/len(res_h)
        b_w_calc =  fps_calc * res_w_calc * res_h_calc
        self._sys_second_list.append(sys_second)
        fps_final_calc = round(fps_calc, 2)
        bw_final_calc = round(b_w_calc / 100000, 2)
        self._fps_list.append(fps_final_calc)
        self._bw_list.append(bw_final_calc)
        fps_final_average = round(sum(self._fps_list) / len(self._fps_list), 2)
        fps_final_calc_show = str(fps_final_calc)
        fps_final_average_show = str(fps_final_average)
        bw_final_average = round(sum(self._bw_list) / len(self._bw_list), 2)
        bw_final_calc_show = str(bw_final_calc)
        bw_final_average_show = str(bw_final_average)
        if len(self._fps_list) > 0 and len (self._sys_second_list) > 0:
            match self._graph_type:
                case 'fps':
                    self._data_line.setData(self._sys_second_list, self._fps_list)  # Update the data.
                    self.plot.setTitle("FPS: " + fps_final_calc_show + ", AVG-FPS: " + fps_final_average_show)
                    self.plot.setLabel("bottom", "Run time (sec): " + str(sys_second), **self.default_styles)
                case 'bw':
                    self._data_line.setData(self._sys_second_list, self._bw_list)    
                    self.plot.setTitle("Band-Width: " + bw_final_calc_show + " Kbps " ", AVG-Band-Width: " + bw_final_average_show + " Kbps")