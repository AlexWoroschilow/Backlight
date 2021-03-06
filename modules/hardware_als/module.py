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
import glob
from lib.plugin import Loader

from .service import AmbientlightPool


class Loader(Loader):

    @property
    def enabled(self):
        return True

    @property
    def devices(self):
        return [x for x in glob.glob('{}/*'.format('/sys/bus/iio/devices'))]

    def config(self, binder):
        if not len(self.devices):
            return binder.bind('al-sensors', None)
        binder.bind('al-sensors', AmbientlightPool())
