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

from .thread import TimeIntervalThread


class Webcam(object):

    def __init__(self, source=None, width=160, height=120):

        self.source = source
        self.value = 0

        self.thread = TimeIntervalThread(self, width, height)
        self.thread.update.connect(self._update)
        self.thread.start()
        
    def _update(self, value):
        if value is None:
            return None
        self.value = value

    @property
    def code(self):
        return os.path.basename(self.source)

    @property
    def name(self):
        name = os.path.basename(self.source)
        return name.capitalize() 

    @property
    def brightness(self):
        return self.value

    @brightness.setter
    def brightness(self, percent):
        raise Exception('Can not change the ambient light')
