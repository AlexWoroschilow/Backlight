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
import functools

from PyQt5 import QtCore
from PyQt5 import QtWidgets


class RadioButtonGroup(QtWidgets.QWidget):

    change = QtCore.pyqtSignal(int)

    def __init__(self, values=[], selected=None):
        super(RadioButtonGroup, self).__init__()

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.setLayout(layout)

        self.collection = []
        for value in values:
            checkbox = QtWidgets.QRadioButton('Threshold {} %'.format(value))
            checkbox.setChecked(value == selected)
            action = functools.partial(self.onActionThresholdChange, threshold=value)
            checkbox.toggled.connect(action)
            layout.addWidget(checkbox)

    def onActionThresholdChange(self, event, threshold):
        self.change.emit(threshold)
