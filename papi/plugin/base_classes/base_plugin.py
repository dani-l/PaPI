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

from papi.data.DPlugin import DBlock, DEvent
from papi.data.DParameter import DParameter
from papi.data.DOptionalData import DOptionalData
from papi.yapsy.IPlugin import IPlugin
from papi.constants import CORE_TIME_SIGNAL
import papi.event as Event
import papi.exceptions as pe

class base_plugin(IPlugin):
    """
    This class is used as basis class for all other plugin bases

    """

    def __init__(self):
        super(base_plugin, self).__init__()
        self.__id__ = -1
        self._dplugin_info = None
        self.__subscription_for_demux = None

    def _papi_init(self, ):
        """
        Used to initialized this class in the context of PaPI

        :return:
        """
        self._dplugin_info       = None
        self.__subscription_for_demux = None

    def _get_type(self):
        """
        Returns the type of the plugin. Must be implemented !

        :return:
        """
        raise NotImplementedError("Please Implement this method")

    def cb_execute(self, Data=None, block_name = None, plugin_uname = None):
        """
        Called by the PaPI framework when new date can be processed.  Must be implemented !

        :param Data: Contains a hash with an array for every key.
        :param block_name: Block of the plugin to which the signal belongs
        :param plugin_uname: Plugin which sent this data.
        :return:
        """
        raise NotImplementedError("Please Implement this method")

    def get_configuration_base(self):
        """
        Returns the base configuration. Must be implemented !

        :return:
        """
        raise NotImplementedError("Please Implement this method")

    def get_startup_configuration(self):
        """
        Creates the startup configuration which is created by merging the configuration provided by the plugin base
        and the plugin configuration.

        :return:
        """
        return self._merge_configs(self.get_configuration_base(), self.cb_get_plugin_configuration())

    def cb_get_plugin_configuration(self):
        """
        Returns the plugin specific configuration. Must be implemented !

        :return:
        """
        raise NotImplementedError("Please Implement this method")

    # some control callback functions
    # ----------------------
    def cb_pause(self):
        """
        Called when the plugin should pause. Must be implemented !

        :return:
        """
        raise NotImplementedError("Please Implement this method")

    def cb_resume(self):
        """
        Called when the plugin should resume. Must be implemented !

        :return:
        """
        raise NotImplementedError("Please Implement this method")

    def cb_quit(self):
        """
        Called when the plugin should quit. Must be implemented !

        :return:
        """
        raise NotImplementedError("Please Implement this method")

    def cb_set_parameter(self, parameter_name, parameter_value):
        """
        Called when a parameter was changed.
        This function is called with the parameter name and its current value. Must be implemented !

        :param parameter_name: Name of parameter
        :param parameter_value: New value of the parameter
        :return:
        """
        raise NotImplementedError("Please Implement this method")

    def _set_parameter_internal(self, name, value):
        """
        Internal function used to set parameters.

        :param name:
        :param value:
        :return:
        """
        self.cb_set_parameter(name, value)


    # some api functions
    # ------------------
    def _merge_configs(self, cfg1, cfg2):
        """
        This function is used to merge two configurations.

        :param cfg1:
        :param cfg2:
        :return:
        """
        return dict(list(cfg1.items()) + list(cfg2.items()) )

    def pl_emit_event(self, data, event):
        """
        This function is used by plugins to emit a specific event.

        :param data: New value provided by the DEvent
        :param event: DEvent which should be emitted.
        :return:
        """
        if isinstance(event, DEvent) == False and isinstance(event, str) == False:
            raise pe.WrongType("block",  [DEvent, str])

        self.pl_send_parameter_change(data, event)

    def pl_send_parameter_change(self, data, block):
        """
        Internal function, should be not directly used anymore.

        :param data:
        :param block:
        :return:
        """
        opt = DOptionalData(DATA=data)
        opt.data_source_id = self.__id__
        opt.is_parameter = True

        if isinstance(block, DBlock) is False and isinstance(block, str) is False:
            raise pe.WrongType("block",  [DBlock, str])

        if isinstance(block, DBlock):
            opt.block_name = block.name

        if isinstance(block, str):
            opt.block_name = block

        event = Event.data.NewData(self.__id__, 0, opt, None)
        self._Core_event_queue__.put(event)

    def pl_send_new_data(self, block_name, time_line, data):
        """
        This function is called by plugins to send new data for a single block.

        :param block_name: Name of the block
        :param time_line: A time vector
        :param data: Data containing the values in a hash array of signal names as key.
        :return:
        """

        dataHash = data
        dataHash[CORE_TIME_SIGNAL] = time_line
        opt = DOptionalData(DATA = dataHash)
        opt.data_source_id = self.__id__
        opt.block_name = block_name

        event = Event.data.NewData(self.__id__, 0, opt, None)
        self._Core_event_queue__.put(event)

    def pl_send_new_event_list(self, events):
        """
        Used to inform the PaPI framework about all DEvents provided by this plugins.

        :param events: List of DEvents
        :return:
        """

        if not isinstance(events, list):
            raise pe.WrongType("events", list)

        if len(events) == 0:
            raise pe.WrongLength("events", len(events), ">0")

        for i in range(len(events)):
            event = events[i]
            if not isinstance(event, DEvent):
                raise pe.WrongType('events['+str(i)+']', DEvent)

        self.pl_send_new_block_list(events)

    def pl_send_new_block_list(self, blocks):
        """
        Used to inform the PaPI framework about all DBlocks provided by this plugins.

        :param blocks: List of DBlocks
        :return:
        """

        if not isinstance(blocks, list):
            raise pe.WrongType("blocks", list)

        if len(blocks) == 0:
            raise pe.WrongLength("blocks", len(blocks), ">0")

        for i in range(len(blocks)):
            block = blocks[i]
            if not isinstance(block, DBlock):
                raise pe.WrongType('blocks['+str(i)+']', DBlock)

        opt = DOptionalData()
        opt.block_list = blocks
        event = Event.data.NewBlock(self.__id__, 0, opt)
        self._Core_event_queue__.put(event)

    def send_new_parameter_list(self, parameters):
        """
        Used to inform the PaPI framework about all DParameters provided by this plugins.

        :param parameters: List of DParameters
        :return:
        """

        if not isinstance(parameters, list):
            raise pe.WrongType("parameters", list)

        if len(parameters) == 0:
            raise pe.WrongLength("parameters", len(parameters), ">0")

        for i in range(len(parameters)):
            parameter = parameters[i]
            if not isinstance(parameter, DParameter):
                raise pe.WrongType('parameters['+str(i)+']', DParameter)

        opt = DOptionalData()
        opt.parameter_list = parameters

        event = Event.data.NewParameter(self.__id__, 0, opt)
        self._Core_event_queue__.put(event)

    def send_delete_block(self, block):
        """
        Used to inform the PaPI framework that a single DBlock was deleted.

        :param block: Block which should be deleted.
        :return:
        """
        block_name = None

        if isinstance(block, DBlock) == False and isinstance(block, str) == False:
            raise pe.WrongType("parameters", [DBlock, str])

        if isinstance(block, DBlock):
            block_name = block.name

        if isinstance(block, str):
            block_name = block

        event = Event.data.DeleteBlock(self.__id__, 0, block_name)
        self._Core_event_queue__.put(event)

    def send_delete_parameter(self, parameter):
        """
        Used to inform the PaPI framework that a single DParameter was deleted.

        :param parameter: DParameter which should be deleted.
        :return:
        """

        parameter_name = None

        if isinstance(parameter, DParameter) == False and isinstance(parameter, str) == False:
            raise pe.WrongType("parameter", [DParameter, str])

        if isinstance(parameter, DParameter):
            parameter_name = parameter.name

        if isinstance(parameter, str):
            parameter_name = parameter

        event = Event.data.DeleteParameter(self.__id__, 0, parameter_name)
        self._Core_event_queue__.put(event)

    def update_plugin_meta(self, dplug):
        """
        Function which is used to update all meta information which are known by the PaPI framework.

        :param dplug: DPlugin object containg all known information
        :return:
        """

        self._dplugin_info = dplug
        self.__subscription_for_demux = self._dplugin_info.get_subscribtions()
        self.cb_plugin_meta_updated()

    def cb_plugin_meta_updated(self):
        """
        Function which is called when ever the meta information were updated.

        :return:
        """
        raise NotImplementedError("Please Implement this method")

    def demux(self, source_id, block_name, data):
        """
        Internal function which is called to demux all signals.
        This function will make sure that only the subscribed signals will be transferred to the plugin.

        :param source_id:
        :param block_name:
        :param data:
        :return:
        """
        if self.__subscription_for_demux is None:
           self.__subscription_for_demux = self._dplugin_info.get_subscribtions()

        sub_object = self.__subscription_for_demux[source_id][block_name]
        sub_signals = sub_object.signals

        return dict([(i, data[i]) for i in sub_signals if i in data])


    def pl_get_dplugin_info(self):
        return self._dplugin_info