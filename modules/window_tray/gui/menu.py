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
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from .thread import TimeIntervalThread


class BacklightDeviceAction(QtWidgets.QAction):

    changed = QtCore.pyqtSignal(int)

    thread = TimeIntervalThread() 
    device = None
    value = None
    adjust = True

    def __init__(self, device, menu):
        super(BacklightDeviceAction, self).__init__('{:>s}: {:>.0f} %'.format(
            device.name, device.brightness
        ), menu)
        
        self.value = device.brightness
        self.device = device
        
        self.thread.refresh.connect(lambda x: self.refresh())
        self.thread.start()

    def refresh(self):
        name = self.device.name 
        brightness = self.device.brightness
        if self.value == brightness: 
            return None
         
        self.setText('{:>s}: {:>.0f} %'.format(name, brightness))
        self.changed.emit(brightness)
        self.value = brightness

    def change(self, value=None):
        if value is None or not self.adjust:
            return None
        self.device.brightness = value if value >= 5 else 5
        return None

    def adjust(self, value=None):
        self.adjust = value

    def quit(self):
        self.thread.exit()


class AmbientlightDeviceAction(QtWidgets.QAction):

    changed = QtCore.pyqtSignal(int)
    thread = TimeIntervalThread() 
    device = None
    value = None

    def __init__(self, device, menu):
        super(AmbientlightDeviceAction, self).__init__('{:>s}: {:>.0f} %'.format(
            device.name, device.brightness
        ), menu)
        
        self.value = device.brightness
        self.device = device
        
        self.thread.refresh.connect(lambda x: self.refresh())
        self.thread.start()

    def refresh(self):
        name = self.device.name 
        brightness = self.device.brightness
        if self.value == brightness: 
            return None
         
        self.setText('{:>s}: {:>.0f} %'.format(name, brightness))
        self.changed.emit(brightness)
        self.value = brightness

    def quit(self):
        self.thread.exit()

