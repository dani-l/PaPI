#!/usr/bin/python3
#-*- coding: latin-1 -*-

"""
Copyright (C) 2014 Technische Universitšt Berlin,
Fakultšt IV - Elektrotechnik und Informatik,
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
 
You should have received a copy of the GNU General Public License
along with PaPI.  If not, see <http://www.gnu.org/licenses/>.
 
Contributors:
Sven Knuth
"""

__author__ = 'Sven Knuth'

from papi.event.data.DataBase import DataBase


class EditDPluginByUname(DataBase):
    def __init__(self, oID, plugin_uname, eObject, changeRequest):
        super().__init__(oID, None, 'edit_dplugin_by_uname', None)
        #Object of DPlugin, which should be changed
        self.editedObject = eObject
        #Kind of action. e.g. {'edit': DSignal}
        self.changeRequest = changeRequest

        self.plugin_uname = plugin_uname
