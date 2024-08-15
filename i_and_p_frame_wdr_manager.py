from app import *
class IAndPFrameWDRManager(QThread):
    frame_recieved_changed = pyqtSignal(list)
    basic_info_video_changed = pyqtSignal(dict)
    count_of_frames_changed = pyqtSignal(int, int)
    is_save_i_frames_changed = pyqtSignal(bool)
    status_save_i_frames_changed = pyqtSignal(str)
    status_save_p_frames_changed = pyqtSignal(str)
    is_save_p_frames_changed = pyqtSignal(bool)     
    def __init__(self, data= {}, stop=False, parent = None):
        super(IAndPFrameWDRManager, self).__init__(parent=parent)
        if stop == True:
            self.stop()
        else:
            self.initializeValues()
            self.assistant(data)
    def initializeValues(self):
        self._isRunning = True
        self._path = ''
        self._count_of_i_frames = 0
        self._count_of_p_frames = 0
    def assistant(self, data):
        if data is None:
            self.stop() 
        else:      
            if len(data) > 0:
                if 'path' in data:
                    self._path = data['path']
    def run(self):
        self.get_basic_info(self._path)
        self.show_i_frames(self._path)
        self.save_i_frames(self._path)
        self.save_p_frames(self._path)
    def get_basic_info(self, path):
        command1 = 'ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of csv=p=0 '
        frames_count = subprocess.check_output(command1 + path).decode()
        command2 = 'ffprobe -v error -select_streams v:0 -show_entries stream=width,height,duration,bit_rate -of default=noprint_wrappers=1 '
        basic_info = subprocess.check_output(command2 + path).decode()
        if (int(frames_count) > MIN_SHOW_FRAME and int(frames_count) < MAX_SHOW_FRAME):
            basic_info  = basic_info.replace("\n", " , ")
            data = {
                "count_of_frames": int(frames_count),
                "basic_info": basic_info,
            }
            self.basic_info_video_changed.emit(data)
    def get_frame_types(self,path):
        command = 'ffprobe -v error -show_entries frame=pict_type -of default=noprint_wrappers=1 '.split()
        out = subprocess.check_output(command + [path]).decode()
        frame_types = out.replace('pict_type=','').split()
        return zip(range(len(frame_types)), frame_types)
    def show_i_frames(self,path):
        frame_types = self.get_frame_types(path)
        i_frames = [x[0] for x in frame_types if x[1]=='I']
        self._count_of_i_frames = len(i_frames)
        self.get_count_of_p_frames(path=path)
        cap = cv2.VideoCapture(path)
        frames_ = []
        if i_frames:
            for frame_no in i_frames:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
                frame = cap.read()[1]
                frames_.append(frame)         
        else:
            pass
        cap.release()
        self.frame_recieved_changed.emit(frames_)
    def get_count_of_p_frames(self,path):
        frame_types = self.get_frame_types(path)
        p_frames = [x[0] for x in frame_types if x[1]=='P']
        self.count_of_frames_changed.emit(self._count_of_i_frames, len(p_frames)) 
    def get_frame_types_for_save(self, path):
       command = 'ffprobe -v error -show_entries frame=pict_type -of default=noprint_wrappers=1 '.split()
       out = subprocess.check_output(command + [path]).decode()
       frame_types = out.replace('pict_type=','').split()
       return zip(range(len(frame_types)), frame_types)   
    def save_i_frames(self,path):
        frame_types = self.get_frame_types_for_save(path)
        i_frames = [x[0] for x in frame_types if x[1]=='I']
        if i_frames:
            basename = os.path.splitext(os.path.basename(path))[0]
            dir_local_i_frames = I_AND_P_FRAMES_DIR + basename + "/I-FRAMES/"
            if not os.path.exists(dir_local_i_frames):
                os.makedirs(dir_local_i_frames)
            cap = cv2.VideoCapture(path)
            index_show = 1
            for frame_no in i_frames:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
                frame = cap.read()[1]
                outname = 'i_'+str(frame_no)+'.jpg'               
                cv2.imwrite(dir_local_i_frames + outname, frame)
                self.status_save_i_frames_changed.emit(str(index_show) + " from " + str(len(i_frames)))
                index_show = index_show + 1

            cap.release()
            self.is_save_i_frames_changed.emit(True)
        else:
            pass
    def save_p_frames(self,path):
        frame_types = self.get_frame_types_for_save(path)
        p_frames = [x[0] for x in frame_types if x[1]=='P']
        if p_frames:
            basename = os.path.splitext(os.path.basename(path))[0]
            dir_local_p_frames = I_AND_P_FRAMES_DIR + basename + "/P-FRAMES/"
            if not os.path.exists(dir_local_p_frames):
                os.makedirs(dir_local_p_frames)
            cap = cv2.VideoCapture(path)
            index_show = 1
            for frame_no in p_frames:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
                frame = cap.read()[1]
                outname = 'p_'+str(frame_no)+'.jpg'               
                cv2.imwrite(dir_local_p_frames + outname, frame)
                self.status_save_p_frames_changed.emit(str(index_show) + " from " + str(len(p_frames)))
                index_show = index_show + 1
            cap.release()
            self.is_save_p_frames_changed.emit(True)
        else:
            pass
    def __del__(self):
        del self
    def stop(self):
        self._isRunning = False
        self.isRunning = False
        self.isFinished = True
        self.exit()
        self.quit()
        del self
