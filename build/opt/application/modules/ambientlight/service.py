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


class Backlight(object):

    def __init__(self, path=None):
        self.path = path

    def _get(self, path=None):
        try:
            if not path or not os.path.isfile(path):
                return None
            with open(path, 'r', errors='ignore') as stream:
                return stream.read().strip("\n")
        except (OSError, IOError) as ex:
            return None
        return None

    def _set(self, path=None, value=None):
        try:
            if not path or not os.path.isfile(path):
                return None
            with open(path, 'w', errors='ignore') as stream:
                stream.write(value)
                stream.close()
        except (OSError, IOError) as ex:
            return None
        return None

    @property
    def code(self):
        for source in glob.glob('%s/name' % self.path):
            return self._get(source)
        return None

    @property
    def name(self):
        return self.code\
            .replace('-', ' ')\
            .capitalize() 

    @property
    def max(self):
        return 4095
    
    @property
    def actual(self):
        for source in glob.glob('%s/in_illuminance_input' % self.path):
            return int(self._get(source))
        return None

    @property
    def brightness(self):
        return self.actual / self.max * 100

    @brightness.setter
    def brightness(self, percent):
        raise Exception('Can not change the ambient light')


class AmbientlightPool(object):
    path = '/sys/bus/iio/devices'

    @property
    def devices(self):
        for device in glob.glob('{}/*'.format(self.path)):
            yield Backlight(device)


class AmbientlightManager(object):
    
    pool = AmbientlightPool()
    
    @property
    def brightness(self):
        pass

    @brightness.setter
    def brightness(self, percent):
        pass


if __name__ == "__main__":
    pool = AmbientlightPool()
    for index, device in enumerate(pool.devices):
        print(device.name, device.brightness)
            
