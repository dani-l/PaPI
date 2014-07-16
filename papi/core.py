#!/usr/bin/python3
# -*- coding: latin-1 -*-

"""
Copyright (C) 2014 Technische Universitšt Berlin,
Fakultšt IV - Elektrotechnik und Informatik,
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

Contributors
Sven Knuth
"""

version = '0.1'

from yapsy.PluginManager import PluginManager
from multiprocessing import Process, Array, Lock, Queue
import time
import os


class Core:

    def run(self):


        print("initialize PaPI - Plugin based Process Interaction")
        print("Core process id: ",os.getpid())

        coreEventQueue = Queue()

        guiEventQueue = Queue()

        # sollte weg, wenn Datenstruktur da
        process_alive_cout = 0


        # GUIAlive
        guiAlive = 0




        coreGoOn = 1
        while coreGoOn:
            event = coreEventQueue.get()
            self.__process_event__(event)
            coreGoOn = process_alive_cout == 0 & guiAlive






    def __process_event__(self,event):
        pass








