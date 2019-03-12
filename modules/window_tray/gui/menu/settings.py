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

from .widget.threshold import ThresholdWidget


class MenuSettingsAction(QtWidgets.QWidget):

    pause = QtCore.pyqtSignal(int)
    threshold = QtCore.pyqtSignal(int)

    @inject.params(config='config')
    def __init__(self, config=None):
        if config is None: return None
        super(MenuSettingsAction, self).__init__()
        
        layout = QtWidgets.QVBoxLayout()

        self.thresholds = ThresholdWidget()
        self.thresholds.change.connect(lambda x: self.threshold.emit(x))
        layout.addWidget(self.thresholds)

        self.toggle = QtWidgets.QCheckBox('Enabled')
        self.toggle.setChecked(int(config.get('brightness.enabled')))
        self.toggle.stateChanged.connect(self.pause.emit)
        layout.addWidget(self.toggle)
        
        self.setLayout(layout)
        
