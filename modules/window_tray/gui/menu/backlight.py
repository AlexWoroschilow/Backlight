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

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt 

from .widget.gauge import Gauge
from .thread import TimeIntervalThread


class MenuBacklightAction(QtWidgets.QWidgetAction):

    thread = TimeIntervalThread() 

    @inject.params(backlight='backlight')
    def __init__(self, parent=None, backlight=None):
        if parent is None: return None
        super(MenuBacklightAction, self).__init__(parent)
        
        layout = QtWidgets.QGridLayout()

        collection = [device for device in backlight.devices]
        if not len(collection): return None

        self.label = QtWidgets.QLabel('Backlight')
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label, 0, 0, 1, len(collection))
        
        for index, device in enumerate(collection):
            if device is None: continue
            gauge = Gauge(None, 100)
            layout.addWidget(gauge, 1, index)
            label = QtWidgets.QLabel(device.name)
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label, 2, index)
            
            action = functools.partial(self.refresh, chart=gauge, device=device) 
            self.thread.refresh.connect(action)

        container = QtWidgets.QWidget()
        container.setStyleSheet('QWidget { background-color: #ffffff }')
        container.setLayout(layout)
        
        self.setDefaultWidget(container)
        self.thread.start()

    def onActionPause(self, value):
        self.pause = value

    @inject.params(backlights='backlight')
    def onActionAmbientLight(self, value=None, backlights=None):
        if backlights is None: return None
        if value is None: return None
        for device in backlights.devices:
            if device is None: continue
            if value is not None and value < 5:
                device.brightness = 5
            if value is not None and value >= 5:
                device.brightness = value

    def refresh(self, event=None, chart=None, device=None):
        if chart is None: return None
        if device is None: return None
        if event is None: return None
        chart.value(device.brightness)

    def quit(self):
        self.thread.exit()

