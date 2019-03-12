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

from .menu.container import MenuContainerWidget


class TrayWidget(QtWidgets.QSystemTrayIcon):
    
    pause = QtCore.pyqtSignal(int)
    threshold = QtCore.pyqtSignal(int)
    backgroundLight = QtCore.pyqtSignal(int)
    ambientLight = QtCore.pyqtSignal(int)
    quit = QtCore.pyqtSignal()
    
    def __init__(self, icon, app=None):
        QtWidgets.QApplication.__init__(self, icon, app)
        self.activated.connect(self.onActionClick)
        self.setToolTip('Ambient light brightness')

        self.menu = QtWidgets.QMenu()

        self.container = MenuContainerWidget()
        self.container.pause.connect(self.pause.emit)
        self.container.threshold.connect(self.threshold.emit)
        self.container.backgroundLight.connect(self.backgroundLight.emit)
        self.container.ambientLight.connect(self.ambientLight.emit)
        self.container.quit.connect(self.quit.emit)

        settings = QtWidgets.QWidgetAction(self)
        settings.setDefaultWidget(self.container)
        self.menu.addAction(settings)
        
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

