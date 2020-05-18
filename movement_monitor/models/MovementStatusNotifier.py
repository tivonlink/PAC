from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal

from movement_monitor.models.MovementMonitor import MovementStatus, MovementMonitor
from twilio.rest import Client as twClient
from twilio.http.http_client import TwilioHttpClient as twHttpClient

from os import path
import xml.etree.ElementTree as xmlElementTree


class MovementStatusNotifierSignal(QObject):
    subscribers_changed = pyqtSignal(list)


class MovementStatusNotifier(QObject):
    def __init__(self, monitor: MovementMonitor):
        super().__init__()
        # public member
        self.signals = MovementStatusNotifierSignal()

        # private member
        self.__subscribers = []
        self.__monitor = monitor
        self.__movement_status = MovementStatus.Stopped
        self.__setting_file = "./resource/setting.xml"

        # read setting file
        if path.exists(self.__setting_file):
            xmlTree = xmlElementTree.parse(self.__setting_file)
            for phoneElement in xmlTree.getroot().findall("subscribers/phone"):
                self.__subscribers.append(phoneElement.get("number"))

        # exteranl signal connection
        self.__monitor.signals.movement_status_changed.connect(self.on_movement_status_changed)

    def __del__(self):
        # write setting file
        if len(self.__subscribers) > 0:
            root = xmlElementTree.Element("settings")
            subscribers = xmlElementTree.SubElement(root, "subscribers")
            for num in self.__subscribers:
                phone = xmlElementTree.SubElement(subscribers, "phone", {"number": num})

            xmlTree = xmlElementTree.ElementTree(root)
            xmlTree.write(self.__setting_file,
                          encoding="utf-8",
                          method="xml",
                          xml_declaration=True)

    @pyqtSlot(MovementStatus)
    def on_movement_status_changed(self, status: MovementStatus):
        if self.__movement_status == MovementStatus.Moving \
                and status == MovementStatus.Stopped:
            sid = "AC81f933fac5b6c884b03864e0c088334d"
            token = "38e7724f25392b6dcf60ceaaa2332997"
            number = "+12058800988"
            http_client = twHttpClient(proxy={"http": "http://lks00043:Bqqq,001@10.180.41.77:3128",
                                              "https": "http://lks00043:Bqqq,001@10.180.41.77:3128"})
            client = twClient(sid, token, http_client=http_client)
            for receiver in self.__subscribers:
                message = client.messages.create(
                    to=receiver,
                    from_=number,
                    body="Moniterd movement has stopped!, Please check.")

                print(F"sent message to subscribers {receiver}")
        if self.__movement_status != status:
            self.__movement_status = status

    @property
    def subscribers(self):
        return self.__subscribers

    def add_subscriber(self, phone_number: str):
        if self.__subscribers.count(phone_number) == 0:
            self.__subscribers.append(phone_number)
            self.signals.subscribers_changed.emit(self.__subscribers)

    def remove_subscriber(self, phone_number: str):
        self.__subscribers.remove(phone_number)
        self.signals.subscribers_changed.emit(self.__subscribers)

    def clear_subscribers(self):
        self.__subscribers.clear()
        self.signals.subscribers_changed.emit(self.__subscribers)

    @staticmethod
    def send_verification_code(code: str, phone: str):
        sid = "AC81f933fac5b6c884b03864e0c088334d"
        token = "38e7724f25392b6dcf60ceaaa2332997"
        number = "+12058800988"
        http_client = twHttpClient(proxy={"http": "http://lks00043:Bqqq,001@10.180.41.77:3128",
                                          "https": "http://lks00043:Bqqq,001@10.180.41.77:3128"})
        client = twClient(sid, token, http_client=http_client)

        message = client.messages.create(
            to=phone,
            from_=number,
            body=F"Your verification code is {code}. \n \
                This message is sent by SAIFEI Movement Monitor.  \
                If this is not your operation, please ignore.")

        print(F"Sent code to phone {phone}")
