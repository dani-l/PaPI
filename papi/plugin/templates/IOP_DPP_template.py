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
<Stefan Ruppin
"""

__author__ = 'control'

from papi.plugin.plugin_base import plugin_base
from papi.data.DPlugin import DBlock
from papi.data.DParameter import DParameter


class IOP_DPP_template(plugin_base):

    def start_init(self, config=None):
        # do user init
        # define vars, connect to rtai .....

        # create a block object
        #   block1 = DBlockself.__id__.,signal count,frequnce,'Blockname',['Signalname1','Signalname2'])

        # send block list
        #   self.send_new_block_list([block1, block2, block3])

        # create a parameter object
        #   self.para = DParameter('type','ParameterName',InitWert,RangeArray,1)

        # build parameter list to send to Core
        #   para_list = [self.para]
        #   self.send_new_parameter_list(para_list)

        # if wanted, change event mode to True, False, 'default'
        # self.set_event_trigger_mode()

        # use startup config like this:
        # default_config = self.get_startup_configuration()
        # self.config = None
        # if config is None:
        #     self.config = default_config
        # else:
        #     self.config = dict(list(default_config.items()) + list(config.items()))
        #
        # self.sample = self.config['sampleinterval']['value']


        # return init success, important
        return True

    def pause(self):
        pass

    def resume(self):
        pass

    def execute(self, Data=None, block_name = None):
        # param: Data is a Data hash send to this  Plugin and block_name is the block_name of Data origin
        # Data is a hash, so use ist like:  Data['t'] = [t1, t2, ...]
        # implement execute and send new data
        #   self.send_new_data(data_vec,'block_name')
        # data_vec has to be a numpy array and used like this
        # data_vec[0] = [t1, t2, ...]      data_vec[0] has to be the time line!
        # data_vec[1] = data....

        pass


    def set_parameter(self, name, value):
        # if name == 'irgendeinParameter':
        #   do that .... with value
        pass

    def quit(self):
        # do something before plugin will close, e.a. close connections ...
        pass

    def get_type(self):
        # return type: IOP or DPP
        return 'IOP'

    def get_startup_configuration(self):
        config = {
            "sampleinterval": {
                'value': 1,
                'regex': '[0-9]+'
        }, 'timewindow': {
                'value': "1000",
                'regex': '[0-9]+'
        }, 'size': {
                'value': "(200,200)",
                'regex': '\(([0-9]+),([0-9]+)\)'
        }, 'name': 'Plot_Plugin', 'label_y': {
                'value': "amplitude, V",
                'regex': '\w+,\s+\w+'
        }, 'label_x': {
                'value': "time, s",
                'regex': '\w+,\s*\w+'
        }}
        return config

    # def hook_update_plugin_meta(self):
    #     """
    #     Whenever the meta information is updated this function is called (if implemented).
    #     :return:
    #     """
    #     dplugin_info = self.dplugin_info