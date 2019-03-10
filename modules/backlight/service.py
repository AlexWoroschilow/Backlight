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
import logging


class Backlight(object):

    def __init__(self, path=None):
        self.path = path

    def _get(self, path=None):
        try:
            if not os.path.exists(path): return None
            if not os.path.isfile(path): return None
            with open(path, 'r', errors='ignore') as stream:
                return stream.read().strip("\n")
        except (OSError, IOError) as ex:
            logger = logging.getLogger('backlight')
            logger.error(ex)
            return None
        return None

    def _set(self, path=None, value=None):
        try:
            if not os.path.exists(path): return None
            if not os.path.isfile(path): return None
            with open(path, 'w', errors='ignore') as stream:
                stream.write('{:>.0f}'.format(value))
                stream.close()
                return True
        except (OSError, IOError) as ex:
            logger = logging.getLogger('backlight')
            logger.error(ex)
            return False
        return False

    @property
    def code(self):
        return os.path.basename(self.path) 

    @property
    def name(self):
        return self.code\
            .replace('_', ' ')\
            .capitalize() 

    @property
    def max(self):
        for source in glob.glob('%s/max_brightness' % self.path):
            if not os.path.exists(source): return None
            if not os.path.isfile(source): return None
            return int(self._get(source))
        return None
    
    @property
    def actual(self):
        for source in glob.glob('%s/actual_brightness' % self.path):
            if not os.path.exists(source): return None
            if not os.path.isfile(source): return None
            return int(self._get(source))
        return None

    @property
    def brightness(self):
        return self.actual / self.max * 100

    @brightness.setter
    def brightness(self, percent):
        for source in glob.glob('{}/brightness'.format(self.path)):
            if not os.path.exists(source): return False
            if not os.path.isfile(source): return None
            return self._set(source, percent / 100 * self.max)
        return False


class BacklightPool(object):

    @property
    def devices(self):
        for device in glob.glob('{}/*'.format('/sys/class/backlight')):
            if not os.path.exists(device): continue
            if not os.path.isdir(device): return None
            yield Backlight(device)

    @property
    def device(self):
        for device in self.devices:
            if device is None: continue
            if device.code in ['gmux_backlight']:
                return device
        for device in self.devices:
            if device is None: continue
            return device

    @property
    def name(self):
        if self.device is None: return None
        return self.device.name

    @property
    def brightness(self):
        if self.device is None: return None
        return self.device.brightness

    @brightness.setter
    def brightness(self, percent):
        for device in self.devices:
            if device is None: continue
            device.brightness = percent


if __name__ == "__main__":
    pool = BacklightPool()
    for index, device in enumerate(pool.devices):
        device.brightness = 30
        print(device.name, device.brightness)
    print(pool.name, pool.brightness)
