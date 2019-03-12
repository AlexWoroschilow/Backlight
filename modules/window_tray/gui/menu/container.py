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

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from .settings import MenuSettingsAction
from .sensor import MenuSensorsAction
from .backlight import MenuBacklightAction


class MenuContainerWidget(QtWidgets.QWidget):

    pause = QtCore.pyqtSignal(int)
    threshold = QtCore.pyqtSignal(int)
    ambientLight = QtCore.pyqtSignal(int)
    backgroundLight = QtCore.pyqtSignal(int)
    quit = QtCore.pyqtSignal()

    @inject.params(config='config')
    def __init__(self, config=None):
        if config is None: return None
        super(MenuContainerWidget, self).__init__()
        self.setStyleSheet('QGroupBox { background-color: #ffffff; border: none; margin: 0px; }')
        
        layout = QtWidgets.QGridLayout()

        self.settings = MenuSettingsAction()
        self.settings.threshold.connect(self.onActionThreshold)
        self.settings.pause.connect(self.onActionPause)
        layout.addWidget(self.settings, 0, 0)

        self.sensors = MenuSensorsAction()
        layout.addWidget(self.sensors, 0, 1)

        self.backlight = MenuBacklightAction()
        layout.addWidget(self.backlight, 0, 2)
        
        self.sensors.ambientLight.connect(self.backlight.onActionAmbientLight)
        self.sensors.ambientLight.connect(lambda x: self.ambientLight.emit(x))
        self.sensors.ambientLight.connect(lambda x: self.backgroundLight.emit(x))

        self.setLayout(layout)

    def onActionClick(self, value):
        if value == self.Trigger:  # left click!
            self.menu.exec_(QtGui.QCursor.pos())

    @inject.params(config='config')
    def onActionPause(self, value=None, config=None):
        config.set('brightness.enabled', '{}'.format(int(value)))

    @inject.params(config='config')
    def onActionThreshold(self, value=None, config=None):
        config.set('brightness.threshold', '{}'.format(int(value)))

