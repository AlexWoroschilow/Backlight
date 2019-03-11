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
import inject
import pygame.camera

from PyQt5 import QtCore


class TimeIntervalThread(QtCore.QThread):

    update = QtCore.pyqtSignal(float)

    def __init__(self, device, width, height):
        super(TimeIntervalThread, self).__init__()
        self.source = device.source 
        self.device = device 
        self.height = height
        self.width = width

    def brightnessFromRGB(self, r, g, b):
        brightness = (r + r + b + g + g + g) / 6
        return (brightness / 255) * 100 

    @property
    def brightness(self):
        
        camera = pygame.camera.Camera(self.source, (self.width, self.height)) 
        
        camera.start()
        time.sleep(0.1)
        
        image = camera.get_image()
        camera.stop()
    
        collection = []
        for x in range(0, self.width):
            for y in range(0, self.height):
                r, g, b, a = image.get_at((x, y))
                collection.append(self.brightnessFromRGB(r, g, b))
        return math.floor(sum(collection) / len(collection))

    @inject.params(config='config')
    def run(self, config=None):
        while True:
            try:
                if not int(config.get('sensors.{}'.format(self.device.code))):
                    time.sleep(10)
                    continue
                brightness = self.brightness
                if brightness is not None and brightness:
                    self.update.emit(brightness)
            except (SystemError) as error:
                print(error)
                time.sleep(10)
                continue
            time.sleep(60)

