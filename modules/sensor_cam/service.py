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
import os
import glob
import time
import math
import logging

import pygame.camera

from .webcam.device import Webcam 


class WebcamPool(object):

    @property
    def devices(self):
        pygame.camera.init()
        for device in pygame.camera.list_cameras():
            yield Webcam(device)


if __name__ == "__main__":
    pool = WebcamPool()
    for index, device in enumerate(pool.devices):
        print(device.name, device.brightness)
            
