import os
import sys
import unittest

from PyQt5.QtWidgets import QApplication
from id_validator import validator
from collections import deque
from PyQt5.QtCore import QTimer
import time
import cv2
import os.path


class POCTest(unittest.TestCase):
    def test_id_validator(self):

        # 15222119870917xx3x
        count = 0
        for xx in range(100):
            for g in [1, 3, 5, 7, 9]:
                for x in range(10):

                    id_num = "15222119870917%0d%d%d" % (xx, g, x)

                    if validator.is_valid(id_num):
                        count += 1
                        print(count, id_num)
                id_num = "15222119870917%0d%dX" % (xx, g)
                if validator.is_valid(id_num):
                    count += 1
                    print(count, id_num)
                #    pass

        self.assertTrue(True)

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


if __name__ == '__main__':
    unittest.main()
