#!/usr/bin/python3
#-*- coding: utf-8 -*-

"""
Copyright (C) 2014 Technische Universität Berlin,
Fakultät IV - Elektrotechnik und Informatik,
Fachgebiet Regelungssysteme,
Einsteinufer 17, D-10587 Berlin, Germany
 
This file is part of PaPI.
 
PaPI is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
 
PaPI is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
 
You should have received a copy of the GNU Lesser General Public License
along with PaPI.  If not, see <http://www.gnu.org/licenses/>.
 
Contributors:
Stefan Ruppin
Sven Knuth
"""

from papi.plugin.base_classes.base_visual import base_visual

from papi.constants import PLUGIN_PCP_IDENTIFIER


class pcp_base(base_visual):

    def initiate_layer_1(self, config):
        return self.initiate_layer_0(config)

    def initiate_layer_0(self, config):
        raise NotImplementedError("Please Implement this method")

    def get_type(self):
        return PLUGIN_PCP_IDENTIFIER

    def new_parameter_info(self, dparameter_object):
        raise NotImplementedError("Please Implement this method")