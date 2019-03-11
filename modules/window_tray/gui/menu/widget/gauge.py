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
import os
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtQuick


class Gauge(QtWidgets.QWidget):

    def __init__(self, min_width=None, min_height=100):
        super(Gauge, self).__init__()
        if min_height is not None: self.setMinimumHeight(min_height)
        if min_width is not None: self.setMinimumWidth(min_width)
        
        
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.chart = QtQuick.QQuickView()
        self.chart.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)
        
        source = '{}/gauge.qml'.format(os.path.dirname(__file__))
        if not os.path.exists(source): return None
        if not os.path.isfile(source): return None

        self.chart.setSource(QtCore.QUrl(source))
        
        container = QtWidgets.QWidget.createWindowContainer(self.chart, self)
        layout.addWidget(container)

    def value(self, percent=None):
        gauge = self.chart.findChild(QtCore.QObject, 'test_gauge')
        gauge.setProperty('gauge_value', percent)
