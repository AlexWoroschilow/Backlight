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

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from .thread import TimeIntervalThread


class SensorsRadioButton(QtWidgets.QRadioButton):
    ambientLight = QtCore.pyqtSignal(int)
    thread = TimeIntervalThread() 
    
    @inject.params(config='config')
    def __init__(self, device, config=None):
        self.name = device.name
        self.code = device.code
        self.device = device
        self.brightness = 0
        
        super(SensorsRadioButton, self).__init__("{}: {:>.0f} %".format(
            self.name, self.brightness
        ))
        
        self.toggled.connect(self.onActionToggle)
        if int(config.get('brightness.enabled')):
            self.ambientLight.emit(self.brightness)
        self.thread.refresh.connect(self.refresh)
        self.thread.start()
    
    @inject.params(config='config')
    def onActionToggle(self, state, config):
        config.set('sensors.{}'.format(self.code), '{}'.format(int(state)))        
        self.setText('{:>s}: {:>.0f} %'.format(
            self.name, self.device.brightness
        ))
    
    @inject.params(config='config')
    def refresh(self, event, config=None):
        
        enabled = config.get('sensors.{}'.format(self.code))
        if enabled is not None and int(enabled) == 0:
            return self.setText('{:>s}: ignored'.format(self.name))

        brightness = self.device.brightness
        self.setText('{:>s}: {:>.0f} %'.format(self.name, brightness))
        if self.brightness == brightness: 
            return None

        threshold = math.fabs(self.brightness - brightness)
        if threshold < int(config.get('brightness.threshold')):
            return None

        if int(config.get('brightness.enabled')):
            self.ambientLight.emit(brightness)
            self.brightness = brightness

    def quit(self):
        self.thread.exit()

