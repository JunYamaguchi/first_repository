#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import serial
import os
import json
import struct
import time
import fcntl
import threading
import traceback
from optparse import OptionParser

import xbee as python_xbee
import paho.mqtt.client as mqtt

class TestClass:
    def __init__(self, test_num, test_dict):
        self.test_num  = test_num
        self.test_dict = test_dict

    def test_add(self):
        print('before : %d' % self.test_num)
        print(id(self.test_num))
        self.test_num += 1
        print('after : %d' % self.test_num)
        print(id(self.test_num))

    def edit_dict(self, value):
        print(self.test_dict)
        self.test_dict['yamada'] = value
        print(self.test_dict)

    # Raspi側のxbeeでパケットを受信してパブリッシュするプロセス
    def process_run(self):
        process = threading.Thread(target=self.test_process, args=())
        process.start()

    def test_process(self):
        test_class1.edit_dict(2020)

if __name__ == '__main__':

    test_num  = 1  # immutable
    test_dict = {"yamada":75}  # mutable

    test_class1 = TestClass(test_num, test_dict)
    test_class2 = TestClass(test_num, test_dict)

    print('===class mesod===')

    test_class1.test_add()
    test_class1.test_add()
    test_class2.test_add()  # class間でもimmutableな値の変更は反映されない

    test_class1.edit_dict(99)
    test_class1.edit_dict(1000)

    test_class2.edit_dict(22) # class間でもmutableな値は反映される

    print('===main===')
    print('main test_num : %d' % test_num)  # mainと関数間でimmutableな値は更新されない
    print(test_dict)  # mainと関数間で、mutableな値は更新される

    print('===sub process===')
    test_class1.process_run()

    time.sleep(1)  ## subプロセス完了をちょっと待つ

    test_class2.edit_dict(1111)  # 別オブジェクト内のsubプロセスでの変更もclass間で反映される

    print(test_dict)
