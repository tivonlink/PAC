from PyQt5.QtCore import QItemSelectionModel, pyqtSlot, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QAbstractItemView, QWidget, QMessageBox, QInputDialog

from movement_monitor.models.MovementStatusNotifier import MovementStatusNotifier
from movement_monitor.views.NotificationSettingDialogUI import NotificationSettingDialogUI
import random

class NotificationSettingDialog(QDialog):
    def __init__(self, parent: QWidget, notifier: MovementStatusNotifier):
        super().__init__(parent)
        self.__ui = NotificationSettingDialogUI()
        self.__ui.setupUi(self)
        self.__notifier = notifier

        self.__data_model = QStandardItemModel(self)
        self.__selection_model =QItemSelectionModel(self.__data_model)

        self.__ui.lsv_subscribers.setModel(self.__data_model)
        self.__ui.lsv_subscribers.setSelectionModel(self.__selection_model)
        self.__ui.lsv_subscribers.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.__ui.lsv_subscribers.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.__notifier.signals.subscribers_changed.connect(self.on_subscribers_changed)

        self.__notifier.signals.subscribers_changed.emit(self.__notifier.subscribers)


    #notifier signal slots
    @pyqtSlot(list)
    def on_subscribers_changed(self, subscribers: list):
        self.__data_model.clear()
        self.__data_model.appendColumn([QStandardItem("Mobile Phone Number")])
        for m in subscribers:
            self.__ui.lsv_subscribers.model().appendRow(QStandardItem(m))

    #ui signal slots
    @pyqtSlot()
    def on_btn_remove_subscriber_clicked(self):
        if len(self.__selection_model.selection().indexes())>0:
            buffer = list(self.__data_model.itemData(i)[0]
                          for i in self.__selection_model.selection().indexes())
            for number in buffer:
                self.__notifier.remove_subscriber(number)

    @pyqtSlot()
    def on_btn_add_subscriber_clicked(self):
        phoneNum = self.__ui.txt_phone_number.text()
        print("adding ", phoneNum)
        if len(phoneNum)!=14:
            QMessageBox.warning(self,"Error","Phone number must have 11 digits.")
            return
        #logic for validation code
        code = str.join("", random.sample("0123456789",6))
        MovementStatusNotifier.send_verification_code(code, phoneNum)
        input_code, flag = QInputDialog.getText(self,"Phone Number Verification",
                             "6 digit verification code:")
        if flag and code == input_code:
            self.__notifier.add_subscriber(self.__ui.txt_phone_number.text())
        else:
            QMessageBox.warning(self, "Error", "Verification code wrong, could not add phone number to subscribers.")

    def on_btn_clear_subscriber_clicked(self):
        self.__notifier.clear_subscribers()


