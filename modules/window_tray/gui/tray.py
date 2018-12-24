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
from PyQt5.QtCore import Qt 
from PyQt5 import QtCore
from PyQt5 import QtGui

from .menu import MenuSettingsAction
from .menu import MenuSensorsAction
from .menu import MenuBacklightAction


class TrayWidget(QtWidgets.QSystemTrayIcon):
    
    pause = QtCore.pyqtSignal(int)
    threshold = QtCore.pyqtSignal(int)

    quit = QtCore.pyqtSignal()
    
    @inject.params(backlight='backlight', sensors='sensors')
    def __init__(self, icon, app=None, backlight=None, sensors=None):
        QtWidgets.QApplication.__init__(self, icon, app)
        self.activated.connect(self.onActionClick)

        self.menu = QtWidgets.QMenu()
        
        self.settings = MenuSettingsAction(self)
        self.settings.threshold.connect(self.onActionThreshold)
        self.settings.pause.connect(self.onActionPause)
        self.menu.addAction(self.settings)

        self.menu.addSeparator()

        self.sensors = MenuSensorsAction(self)
        self.menu.addAction(self.sensors)

        self.menu.addSeparator()

        self.backlight = MenuBacklightAction(self)
        self.sensors.ambientLight.connect(self.backlight.onActionAmbientLight)
        self.menu.addAction(self.backlight)
        
        self.menu.addSeparator()

        button = QtWidgets.QAction('Quit', self.menu)
        button.triggered.connect(lambda x: self.quit.emit())        
        self.menu.addAction(button)

        self.setContextMenu(self.menu)

        self.show()

    def onActionClick(self, value):
        if value == self.Trigger:  # left click!
            self.menu.exec_(QtGui.QCursor.pos())

    @inject.params(config='config')
    def onActionPause(self, value=None, config=None):
        config.set('brightness.enabled', '{}'.format(int(value)))

    @inject.params(config='config')
    def onActionThreshold(self, value=None, config=None):
        config.set('brightness.threshold', '{}'.format(int(value)))

