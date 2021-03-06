#!/usr/bin/python3
#-*- coding: latin-1 -*-

"""

"""

from papi.plugin.base_classes.iop_base import iop_base

from papi.data.DPlugin import DBlock
from papi.data.DParameter import DParameter
from papi.data.DSignal import DSignal

import numpy
import time



class CPU_Load(iop_base):
    INTERVAL = 0.1
    def cb_initialize_plugin(self):
        self.t = 0
        self.delta_t = 0.01

        self.para_delta_t = self.pl_create_DParameter('Delta_t', default_value=0.01)

        self.pl_send_new_parameter_list([self.para_delta_t])

        block1 = self.pl_create_DBlock('CPUload')
        signal = self.pl_create_DSignal('load_in_percent')

        block1.add_signal(signal)

        self.pl_send_new_block_list([block1])
        return True

    def cb_pause(self):
        pass


    def cb_resume(self):
        pass

    def cb_execute(self, Data=None, block_name = None, plugin_uname = None):
        vec = numpy.zeros((2,1))

        vec[0,0] = self.t*10
        vec[1,0] = self.getCpuLoad() * 100

        self.t += self.delta_t

        self.pl_send_new_data('CPUload', [vec[0, 0]], {'load_in_percent': vec[1]})

        time.sleep(self.delta_t)

    def cb_set_parameter(self, name, value):
        pass


    def cb_quit(self):
        print('CPU Load: will quit')


    def getTimeList(self):
        """
        Fetches a list of time units the cpu has spent in various modes
        Detailed explanation at http://www.linuxhowtos.org/System/procstat.htm
        """
        cpuStats = open("/proc/stat", "r").readline()
        columns = cpuStats.replace("cpu", "").split(" ")
        return map(int, filter(None, columns))

    def deltaTime(self, interval):
        """
        Returns the difference of the cpu statistics returned by getTimeList
        that occurred in the given time delta
        """
        timeList1 = self.getTimeList()
        time.sleep(interval)
        timeList2 = self.getTimeList()
        return [(t2-t1) for t1, t2 in zip(timeList1, timeList2)]

    def getCpuLoad(self):
        """
        Returns the cpu load as a value from the interval [0.0, 1.0]
        """
        dt = list(self.deltaTime(self.INTERVAL))
        idle_time = float(dt[3])
        total_time = sum(dt)
        load = 1-(idle_time/total_time)
        return load

    def cb_plugin_meta_updated(self):
        pass

    def cb_get_plugin_configuration(self):
        return {}