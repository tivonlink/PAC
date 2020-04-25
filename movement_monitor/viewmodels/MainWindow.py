from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QGraphicsScene, QInputDialog

from movement_monitor.models.MovementMonitor import MovementMonitor, MonitorStatus
from movement_monitor.views.MainWindowUI import MainWindowUI
import numpy as np
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__monitor = MovementMonitor()

        self.__ui = MainWindowUI()

        self.__ui.setupUi(self)

        # init ui per monitor property
        self.__ui.spb_sampling_interval.setValue(self.__monitor.sampling_interval)
        self.__ui.spb_sampling_quantity.setValue(self.__monitor.sampling_quantity)

        # connect monitor's signals
        self.__monitor.signals.video_source_changed.connect(self.on_video_source_changed)
        self.__monitor.signals.image_changed.connect(self.on_image_changed)
        self.__monitor.signals.message.connect(self.on_monitor_message)

    # monitor signals slots
    @pyqtSlot(np.ndarray)
    def on_image_changed(self, im: np.ndarray):
        if self.__ui.graphicsView.scene() is None:
            self.__ui.graphicsView.setScene(QGraphicsScene())
        self.__ui.graphicsView.scene().clear()
        self.__ui.graphicsView.scene().addPixmap(QPixmap.fromImage(self.ndarray2qimage(im)))
        pass

    @pyqtSlot(str)
    def on_video_source_changed(self, source: str):
        self.__ui.lab_video_source.setText(source)

    # TODO: deal with error messages
    @pyqtSlot(str)
    def on_monitor_message(self, msg: str):
        self.__ui.statusbar.showMessage(msg)

    # ui widget signals slots
    @pyqtSlot()
    def on_btn_run_clicked(self):
        if self.__monitor.monitor_status == MonitorStatus.Stopped:
            self.__monitor.signals.monitor_status_changed.emit(MonitorStatus.Running)
            self.__ui.btn_run.setText("Stop")
        else:
            self.__monitor.signals.monitor_status_changed.emit(MonitorStatus.Stopped)
            self.__ui.btn_run.setText("Start")

    @pyqtSlot()
    def on_action_open_video_file_triggered(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                                                         caption="open video file",
                                                         directory=os.path.curdir,
                                                         filter="mp4 (*.mp4);;wmv (*.wmv);;avi (*.avi)")
        if filename != "":
            self.__monitor.video_source = filename

    @pyqtSlot()
    def on_action_open_video_stream_triggered(self):
        stream, flag = QInputDialog.getText(self,
                                            "please input valid video stream address",
                                            "stream address:")
        if flag:
            self.__monitor.video_source = stream

    # functions
    @staticmethod
    def ndarray2qimage(im: np.ndarray):
        h, w = im.shape
        im = QImage(im.data, w, h, QImage.Format_Indexed8)
        return im
