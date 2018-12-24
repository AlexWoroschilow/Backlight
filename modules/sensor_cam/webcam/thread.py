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
import math

from PyQt5 import QtCore


class TimeIntervalThread(QtCore.QThread):

    update = QtCore.pyqtSignal(float)

    def __init__(self, camera, width, height):
        super(TimeIntervalThread, self).__init__()
        self.camera = camera
        self.height = height
        self.width = width

    def _brightness(self, r, g, b):
        brightness = (r + r + b + g + g + g) / 6
        return (brightness / 255) * 100 

    @property
    def brightness(self):
        
        self.camera.start()
        time.sleep(0.1)
        
        image = self.camera.get_image()
        self.camera.stop()
    
        collection = []
        for x in range(0, self.width):
            for y in range(0, self.height):
                r, g, b, a = image.get_at((x, y))
                collection.append(self._brightness(r, g, b))
        return math.floor(sum(collection) / len(collection))

    def run(self):
        while True:
            try:
                brightness = self.brightness
                if brightness is not None and brightness:
                    self.update.emit(brightness)
            except SystemError:
                continue
            time.sleep(60)

