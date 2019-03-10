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
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtQuick

from .gauge import Gauge


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, icon=None):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Ambient light brightness')
        self.setContentsMargins(0, 0, 0, 0)
        self.setMinimumHeight(150)
        
        if icon is None: return None
        self.setWindowIcon(icon)
        
        self.layout = QtWidgets.QVBoxLayout()
        
        self.ambient_light = Gauge()
        self.layout.addWidget(QtWidgets.QLabel('Ambient light'))
        self.layout.addWidget(self.ambient_light)
        
        self.background_light = Gauge()   
        self.layout.addWidget(QtWidgets.QLabel('Backlight'))
        self.layout.addWidget(self.background_light)        

#         title = QtWidgets.QLabel('Ambient light')
#         self.layout.addWidget(title, 0, 0, 1, 10)        
#         
#         icon = QtWidgets.QLabel(self)
#         pixmap = QtGui.QPixmap('icons/ambient-light.svg')
#         icon.setPixmap(pixmap.scaled(40, 40, QtCore.Qt.KeepAspectRatio))
#         self.layout.addWidget(icon, 1, 0)        
#         
#         self.ambientLight = QtWidgets.QLabel(' - %')
#         self.layout.addWidget(self.ambientLight, 1, 1)        
# 
#         title = QtWidgets.QLabel('Backlight')
#         self.layout.addWidget(title, 2, 0, 1, 10)        
# 
#         icon = QtWidgets.QLabel(self)
#         pixmap = QtGui.QPixmap('icons/backlight.svg')
#         icon.setPixmap(pixmap.scaled(40, 40, QtCore.Qt.KeepAspectRatio))
#         self.layout.addWidget(icon, 3, 0)        
# 
#         self.backlight = QtWidgets.QLabel(' - %')
#         self.layout.addWidget(self.backlight, 3, 1)        
# 
#         self.layout.addWidget(Gauge(), 4, 0)        
#         
        container = QtWidgets.QWidget()
        container.setLayout(self.layout)
        
        self.setCentralWidget(container)
        
    def setAmbientLight(self, percent=None):
        if percent is None: return None
        self.ambient_light.value(percent)

    def setBacklight(self, percent=None):
        if percent is None: return None
        self.background_light.value(percent)

