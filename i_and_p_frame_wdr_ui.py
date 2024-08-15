from app import *
class IAndPFrameWDRUI(QWidget):
    def __init__(self, data={}):
        super().__init__()
        self.setupUi(self)
        self._data = data
    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.verticalLayoutWidget = QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, AVAILABLE_WIDTH // 4,AVAILABLE_HEIGHT // 4))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblCamera = QLabel(self.verticalLayoutWidget)
        self.lblCamera.setText("")
        self.lblCamera.setPixmap(QPixmap(".\\waiting.png"))
        self.lblCamera.setScaledContents(True)
        self.lblCamera.setObjectName("lblCamera")
        self.verticalLayoutWidget.setMinimumSize(WIDTH_GRID_ITEM_VIEW // 4,(HEIGHT_GRID_ITEM_VIEW + (HEIGHT_GRID_ITEM_VIEW // 8)) // 5)
        self.verticalLayout.addWidget(self.lblCamera)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnFullsc = QPushButton(self.verticalLayoutWidget)
        self.btnFullsc.setObjectName("btnFullsc")
        self.lblContrast = QLabel(self.verticalLayoutWidget)
        self.lblContrast.setObjectName("lblContrast")
        self.lblContrast.setVisible(False)
        self.btnHist = QPushButton(self.verticalLayoutWidget)
        self.btnHist.setObjectName("btnHist")
        self.btnHist.setVisible(False)
        self.lblWdr = QLabel(self.verticalLayoutWidget)
        self.lblWdr.setObjectName("lblWdr")
        self.lblWdr.setVisible(False)
        self.horizontalLayout.addWidget(self.btnHist)
        self.horizontalLayout.addWidget(self.lblContrast)
        self.horizontalLayout.addWidget(self.lblWdr)
        self.horizontalLayout.addWidget(self.btnFullsc)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)
    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", APP_NAME))
        self.btnHist.setText(_translate("Form", "Histogram + WDR + Contrast"))
        self.lblContrast.setText(_translate("Form", ""))
        self.lblWdr.setText(_translate("Form", ""))
        self.lblContrast.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.lblWdr.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
    def histoViewer(self):
        self.btnHist.setEnabled(False)
        self.btnHist.setVisible(False)
        self.btnHist.setHidden(True)
        if 'frame' in self._data:
            self.fig, self.ax = plt.subplots()
            self.canvas = FigureCanvas(self.fig)
            self.verticalLayout.replaceWidget(self.lblCamera, self.canvas)
            QPixmapCache.clear()
            frame = self._data['frame']
            color = ('b', 'g', 'r')
            for i,col in enumerate(color):
                histr = cv2.calcHist([frame],[i],None,[256],[0,256])
                plt.plot(histr,color = col)
                plt.xlim([0,256])
            self.canvas.draw()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            contrast = gray.std()
            self.lblContrast.setText("Contrast: " + str(round(contrast,2)) + " %")
            pixel_brightness = []
            height = frame.shape[0]
            width = frame.shape[1]
            for x in range (1, height):
                for y in range (1, width):
                    try:
                        pixel = frame[x,y]
                        R, G, B = pixel
                        R = np.array(R, dtype=np.float64)
                        G = np.array(G, dtype=np.float64)
                        B = np.array(B, dtype=np.float64)
                        brightness = sum([R,G,B])/3
                        brightness = np.array(brightness, dtype=np.float64)
                        if brightness > 0:
                            pixel_brightness.append(brightness)
                    except IndexError:
                        pass
            try:
                np.seterr(divide = 'ignore')
                np.seterr(divide = 'warn') 
                dyn_range = round(np.log2(max(pixel_brightness))-np.log2(min((pixel_brightness))), 2)
                self.lblWdr.setText("Wide Dynamic Range: " + str(dyn_range))
            except IndexError:
                self.lblWdr.setText("Something went wrong")
                pass