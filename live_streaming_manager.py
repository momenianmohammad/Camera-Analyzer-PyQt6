from app import *
class LiveStreamingManager(QThread):
    streaming_changed = pyqtSignal(np.ndarray)
    basic_info_changed = pyqtSignal(int, list, list, list)
    basic_info_once_changed = pyqtSignal(list)
    basic_info_just_sys_second_changed = pyqtSignal(int)
    is_connected_changed = pyqtSignal(list)
    def __init__(self, data= {}, parent=None):
        super(LiveStreamingManager, self).__init__(parent=parent)
        self.initializeValues()
        self.assistant(data)
        self._data = data
    def run(self):
        if self._data is None:
            self.stop()
        else:
            self.check_ip_camera_connectivity()
            self.prepare_video()
    def initializeValues(self):
        self.cap = cv2.VideoCapture()
        self._isRunning = True
        self._send_once = False
        self._sys_second = 0
        self._prev_frame_time = 0
        self._new_frame_time = 0
        self._fps = 0
        self._fps_list = []
        self._frame_w_list = []
        self._frame_h_list = []
        self._interval = 0
        self._connection_test = False
        self._fps_cv = 0
    def assistant(self, data):
        if data is None:
            self.stop() 
        else:
            if len(data) > 0:
                if 'path_offline' in data:
                    path = data['path_offline']
                    if path != '':
                        self._golden_link = path
                else:
                    if 'connection_test' in data:
                        self._connection_test = data['connection_test']
                        if 'user_info' in data:
                            ip = data['user_info'][0]
                            user = data['user_info'][1]
                            password = data['user_info'][2]
                        if 'type_brand_streams' in data:
                            usb_or_ip = data['type_brand_streams'][0]
                            brand = data['type_brand_streams'][1]
                        if 'profile' in data:
                            fps = data['profile'][0]
                            self._fps_cv = fps
                            res_w = data['profile'][1]
                            res_h = data['profile'][2]
                            res = str(res_w) + "x" + str(res_h)
                            codec = data['profile'][3]
                            compression = data['profile'][4]
                        match self._connection_test:
                            case True: 
                                match  usb_or_ip, brand:
                                    case 'ip', 'axis': 
                                        self._golden_link = "rtsp://" + user + ":" + password + "@" + ip + ":554/axis-media/media.amp"
                            case False:
                                match  usb_or_ip, brand:
                                    case 'ip', 'axis':
                                        self._golden_link = "rtsp://" + user + ":" + password + "@" + ip + ":554/axis-media/media.amp?fps=" + str(fps) + "&resolution=" + res + "&compression=" + str(compression) + "&videocodec=" + str(codec)
    def check_ip_camera_connectivity(self):
        while self._isRunning and self._connection_test:
            try:
                self.cap.setExceptionMode(True)
                self.cap.open(self._golden_link,apiPreference=cv2.CAP_FFMPEG,params=[cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 5000],)
                if self.cap.isOpened():
                    self.is_connected_changed.emit([True, 0,"Ok"])
                    self._isRunning = False
                    self.stop()
                    break
            except cv2.error as e:
                for k in dir(e):
                    if k[0:2] != "__":
                        self.is_connected_changed.emit([False, int(e.code),str(e.err)])
                        self._isRunning = False
                        self.stop()
                        break
                if e.err == "!_src.empty()":
                    self.is_connected_changed.emit([False, int(e.code),str(e.err)])
                    self._isRunning = False
                    self.stop()
                    break
                self._isRunning = False
                self.stop()
                break
        else:
            self.is_connected_changed.emit([False, -10 ,"No need to check connection"])  
    def prepare_video(self):
        try:
            self.cap.open(self._golden_link,apiPreference=cv2.CAP_FFMPEG)
            while self.cap.isOpened() and self.isRunning:  
                ret, cv_img = self.cap.read()
                if not ret:
                    self.stop()
                    break
                if ret and cv_img is not None:
                    self.streaming_changed.emit(cv_img)
                    try: 
                        codec = int(self.cap.get(cv2.CAP_PROP_FOURCC))
                        width  = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                        height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                        if self._send_once == False and int(width) > 0 and int(height) > 0:
                            if self._fps_cv > 0:
                                self._send_once = True
                                self.basic_info_once_changed.emit([codec, self._fps_cv, width , height])
                            else:
                                self._send_once = True
                                self._fps_cv = self.cap.get(cv2.CAP_PROP_FPS)
                                self.basic_info_once_changed.emit([codec, self._fps_cv, width , height])
                        self._new_frame_time = time.time()
                        self._fps = 1/(self._new_frame_time-self._prev_frame_time)
                        self._prev_frame_time = self._new_frame_time                        
                        self._interval = self._interval+1
                        self._fps_list.append(self._fps)
                        self._frame_w_list.append(width)
                        self._frame_h_list.append(height)
                        if self._interval == self._fps_cv:
                            self._sys_second  = self._sys_second + 1
                            self._interval = 0
                            self.basic_info_changed.emit(self._sys_second, self._fps_list, self._frame_w_list, self._frame_h_list)
                            self.basic_info_just_sys_second_changed.emit(self._sys_second)
                            self._fps_list.clear()
                            self._frame_w_list.clear()
                            self._frame_h_list.clear()
                            if self._sys_second > RUN_TIME_THREAD_LIMITATION:
                                self.stop()
                    except:
                        pass
            else:
                self.cap.release()
        except:
            pass

    def __del__(self):
        del self
    def stop(self):
        self._isRunning = False
        self.isFinished = True
        self.isRunning = False
        self.cap.release()
        self.exit()
        self.quit()
        del self




        