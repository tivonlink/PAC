from enum import Enum
from PyQt5.QtCore import QRect, QObject, QTimer, pyqtSignal, pyqtSlot
from collections import deque
import cv2
from skimage.measure import compare_ssim
import os
import numpy as np


class MovementStatus(Enum):
    Moving = 1
    Stopped = 2
    Processing = 3


class MonitorStatus(Enum):
    Running = 1
    Stopped = 0


class VideoSourceType(Enum):
    File = 0
    Stream = 1
    NotValid = 2


class MovementMonitorSignal(QObject):
    image_queue_changed = pyqtSignal()
    image_changed = pyqtSignal(np.ndarray)
    video_source_changed = pyqtSignal(str)
    monitor_status_changed = pyqtSignal(MonitorStatus)
    movement_status_changed = pyqtSignal(MovementStatus)
    message = pyqtSignal(str)
    image_rect_changed = pyqtSignal(QRect)


class MovementMonitor(QObject):
    def __init__(self):
        super().__init__()
        # properties
        self.__timer = QTimer()
        self.__timer_hit = 0
        self.__timer.setSingleShot(False)
        self.__timer.setInterval(1000)

        self.__video_source = ""
        self.__video_source_type = VideoSourceType.NotValid

        self.__image = None

        self.__image_queue = deque(maxlen=10)

        self.__image_rect = QRect()

        self.signals = MovementMonitorSignal()

        # signals connections
        self.signals.image_queue_changed.connect(self.on_image_queue_changed)
        self.signals.monitor_status_changed.connect(self.on_monitor_status_changed)
        self.signals.video_source_changed.connect(self.on_video_source_changed)

        # TODO: test code, to be removed
        self.__timer.timeout.connect(self.on_timer_timeout)

    @property
    def image_rect(self):
        return self.__image_rect

    @image_rect.setter
    def image_rect(self, value: QRect):
        if self.__image_rect!=value:
            self.__image_rect = value
            self.signals.image_rect_changed.emit(value)



    @property
    def video_source(self):
        return self.__video_source

    @video_source.setter
    def video_source(self, value: str):
        if self.__video_source != value:
            self.__video_source_type = self.check_video_source_type(value)
            if self.__video_source_type != VideoSourceType.NotValid:
                self.__video_source = value
                self.signals.video_source_changed.emit(value)
            else:
                self.__error("Video source not valid or supported. Open video failed.")

    @property
    def sampling_interval(self):
        return self.__timer.interval()

    @sampling_interval.setter
    def sampling_interval(self, value: int):
        if self.__timer.interval() != value:
            self.__timer.setInterval(int(value))

    @property
    def sampling_quantity(self):
        return self.__image_queue.maxlen

    @sampling_quantity.setter
    def sampling_quantity(self, value: int):
        if self.__image_queue.maxlen != value:
            self.__image_queue = deque(self.__image_queue, maxlen=value)

    @property
    def monitor_status(self):
        if self.__timer.isActive():
            return MonitorStatus.Running
        else:
            return MonitorStatus.Stopped

    @pyqtSlot(MonitorStatus)
    def on_monitor_status_changed(self, status: MonitorStatus):
        if status == MonitorStatus.Stopped:
            self.__timer.stop()
            self.__timer_hit = 0
            self.__image_queue.clear()
        else:
            self.__timer.start()

    @pyqtSlot()
    def on_timer_timeout(self):
        self.__timer_hit +=1
        print(f"timer timeout hit {self.__timer_hit}")
        if self.__video_source_type == VideoSourceType.File:
            vc = cv2.VideoCapture(self.__video_source)
            if vc.isOpened():
                vc.set(cv2.CAP_PROP_POS_MSEC, self.__timer_hit*self.sampling_interval)
                success, img = vc.read()
                if success:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    self.signals.image_changed.emit(img)
                    self.compute_movement_status(img)
            vc.release()
        elif self.__video_source_type == VideoSourceType.Stream:
            #TODO: add video stream logic here
            pass
        else:
            pass


    @pyqtSlot()
    def on_image_queue_changed(self):
        print("on image queue changed triggered")

    @pyqtSlot(str)
    def on_video_source_changed(self, source_path):
        vc = cv2.VideoCapture(source_path)
        success, im = vc.read()
        if success:
            im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            self.signals.image_changed.emit(im)
        pass

    @staticmethod
    def check_video_source_type(source: str) -> VideoSourceType:
        vc = cv2.VideoCapture(source)
        ret = VideoSourceType.NotValid
        if vc.isOpened():
            if os.path.isfile(source):
                ret = VideoSourceType.File
            else:
                ret = VideoSourceType.Stream
        vc.release()
        return ret

    def __error(self, msg: str):
        self.signals.message.emit(msg)

    def is_ready(self):
        if self.video_source!="":
            return True
        else:
            return False


    def compute_movement_status(self,im:np.ndarray):
        if(len(self.__image_queue)==self.__image_queue.maxlen):
            ssim_queue = deque(maxlen=self.__image_queue.maxlen)
            imcpy = im.copy()
            if self.__image_rect.isNull() == False:
                rect = QRect(self.__image_rect)
                if rect.top() < 0:
                    rect.setTop(0)
                if rect.left() < 0:
                    rect.setLeft(0)
                print("adjuested rect ", rect)

            print("original comparing image shape: ", imcpy.shape)
            if self.__image_rect.isNull() == False:
                imcpy = imcpy[rect.top():rect.bottom(), rect.left():rect.right() ]
                print("cropped comparing image shape: ", imcpy.shape)

            for context in self.__image_queue:
                print("original context image shape: ", context.shape)
                if self.__image_rect.isNull() == False:
                    context = context[rect.top():rect.bottom(), rect.left():rect.right()]
                    print("cropped context image shape: ", context.shape)

                quality = compare_ssim(context,imcpy,gaussian_weights=True)
                ssim_queue.append(quality)
            print(ssim_queue)
            print(sum(map(lambda m: m>0.9,ssim_queue)))
            if sum(map(lambda m: m>0.9,ssim_queue))>len(ssim_queue)*0.8:
                self.signals.movement_status_changed.emit(MovementStatus.Stopped)
            else:
                self.signals.movement_status_changed.emit(MovementStatus.Moving)
        else:
            self.signals.movement_status_changed.emit(MovementStatus.Processing)
        self.__image_queue.append(im)
