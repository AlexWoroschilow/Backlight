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

import platform
from PyQt5 import QtGui

from lib.plugin import Loader


class Loader(Loader):

    @property
    def enabled(self):
        if platform.system() in ["Linux"]:
            return True
        return False

    def config(self, binder=None):
        binder.bind('icon', QtGui.QIcon("icons/icon.svg"))

    @inject.params(window='window', icon='icon')
    def boot(self, options=None, args=None, window=None, icon=None):
        if options is None or args is None: return None
        if window is None or icon is None: return None
        
        window.setWindowIcon(icon)
