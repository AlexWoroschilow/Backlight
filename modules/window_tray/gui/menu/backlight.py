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
import inject
import functools

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt 

from .widget.gauge import Gauge
from .thread import TimeIntervalThread
from .widget.button import RadioButton


class MenuBacklightAction(QtWidgets.QGroupBox):

    backLight = QtCore.pyqtSignal(int)

    thread = TimeIntervalThread() 

    @inject.params(config='config' , backlight='backlight')
    def __init__(self, config=None, backlight=None):
        super(MenuBacklightAction, self).__init__()
        if backlight is None or config is None: return None
        
        layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel('Backlight')
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.gauge = Gauge(120)
        self.backLight.connect(self.gauge.value)
        layout.addWidget(self.gauge)
        
        for device in backlight.devices:
            if device is None: continue
            
            checkbox = RadioButton(device.name)
            checkbox.setChecked(int(config.get('backlights.{}'.format(device.code))))
            
            layout.addWidget(checkbox)
            
            action = functools.partial(self.toggle, checkbox=checkbox, device=device) 
            checkbox.toggled.connect(action)
            
            action = functools.partial(self.refresh, checkbox=checkbox, device=device) 
            self.thread.refresh.connect(action)

        self.setLayout(layout)
        
        self.thread.start()

    @inject.params(backlights='backlight')
    def update(self, value=None, backlights=None):
        if backlights is None or value is None: return None
        for device in backlights.devices:
            if device is None: continue
            if value is not None and value < 5:
                device.brightness = 5
            if value is not None and value >= 5:
                device.brightness = value

    @inject.params(config='config')
    def toggle(self, state=None, config=None, checkbox=None, device=None):
        if config is None or checkbox is None or device is None: return None

        config.set('backlights.{}'.format(device.code), '{}'.format(int(state)))        
        self.refresh(None, checkbox=checkbox, device=device)

    def refresh(self, event=None, checkbox=None, device=None):
        if checkbox is None or device is None: return None
        if not checkbox.isChecked(): return None
        self.backLight.emit(device.brightness)

    def quit(self):
        self.thread.exit()

