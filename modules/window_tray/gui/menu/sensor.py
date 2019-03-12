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

from .widget.gauge import Gauge
from .thread import TimeIntervalThread
from .widget.button import RadioButton


class MenuSensorsAction(QtWidgets.QGroupBox):

    brightness = 0
    sensor = QtCore.pyqtSignal(bool, object)
    ambientLight = QtCore.pyqtSignal(int)
    thread = TimeIntervalThread() 

    @inject.params(config='config', sensors='sensors')
    def __init__(self, config=None, sensors=None):
        super(MenuSensorsAction, self).__init__()
        if sensors is None or config is None: return None
        
        layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel('Ambient light')
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.gauge = Gauge(120)
        self.ambientLight.connect(self.gauge.value)
        layout.addWidget(self.gauge)

        for device in sensors.devices:
            if device is None: continue
 
            checkbox = RadioButton(device.name)
            checkbox.setChecked(int(config.get('sensors.{}'.format(device.code))))
            
            layout.addWidget(checkbox)

            action = functools.partial(self.toggle, checkbox=checkbox, device=device) 
            checkbox.toggled.connect(action)
            
            action = functools.partial(self.refresh, checkbox=checkbox, device=device) 
            self.thread.refresh.connect(action)

        self.setLayout(layout)

        self.thread.start()

    @inject.params(config='config')
    def toggle(self, state=None, config=None, checkbox=None, device=None):
        if config is None or checkbox is None or device is None: return None

        config.set('sensors.{}'.format(device.code), '{}'.format(int(state)))        
        self.refresh(None, checkbox=checkbox, device=device)

    @inject.params(config='config')
    def refresh(self, event=None, config=None, checkbox=None, device=None):
        if config is None or checkbox is None or device is None: return None

        enabled = config.get('brightness.enabled')
        threshold = config.get('brightness.threshold')
        # If the sensor was disabled do not request the values
        # this is important especially for the webcameras
        # because it is expensive to get and process the picturess
        if not checkbox.isChecked(): return None
        if not int(enabled): return None
        
        # cache the value in the variable to avoid 
        # the new read of the device brightness value
        brightness = device.brightness
        # Do nothing if there are not brightness changes  
        if self.brightness == brightness: return None

        difference = math.fabs(self.brightness - brightness)
        if difference < int(threshold): return None

        self.ambientLight.emit(brightness)
        self.brightness = brightness

    def quit(self):
        if self.thread is None: return None
        self.thread.exit()
