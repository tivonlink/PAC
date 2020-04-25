from enum import Enum
from PyQt5.QtCore import QRect, QObject, QTimer, pyqtSignal, pyqtSlot
from collections import deque
import cv2
import time
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


class MovementMonitor(QObject):
    def __init__(self):
        super().__init__()
        # properties
        self.__timer = QTimer()
        self.__timer.setSingleShot(False)
        self.__timer.setInterval(10000)

        self.__video_source = ""
        self.__video_source_type = VideoSourceType.NotValid

        self.__image = None

        self.__image_queue = deque(maxlen=10)

        self.signals = MovementMonitorSignal()

        # signals connections
        self.signals.image_queue_changed.connect(self.on_image_queue_changed)
        self.signals.monitor_status_changed.connect(self.on_monitor_status_changed)
        self.signals.video_source_changed.connect(self.on_video_source_changed)
        # TODO: test code, to be removed
        self.__timer.timeout.connect(self.on_timer_timeout)

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
                self.__success()
            else:
                self.__error("Video source not valid or supported. Open video failed.")

    @property
    def sampling_interval(self):
        return int(self.__timer.interval() / 1000)

    @sampling_interval.setter
    def sampling_interval(self, value: int):
        if self.__timer.interval() != value:
            self.__timer.setInterval(int(value * 1000))

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
        print(self.__timer)
        if status == MonitorStatus.Stopped:
            self.__timer.stop()
        else:
            self.__timer.start()

    @pyqtSlot()
    def on_timer_timeout(self):
        print("timer timeout hint")

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

    def __success(self):
        self.signals.message.emit("")

    def __error(self, msg: str):
        self.signals.message.emit(msg)
