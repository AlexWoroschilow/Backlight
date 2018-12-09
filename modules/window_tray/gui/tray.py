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
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from .menu import BacklightDeviceAction
from .menu import AmbientlightDeviceAction


class DictionaryTray(QtWidgets.QSystemTrayIcon):
    
    ambientlights = []
    
    pause = QtCore.pyqtSignal(int)
    quit = QtCore.pyqtSignal()
    
    @inject.params(backlight='backlight', ambientlight='ambientlight')
    def __init__(self, icon, app=None, backlight=None, ambientlight=None):
        QtWidgets.QApplication.__init__(self, icon, app)
        self.activated.connect(self.onActionClick)

        self.menu = QtWidgets.QMenu()

        pause = QtWidgets.QAction('Adjust brightness', self.menu)
        pause.triggered.connect(lambda x: self.pause.emit(x))        
        pause.setCheckable(True)
        pause.setChecked(True)
        self.menu.addAction(pause)
        
        self.menu.addSeparator()

        for device in ambientlight.devices:
            ambientlight_device = AmbientlightDeviceAction(device, self.menu)
            self.ambientlights.append(ambientlight_device)
            self.quit.connect(ambientlight_device.quit)
            self.menu.addAction(ambientlight_device)
        
        for device in backlight.devices:
            backlight_device = BacklightDeviceAction(device, self.menu)
            for index, ambientlight in enumerate(self.ambientlights):
                ambientlight.changed.connect(backlight_device.change)
            self.pause.connect(backlight_device.adjust)
            self.quit.connect(backlight_device.quit)
            self.menu.addAction(backlight_device)

        self.menu.addSeparator()

        exit = QtWidgets.QAction('Quit', self.menu)
        exit.triggered.connect(lambda x: self.quit.emit())        
        self.menu.addAction(exit)

        self.setContextMenu(self.menu)

        self.show()

    def onActionClick(self, value):
        if value == self.Trigger:  # left click!
            self.menu.exec_(QtGui.QCursor.pos())

