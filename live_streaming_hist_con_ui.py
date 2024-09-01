from app import *
class LiveStreamingHistConUi(QMainWindow):
    enable_menu_changed = pyqtSignal(bool)
    def __init__(self, hist_type = 'g'):
        super(LiveStreamingHistConUi, self).__init__()
        plt.close()
        self._hist_type = hist_type
        self.initPlot(hist_type=hist_type)
    def initPlot(self, hist_type = 'g'):
        self.fig, self.ax = plt.subplots()
        self.fig.suptitle('Waiting to get results....', fontweight ="bold")
        self.canvas = FigureCanvas(self.fig)
        self.setupUi(self)
        self.lw = 4
        self.alpha = 0.5
        self.bins = 16
        self.resizeWidth = 0
        self.contrast = 0.0
        match hist_type:
            case 'r':
                self._hist_type = 'r'
                self.lineR, = self.ax.plot(np.arange(self.bins), np.zeros((self.bins,)), c='r', lw=self.lw, alpha=self.alpha , label='Red')
                self.lineG, = self.ax.plot(np.arange(self.bins), np.zeros((self.bins,)), c='g', lw=self.lw, alpha=self.alpha , label='Green')
                self.lineB, = self.ax.plot(np.arange(self.bins), np.zeros((self.bins,)), c='b', lw=self.lw, alpha=self.alpha , label='Blue')
            case 'g':
                self._hist_type = 'g'
                self.lineGray, = self.ax.plot(np.arange(self.bins), np.zeros((self.bins,1)), c='k', lw=self.lw, label='intensity')
            case _:
                self._hist_type = 'g'
                self.lineGray, = self.ax.plot(np.arange(self.bins), np.zeros((self.bins,1)), c='k', lw=self.lw, label='intensity')
        self.ax.set_xlim(0, self.bins-1)
        self.ax.set_ylim(0, 1)
        self.ax.legend()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.verticalLayoutWidget = QWidget(Form) # Besiar mohem
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, WIDTH_GRID_ITEM_VIEW_LIVE , HEIGHT_GRID_ITEM_VIEW_LIVE - (HEIGHT_GRID_ITEM_VIEW_LIVE // 8)))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.canvas.setMinimumSize(WIDTH_GRID_ITEM_VIEW_LIVE , HEIGHT_GRID_ITEM_VIEW_LIVE - (HEIGHT_GRID_ITEM_VIEW_LIVE // 4))
        self.verticalLayout.addWidget(self.canvas)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)
    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", APP_NAME))
    @pyqtSlot(int)
    def on_basic_info_just_sys_second(self, sys_second):
        if self.contrast > 0:
            if sys_second == ENABLE_MENU_DELAY // 3:
                self.enable_menu_changed.emit(True) 
    @pyqtSlot(np.ndarray)
    def on_streaming(self, cv_img):
        if self.resizeWidth > 0:
            (height, width) = cv_img.shape[:2]
            resizeHeight = int(float(self.resizeWidth / width) * height)
            cv_img = cv2.resize(cv_img, (self.resizeWidth, resizeHeight),
                interpolation=cv2.INTER_AREA)
        numPixels = np.prod(cv_img.shape[:2])
        match self._hist_type:
            case 'r':
                self.fig.suptitle('Real Time RGB Histogram', fontweight ="bold")
                (b, g, r) = cv2.split(cv_img)
                histogramR = cv2.calcHist([r], [0], None, [self.bins], [0, 255]) / numPixels
                histogramG = cv2.calcHist([g], [0], None, [self.bins], [0, 255]) / numPixels
                histogramB = cv2.calcHist([b], [0], None, [self.bins], [0, 255]) / numPixels
                self.lineR.set_ydata(histogramR)
                self.lineG.set_ydata(histogramG)
                self.lineB.set_ydata(histogramB)
                self.canvas.draw()
            case 'g':
                gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
                histogram = cv2.calcHist([gray], [0], None, [self.bins], [0, 255]) / numPixels
                self.lineGray.set_ydata(histogram)
                self.contrast = gray.std()
                self.fig.suptitle('Real Time Gray Scale Histogram. ' + "Contrast: " + str(round(self.contrast,2)) + " %", fontweight ="bold")
                self.canvas.draw()
            case _:
                gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
                histogram = cv2.calcHist([gray], [0], None, [self.bins], [0, 255]) / numPixels
                self.lineGray.set_ydata(histogram)
                self.contrast = gray.std()
                self.fig.suptitle('Real Time Gray Scale Histogram. ' + "Contrast: " + str(round(self.contrast,2)) + " %", fontweight ="bold")
                self.canvas.draw()