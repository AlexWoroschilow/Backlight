#!/usr/bin/python3
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
import os
import sys

abspath = os.path.abspath(__file__)
os.chdir(os.path.dirname(abspath))

root = os.path.dirname(abspath)
sys.path.append('{}/lib'.format(root))

import inject
import optparse
import logging

from PyQt5 import QtWidgets

from lib.kernel  import Kernel


class Application(QtWidgets.QApplication):
    kernel = None

    def __init__(self, options=None, args=None):
        super(Application, self).__init__(sys.argv)
        self.setApplicationName('Backlight adjuster')
        self.kernel = Kernel(self, options, args)
        self.kernel.aplication = self

    @inject.params(widget='window.tray')
    def exec_(self, widget=None):
        if widget is not None and widget.quit:
            widget.quit.connect(self.exit)
        return super(Application, self).exec_()


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("--loglevel", default=logging.DEBUG, dest="loglevel", help="Logging level")
    parser.add_option("--logfile", default=os.path.expanduser('~/.config/brightness/brightness.log'), dest="logfile", help="Logfile location")
    parser.add_option("--config", default=os.path.expanduser('~/.config/brightness/brightness.conf'), dest="config", help="Config file location")
    
    (options, args) = parser.parse_args()

    log_format = '[%(relativeCreated)d][%(name)s] %(levelname)s - %(message)s'
    logging.basicConfig(level=options.loglevel, format=log_format)

    application = Application(options, args)
    sys.exit(application.exec_())
