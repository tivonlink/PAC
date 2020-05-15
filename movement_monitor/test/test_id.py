import os
import sys
import unittest

from PyQt5.QtWidgets import QApplication
#from id_validator import validator
from collections import deque
from PyQt5.QtCore import QTimer, QRect, QPoint
import time
import cv2
import os.path
import ffmpeg
import numpy

from twilio.rest import Client as twClient
from twilio.http.http_client import TwilioHttpClient as twHttpClient



class POCTest(unittest.TestCase):
    # def test_id_validator(self):
    #
    #     # 15222119870917xx3x
    #     count = 0
    #     for xx in range(100):
    #         for g in [1, 3, 5, 7, 9]:
    #             for x in range(10):
    #
    #                 id_num = "15222119870917%0d%d%d" % (xx, g, x)
    #
    #                 if validator.is_valid(id_num):
    #                     count += 1
    #                     print(count, id_num)
    #             id_num = "15222119870917%0d%dX" % (xx, g)
    #             if validator.is_valid(id_num):
    #                 count += 1
    #                 print(count, id_num)
    #             #    pass
    #
    #     self.assertTrue(True)

    def test_dequeue(self):
        q0 = deque(maxlen=4)
        q0.append(1)
        q0.append(2)
        q0.append(3)
        q0.append(4)
        print(q0)
        q0.append(5)
        print(q0)

        q1 = deque(q0, maxlen=2)
        print(q1)

        q2 = deque(q0, maxlen=6)
        print(q2)
        q2.append(6)
        q2.append(7)
        q2.append(8)
        print(q2)

    def test_video_cap(self):
        print(os.getcwd())
        fpath = "../resource/whole view.mp4"
        print(os.path.isfile(fpath))
        vc = cv2.VideoCapture(fpath)
        self.assertTrue(vc.isOpened())
        success, im = vc.read()
        if success:
            print(im)
            cv2.imshow("image", im)

        pass

    def test_qrect(self):
        rect = QRect( atopLeft=QPoint(0,0),abottomRight=QPoint(0,0))
        print(rect.isNull())
        print(rect.topLeft())
        print(rect.bottomRight())

        rect.setTopLeft(QPoint(1,1))
        rect.setBottomRight(QPoint(3,3))

        print(rect.isNull())
        print(rect.topLeft())
        print(rect.bottomRight())
        print(rect.height())
        print(rect.width())
        print(rect.center())

    @staticmethod
    def read_frame_by_time(in_file: str, time: int):
        """
        read frame at specified time
        """
        out, err = (
            ffmpeg.input(in_file, ss=time)
                .output('pipe:', vframes=1, format='image2', vcodec='mjpeg')
                .run(capture_stdout=True)
        )
        return out

    @staticmethod
    def get_video_info(in_file:str):
        """
        read video basic information
        """
        try:
            probe = ffmpeg.probe(in_file)
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            if video_stream is None:
                print('No video stream found', file=sys.stderr)
                sys.exit(1)
            return video_stream
        except ffmpeg.Error as err:
            print(str(err.stderr, encoding='utf8'))
            sys.exit(1)

    def test_ffmpeg(self):
        file_path = "../resource/oscillation test 20cycle.avi"
        video_info = self.get_video_info(file_path)
        print(video_info)
        out = self.read_frame_by_time(file_path,10)
        image_array = numpy.asarray(bytearray(out),dtype="uint8")
        image = cv2.imencode(image_array,cv2.IMREAD_GRAYSCALE)
        cv2.imshow("frame",image)
        cv2.waitKey()


    def test_twilio(self):
        sid = "AC81f933fac5b6c884b03864e0c088334d"
        token ="38e7724f25392b6dcf60ceaaa2332997"
        number = "+12058800988"
        receiver = "+8618516703450"
        http_client = twHttpClient(proxy={"http":"http://lks00043:Bqqq,001@10.180.41.77:3128",
                                          "https":"http://lks00043:Bqqq,001@10.180.41.77:3128"})
        client = twClient(sid,token,http_client=http_client)

        message = client.messages.create(
            to=receiver,
            from_=number,
            body="Hellow from Python!")

        print(message.status)

if __name__ == '__main__':
    unittest.main()
