# -*- coding: utf-8 -*-
# Copyright 2015 Alex Woroschilow (alex.woroschilow@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import time
from PyQt5 import QtCore


class TimeIntervalThread(QtCore.QThread):

    refresh = QtCore.pyqtSignal(object)
    interval = 5

    def __init__(self, interval=5):
        super(TimeIntervalThread, self).__init__()
        self.interval = interval

    def run(self):
        starttime = time.time()
        while True:
            time.sleep(self.interval)
            self.refresh.emit((starttime, time.time()))

