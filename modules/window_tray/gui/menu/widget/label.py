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
import math
import inject    
from PyQt5 import QtWidgets

from modules.window_tray.gui.menu.thread import TimeIntervalThread


class BacklightLabel(QtWidgets.QLabel):
    
    thread = TimeIntervalThread(1) 

    def __init__(self, device):
        
        text = "{}: {:>.0f} %".format(device.name, device.brightness)
        super(BacklightLabel, self).__init__(text)
        
        self.value = device.brightness
        self.device = device
        
        self.thread.refresh.connect(self.refresh)
        self.thread.start()
        
    @inject.params(config='config')
    def refresh(self, event=None, config=None):
        if config is None: return None
        if event is None: return None

        brightness = self.device.brightness
        if self.value == brightness: return None
         
        text = '{:>s}: {:>.0f} %'.format(self.device.name, brightness)
        self.setText(text)

        threshold = math.fabs(self.value - brightness)
        if threshold < int(config.get('brightness.threshold')):
            return None

        self.value = brightness

