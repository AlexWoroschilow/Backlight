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
from PyQt5.QtCore import Qt 

from .label import BacklightLabel
from .button import SensorsRadioButton

from .widget import ThresholdsWidget


class MenuSettingsAction(QtWidgets.QWidgetAction):

    pause = QtCore.pyqtSignal(int)
    threshold = QtCore.pyqtSignal(int)

    @inject.params(config='config')
    def __init__(self, parent, config):
        super(MenuSettingsAction, self).__init__(parent)
        
        layout = QtWidgets.QVBoxLayout()

        self.toggle = QtWidgets.QCheckBox('Enabled')
        self.toggle.setChecked(int(config.get('brightness.enabled')))
        self.toggle.stateChanged.connect(lambda x: self.pause.emit(x))
        layout.addWidget(self.toggle)

        self.thresholds = ThresholdsWidget()
        self.thresholds.change.connect(lambda x: self.threshold.emit(x))
        layout.addWidget(self.thresholds)
        
        container = QtWidgets.QWidget()
        container.setContentsMargins(0, 0, 0, 0)
        container.setMinimumWidth(190)
        container.setLayout(layout)
        
        self.setDefaultWidget(container)


class MenuSensorsAction(QtWidgets.QWidgetAction):

    sensor = QtCore.pyqtSignal(bool, object)
    ambientLight = QtCore.pyqtSignal(int)

    @inject.params(config='config', sensors='sensors')
    def __init__(self, parent, config, sensors):
        super(MenuSensorsAction, self).__init__(parent)
        
        layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel('Sensors')
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        for device in sensors.devices:
            checkbox = SensorsRadioButton(device)
            checkbox.setChecked(int(config.get('sensors.{}'.format(device.code))))
            checkbox.ambientLight.connect(lambda x: self.ambientLight.emit(x))
            layout.addWidget(checkbox)

        container = QtWidgets.QWidget()
        container.setContentsMargins(0, 0, 0, 0)
        container.setLayout(layout)
        
        self.setDefaultWidget(container)


class MenuBacklightAction(QtWidgets.QWidgetAction):

    @inject.params(backlights='backlight')
    def __init__(self, parent, backlights):
        super(MenuBacklightAction, self).__init__(parent)
        
        layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel('Backlight')
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        for device in backlights.devices:
            layout.addWidget(BacklightLabel(device))

        container = QtWidgets.QWidget()
        container.setContentsMargins(0, 0, 0, 0)
        container.setLayout(layout)
        
        self.setDefaultWidget(container)

    def onActionPause(self, value):
        self.pause = value

    @inject.params(backlights='backlight')
    def onActionAmbientLight(self, value, backlights):
        for device in backlights.devices:
            if value is not None and value < 5:
                device.brightness = 5
            if value is not None and value >= 5:
                device.brightness = value

