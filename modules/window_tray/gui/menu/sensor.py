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
import functools

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt 

from .widget.button import SensorsRadioButton
from .widget.gauge import Gauge
from .thread import TimeIntervalThread


class MenuSensorsAction(QtWidgets.QGroupBox):

    brightness = 0
    sensor = QtCore.pyqtSignal(bool, object)
    ambientLight = QtCore.pyqtSignal(int)
    thread = TimeIntervalThread() 

    @inject.params(config='config', sensors='sensors')
    def __init__(self, config=None, sensors=None):
        if sensors is None: return None
        if config is None: return None
        super(MenuSensorsAction, self).__init__()
        self.setMinimumWidth(120)
        
        layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel('Ambient light')
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.gauge = Gauge(None, 120)
        self.ambientLight.connect(self.gauge.value)
        layout.addWidget(self.gauge)

        for device in sensors.devices:
            if device is None: continue
 
            checkbox = SensorsRadioButton('{:>s}'.format(device.name))
            checkbox.setChecked(int(config.get('sensors.{}'.format(device.code))))
            checkbox.ambientLight.connect(lambda x: self.ambientLight.emit(x))

            action = functools.partial(self.toggle, checkbox=checkbox, device=device) 
            checkbox.toggled.connect(action)
            
            action = functools.partial(self.refresh, checkbox=checkbox, device=device) 
            self.thread.refresh.connect(action)
            
            layout.addWidget(checkbox)

        self.setLayout(layout)

        self.thread.start()

    @inject.params(config='config')
    def toggle(self, state=None, config=None, checkbox=None, device=None):
        if config is None: return None
        if checkbox is None: return None
        if device is None: return None

        config.set('sensors.{}'.format(device.code), '{}'.format(int(state)))        
        self.refresh(None, checkbox=checkbox, device=device)

    @inject.params(config='config')
    def refresh(self, event=None, config=None, checkbox=None, device=None):
        if config is None: return None
        if checkbox is None: return None
        if device is None: return None

        # If the sensor was disabled do not request the values
        # this is important especially for the webcameras
        # because it is expensive to get and process the picturess
        if not int(config.get('sensors.{}'.format(device.code))): 
            return None

        brightness = device.brightness
        # Do nothing if there are not brightness changes  
        if self.brightness == brightness: return None

        threshold = math.fabs(self.brightness - brightness)
        if threshold < int(config.get('brightness.threshold')):
            return None

        if not int(config.get('brightness.enabled')): return None
        self.ambientLight.emit(brightness)
        self.brightness = brightness

    def quit(self):
        self.thread.exit()
