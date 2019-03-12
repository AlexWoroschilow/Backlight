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
# WITHOUT WARRANTIES OR CONDITION
import inject


class SensorPool(object):

    @property
    @inject.params(config='config', alsensors='al-sensors', webcameras='webcameras', backlight='backlight')
    def devices(self, config=None, alsensors=None, webcameras=None, backlight=None):
        if alsensors is None or webcameras is None or backlight is None: return
        
        enabled = False 
        
        for index, device in enumerate(backlight.devices, start=0):
            enabled = int(index == 0) if enabled is None else enabled  
            if not config.has('backlights.{}'.format(device.code)):
                config.set('backlights.{}'.format(device.code), enabled)
        
        for index, device in enumerate(alsensors.devices, start=0):
            enabled = int(index == 0) if enabled is None else enabled  
            if not config.has('sensors.{}'.format(device.code)):
                config.set('sensors.{}'.format(device.code), enabled)
            yield device
            
        for index, device in enumerate(webcameras.devices, start=0):
            enabled = int(index == 0) if enabled is None else enabled  
            if not config.has('sensors.{}'.format(device.code)):
                config.set('sensors.{}'.format(device.code), enabled)
            yield device
