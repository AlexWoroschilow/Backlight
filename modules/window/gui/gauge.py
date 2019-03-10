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
from PyQt5 import QtQuick


class Gauge(QtWidgets.QWidget):

    def __init__(self):
        super(Gauge, self).__init__()
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.chart = QtQuick.QQuickView()
        self.chart.setSource(QtCore.QUrl('icons/gauge.qml'))
        self.chart.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)

        container = QtWidgets.QWidget.createWindowContainer(self.chart, self);
        container.setMinimumHeight(150);
        
        layout.addWidget(container)

    def value(self, percent=None):
        gauge = self.chart.findChild(QtCore.QObject, 'test_gauge')
        gauge.setProperty('gauge_value', percent)
