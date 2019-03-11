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

from PyQt5 import QtCore
from PyQt5 import QtWidgets


class ThresholdWidget(QtWidgets.QWidget):

    change = QtCore.pyqtSignal(int)

    @inject.params(config='config')
    def __init__(self, config):
        super(ThresholdWidget, self).__init__()

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.setLayout(layout)

        for value in [0, 5, 10, 15, 20]:
            checkbox = QtWidgets.QRadioButton('Threshold {} %'.format(value))
            checkbox.setChecked(value == int(config.get('brightness.threshold')))
            action = functools.partial(self.onActionThreshold, threshold=value) 
            checkbox.toggled.connect(action)
            layout.addWidget(checkbox)

    def onActionThreshold(self, event, threshold):
        self.change.emit(threshold)     

