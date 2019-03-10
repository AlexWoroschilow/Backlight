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

from .button import SensorsRadioButton
from .widget import ThresholdsWidget
from .gauge import Gauge


class MenuSettingsAction(QtWidgets.QWidgetAction):

    pause = QtCore.pyqtSignal(int)
    threshold = QtCore.pyqtSignal(int)

    @inject.params(config='config')
    def __init__(self, parent, config):
        super(MenuSettingsAction, self).__init__(parent)
        
        layout = QtWidgets.QVBoxLayout()

        self.thresholds = ThresholdsWidget()
        self.thresholds.change.connect(lambda x: self.threshold.emit(x))
        layout.addWidget(self.thresholds)

        self.toggle = QtWidgets.QCheckBox('Enabled')
        self.toggle.setChecked(int(config.get('brightness.enabled')))
        self.toggle.stateChanged.connect(lambda x: self.pause.emit(x))
        layout.addWidget(self.toggle)
        
        container = QtWidgets.QWidget()
        container.setContentsMargins(0, 0, 0, 0)
        container.setMinimumWidth(190)
        container.setLayout(layout)
        
        self.setDefaultWidget(container)


class MenuSensorsAction(QtWidgets.QWidgetAction):

    sensor = QtCore.pyqtSignal(bool, object)
    ambientLight = QtCore.pyqtSignal(int)
    backlight = QtCore.pyqtSignal(int)

    @inject.params(config='config', sensors='sensors')
    def __init__(self, parent, config, sensors):
        super(MenuSensorsAction, self).__init__(parent)
        
        layout = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel('Sensors')
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.gauge = Gauge()
        layout.addWidget(self.gauge)

        for device in sensors.devices:
            if device is None: continue
            checkbox = SensorsRadioButton(device)
            checkbox.setChecked(int(config.get('sensors.{}'.format(device.code))))
            checkbox.ambientLight.connect(lambda x: self.ambientLight.emit(x))
            checkbox.ambientLight.connect(lambda x: self.backlight.emit(x))
            checkbox.ambientLight.connect(self.gauge.value)
            layout.addWidget(checkbox)

        container = QtWidgets.QWidget()
        container.setContentsMargins(0, 0, 0, 0)
        container.setStyleSheet('QWidget { background-color: #ffffff }')
        container.setLayout(layout)
        
        self.setDefaultWidget(container)


class MenuBacklightAction(QtWidgets.QWidgetAction):

    def __init__(self, parent=None):
        if parent is None: return None
        super(MenuBacklightAction, self).__init__(parent)
        
        layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel('Backlight')
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.gauge = Gauge()
        layout.addWidget(self.gauge)

        container = QtWidgets.QWidget()
        container.setContentsMargins(0, 0, 0, 0)
        container.setStyleSheet('QWidget { background-color: #ffffff }')
        container.setLayout(layout)
        
        self.setDefaultWidget(container)

    def onActionPause(self, value):
        self.pause = value

    @inject.params(backlights='backlight')
    def onActionAmbientLight(self, value=None, backlights=None):
        if value is None: return None
        self.gauge.value(value)
        if backlights is None: return None
        for device in backlights.devices:
            if device is None: continue
            if value is not None and value < 5:
                device.brightness = 5
            if value is not None and value >= 5:
                device.brightness = value

