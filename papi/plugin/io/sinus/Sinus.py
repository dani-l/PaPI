#!/usr/bin/python3
#-*- coding: utf-8 -*-

"""
Copyright (C) 2014 Technische Universität Berlin,
Fakultät IV - Elektrotechnik und Informatik,
Fachgebiet Regelungssysteme,
Einsteinufer 17, D-10587 Berlin, Germany

This file is part of PaPI.

PaPI is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PaPI is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with PaPI.  If not, see <http://www.gnu.org/licenses/>.

Contributors:
Stefan Ruppin
"""

from papi.plugin.plugin_base import plugin_base
from papi.data.DPlugin import DBlock
from papi.data.DParameter import DParameter

import time
import math
import numpy


class Sinus(plugin_base):

    def start_init(self):
        self.t = 0
        self.amax = 20
        self.f =0.1

        block1 = DBlock(None,1,10,'SinMit_f1',['t','f1_1'])
        block2 = DBlock(None,1,10,'SinMit_f2',['t','f2_1'])
        block3 = DBlock(None,1,10,'SinMit_f3',['t','f3_1','f3_2'])

        self.send_new_block_list([block1, block2, block3])

        self.para3 = DParameter(None,'Frequenz Block SinMit_f3',0.1,[0,1],1)
        self.para3.id = 1
        para_l = [self.para3]

        self.send_new_parameter_list(para_l)

        return True

    def pause(self):
        pass

    def resume(self):
        pass

    def execute_OLD(self):
        vec = numpy.zeros(self.amax*2)
        vec2 = numpy.zeros(self.amax*2)
        vec3 = numpy.zeros(self.amax*2)
        for i in range(self.amax):
            vec[i] = self.t
            vec[i+self.amax] = math.sin(2*math.pi*0.01*self.t)
            vec2[i] = self.t
            vec2[i+self.amax] = math.sin(2*math.pi*0.15*self.t)
            vec3[i] = self.t
            vec3[i+self.amax] = math.sin(2*math.pi*self.para3.value*self.t)
            self.t += 0.1

        self.send_new_data(vec,'SinMit_f1')
        self.send_new_data(vec2,'SinMit_f2')
        self.send_new_data(vec3,'SinMit_f3')
        time.sleep(0.02)

    def execute(self):
        vec = numpy.zeros( (2,self.amax))
        vec2 = numpy.zeros((2,self.amax))
        vec3 = numpy.zeros((3,self.amax))
        for i in range(self.amax):
            vec[0, i] = self.t
            vec[1, i] = math.sin(2*math.pi*0.01*self.t)
            vec2[0, i] = self.t
            vec2[1, i] = math.sin(2*math.pi*0.15*self.t)
            vec3[0, i] = self.t
            vec3[1, i] = math.sin(2*math.pi*self.para3.value*self.t)
            vec3[2, i] = math.sin(2*math.pi*0.01*self.t)
            self.t += 0.1

        self.send_new_data(vec,'SinMit_f1')
        self.send_new_data(vec2,'SinMit_f2')
        self.send_new_data(vec3,'SinMit_f3')
        time.sleep(0.02)

    def set_parameter(self, parameter_list):
        for p in parameter_list:
            if p.name == self.para3.name:
                self.para3 = p

    def quit(self):
        print('Sinus: will quit')

    def get_type(self):
        return 'IOP'
