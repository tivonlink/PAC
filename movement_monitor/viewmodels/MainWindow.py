from PyQt5.QtCore import pyqtSlot, QRect, QPointF, QRectF, QPoint
from PyQt5.QtGui import QImage, QPixmap, QPen, QBrush, QColor
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QGraphicsScene, QGraphicsView, QInputDialog, QGraphicsRectItem

from movement_monitor.models.MovementMonitor import MovementMonitor, MonitorStatus, MovementStatus
from movement_monitor.views.MainWindowUI import MainWindowUI
import numpy as np
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__monitor = MovementMonitor()

        self.__ui = MainWindowUI()

        self.__ui.setupUi(self)
        self.__ui.graphicsView.setInteractive(True)
        self.__ui.graphicsView.setDragMode(QGraphicsView.RubberBandDrag)

        # init ui per monitor property
        self.__ui.spb_sampling_interval.setValue(self.__monitor.sampling_interval)
        self.__ui.spb_sampling_quantity.setValue(self.__monitor.sampling_quantity)
        self.__ui.lab_monitor_range.setText("(0,0),(0,0)")
        self.__ui.lab_video_source.setText(self.__monitor.video_source)
        self.__ui.lab_move_status.setText(MovementStatus.Stopped.name)



        # connect monitor's signals
        self.__monitor.signals.video_source_changed.connect(self.on_video_source_changed)
        self.__monitor.signals.image_changed.connect(self.on_image_changed)
        self.__monitor.signals.message.connect(self.on_monitor_message)
        self.__monitor.signals.image_rect_changed.connect(self.on_monitor_image_rect_changed)
        self.__monitor.signals.movement_status_changed.connect(self.on_movent_status_changed)


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

    @pyqtSlot(QRect)
    def on_monitor_image_rect_changed(self,rect:QRect):
        self.__ui.lab_monitor_range.setText("(0,0),(0,0)"
                                            if rect.isNull()
                                            else f"({rect.top():d},{rect.left():d}),({rect.bottom():d},{rect.right():d})")

    @pyqtSlot(MovementStatus)
    def on_movent_status_changed(self, status:MovementStatus):
        self.__ui.lab_move_status.setText(status.name)

    @pyqtSlot(str)
    def on_monitor_message(self, msg: str):
        self.__ui.statusbar.showMessage(msg)

    # ui widget signals slots
    @pyqtSlot()
    def on_btn_run_clicked(self):
        if self.__monitor.is_ready() ==False:
            self.__ui.statusbar.showMessage("No video source selected, could not start monitor.")
            return
        if self.__monitor.monitor_status == MonitorStatus.Stopped:
            self.__monitor.signals.monitor_status_changed.emit(MonitorStatus.Running)
            self.__ui.btn_run.setText("Stop")
        else:
            self.__monitor.signals.monitor_status_changed.emit(MonitorStatus.Stopped)
            self.__ui.btn_run.setText("Start")

    @pyqtSlot()
    def on_action_open_video_file_triggered(self):
        if self.__monitor.monitor_status == MonitorStatus.Running:
            self.__ui.statusbar.showMessage("Could not change video source during execution.")
            return

        filename, filetype = QFileDialog.getOpenFileName(self,
                                                         caption="open video file",
                                                         directory=os.path.curdir,
                                                         filter="mp4 (*.mp4);;wmv (*.wmv);;avi (*.avi)")
        if filename != "":
            self.__monitor.video_source = filename

    @pyqtSlot()
    def on_action_open_video_stream_triggered(self):
        if self.__monitor.monitor_status == MonitorStatus.Running:
            self.__ui.statusbar.showMessage("Could not change video source during execution.")
            return

        stream, flag = QInputDialog.getText(self,
                                            "please input valid video stream address",
                                            "stream address:")
        if flag:
            self.__monitor.video_source = stream

    @pyqtSlot(QRect, QPointF,QPointF)
    def on_graphicsView_rubberBandChanged(self, rect: QRect, pFrom:QPointF, pTo: QPointF):
        if self.__monitor.monitor_status == MonitorStatus.Running:
            self.__ui.statusbar.showMessage("Could not change monitor range during execution.")
            return

        if self.__ui.graphicsView.scene() != None and rect.isNull() == False:
            tl = self.__ui.graphicsView.mapToScene(rect.topLeft())
            br = self.__ui.graphicsView.mapToScene(rect.bottomRight())
            neoRect = QRect(QPoint(tl.x(),tl.y()),QPoint(br.x(),br.y()))
            neoRectF = QRectF(tl,br)
            for i in self.__ui.graphicsView.scene().items():
                if isinstance(i,QGraphicsRectItem):
                    self.__ui.graphicsView.scene().removeItem(i)
            self.__ui.graphicsView.scene().addRect(neoRectF,QPen(QColor(0,255,255,255)),QBrush(QColor(224,255,255,63)))
            self.__monitor.image_rect = neoRect

    @pyqtSlot()
    def on_action_clear_monitor_range_triggered(self):
        if self.__monitor.monitor_status == MonitorStatus.Running:
            self.__ui.statusbar.showMessage("Could not change monitor range during execution.")
            return

        for i in self.__ui.graphicsView.scene().items():
            if isinstance(i, QGraphicsRectItem):
                self.__ui.graphicsView.scene().removeItem(i)
        self.__monitor.image_rect = QRect()

    @pyqtSlot(int)
    def on_spb_sampling_interval_valueChanged(self,value:int):
        if self.__monitor.monitor_status == MonitorStatus.Running:
            self.__ui.statusbar.showMessage("Could not change monitor sampling intverval during execution.")
            self.__ui.spb_sampling_interval.setValue(self.__monitor.sampling_interval)
            return
        self.__monitor.sampling_interval=value

    @pyqtSlot(int)
    def on_spb_sampling_quantity_valueChanged(self,value: int):
        if self.__monitor.monitor_status == MonitorStatus.Running:
            self.__ui.statusbar.showMessage("Could not change monitor sampling quantity during execution.")
            self.__ui.spb_sampling_quantity.setValue(self.__monitor.sampling_quantity)
            return
        self.__monitor.sampling_quantity = value

    @pyqtSlot()
    def on_action_start_monitor_triggered(self):
        self.on_btn_run_clicked()

    @pyqtSlot()
    def on_action_quit_triggered(self):
        self.close()

    # functions
    @staticmethod
    def ndarray2qimage(im: np.ndarray):
        h, w = im.shape
        im = QImage(im.data, w, h, QImage.Format_Indexed8)
        return im



