#!/usr/bin/python3
# -*- coding: utf-8 -*-

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
<Stefan Ruppin
"""

__author__ = 'Stefan'

from papi.plugin.base_classes.vip_base import vip_base
from papi.gui.qt_new.custom import FileLineEdit

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QWizard, QWizardPage, QLabel, QLineEdit, QVBoxLayout

import threading, time


class OrtdController(vip_base):

    def initiate_layer_0(self, config=None):

        # ---------------------------
        # Read configuration
        # ---------------------------
        self.ortd_uname = config['ORTD_Plugin_uname']['value']
        # --------------------------------
        # Create Widget
        # --------------------------------
        # Create Widget needed for this plugin
        self.ControllerWidget = QWizard()
        self.ControllerWidget.setOption(QWizard.NoCancelButton)
        self.ControllerWidget.setOption(QWizard.NoBackButtonOnLastPage)
        self.ControllerWidget.setOption(QWizard.NoBackButtonOnStartPage)
        self.ControllerWidget.setOption(QWizard.DisabledBackButtonOnLastPage)
        self.set_widget_for_internal_usage( self.ControllerWidget )
        self.ControllerWidget.addPage(ControllerOrtdStart(api=self.control_api, uname=self.dplugin_info.uname,ortd_uname=self.ortd_uname, config = self.config))
        self.ControllerWidget.addPage(ControllerWorking(api=self.control_api, uname=self.dplugin_info.uname))


        self.lock = threading.Lock()

        self.plugin_started_list = []

        self.event_list = []
        self.thread_alive = False

        return True

    def pause(self):
        # will be called, when plugin gets paused
        # can be used to get plugin in a defined state before pause
        # e.a. close communication ports, files etc.
        pass

    def resume(self):
        # will be called when plugin gets resumed
        # can be used to wake up the plugin from defined pause state
        # e.a. reopen communication ports, files etc.
        pass

    def execute(self, Data=None, block_name = None, plugin_uname = None):
        # Do main work here!
        # If this plugin is an IOP plugin, then there will be no Data parameter because it wont get data
        # If this plugin is a DPP, then it will get Data with data

        # param: Data is a Data hash and block_name is the block_name of Data origin
        # Data is a hash, so use ist like:  Data['t'] = [t1, t2, ...] where 't' is a signal_name
        # hash signal_name: value

        # Data could have multiple types stored in it e.a. Data['d1'] = int, Data['d2'] = []
        self.thread1 = threading.Thread(target=self.execute_cfg)

        self.event_list.append(Data)
        if self.thread_alive is False:
            self.thread1.start()



    def execute_cfg(self):
        while len(self.event_list) > 0:
            Data = self.event_list.pop(0)
            ############################
            #      Reset Signal        #
            ############################
            if 'ControlSignalReset' in Data:
                val = Data['ControlSignalReset']
                if val == 1:
                   while len(self.plugin_started_list):
                        pl_uname = self.plugin_started_list.pop()
                        self.control_api.do_delete_plugin_uname(pl_uname)
                time.sleep(0.5)

            ############################
            #       Create Plugins     #
            ############################
            if 'ControlSignalCreate' in Data:
                cfg = Data['ControlSignalCreate']
                if cfg is not None:
                    for pl_uname in cfg:
                        if pl_uname not in self.plugin_started_list:
                            pl_cfg = cfg[pl_uname]
                            self.control_api.do_create_plugin(pl_cfg['identifier']['value'],pl_uname, pl_cfg['config'])
                            self.plugin_started_list.append(pl_uname)


            ############################
            #       Create Subs        #
            ############################
            if 'ControlSignalSub' in Data:
                cfg = Data['ControlSignalSub']
                if cfg is not None:
                    for pl_uname in cfg:
                        pl_cfg = cfg[pl_uname]
                        sig = []
                        if 'signals' in pl_cfg:
                            sig = pl_cfg['signals']
                        self.control_api.do_subscribe_uname(pl_uname,self.ortd_uname, pl_cfg['block'], signals=sig, sub_alias= None)

            ############################
            #    Set parameter links   #
            ############################
            if 'ControllerSignalParameter' in Data:
                cfg = Data['ControllerSignalParameter']
                if cfg is not None:
                    for pl_uname in cfg:
                        pl_cfg = cfg[pl_uname]
                        para = None
                        if 'parameter' in pl_cfg:
                            para = pl_cfg['parameter']
                        self.control_api.do_subscribe_uname(self.ortd_uname,pl_uname, pl_cfg['block'], signals=[], sub_alias= para)

            ############################
            #    Close plugin          #
            ############################
            if 'ControllerSignalClose' in Data:
                cfg = Data['ControllerSignalClose']
                if cfg is not None:
                    for pl_uname in cfg:
                        if pl_uname in self.plugin_started_list:
                            self.control_api.do_delete_plugin_uname(pl_uname)
                            self.plugin_started_list.remove(pl_uname)


            # wait before set active tab
            time.sleep(1.0)
            if 'ActiveTab' in Data:
                cfg = Data['ActiveTab']
                if cfg is not None:
                    tabName = cfg
                    self.control_api.do_set_tab_active_by_name(tabName)

        self.thread_alive = False

    def set_parameter(self, name, value):
        # attetion: value is a string and need to be processed !
        # if name == 'irgendeinParameter':
        #   do that .... with value
        pass

    def quit(self):
        # do something before plugin will close, e.a. close connections ...
        pass

    def get_plugin_configuration(self):
        #
        # Implement a own part of the config
        # config is a hash of hass object
        # config_parameter_name : {}
        # config[config_parameter_name]['value']  NEEDS TO BE IMPLEMENTED
        # configs can be marked as advanced for create dialog
        # http://utilitymill.com/utility/Regex_For_Range
        config = {
            "ORTD_Plugin_uname": {
                'value': 'ORTDPlugin1',
                'display_text': 'Uname to use for ortd plugin instance',
                'advanced': "0"
            },
            'name': {
                'value': 'ORTDController'
            },
            '1:address': {
                'value': '127.0.0.1',
                'advanced': '1'
            },
            '2:source_port': {
                'value': '20000',
                'advanced': '1'
            },
            '3:out_port': {
                'value': '20001',
                'advanced': '1'
            },
            'size': {
                'value': "(150,300)",
                'regex': '\(([0-9]+),([0-9]+)\)',
                'advanced': '1',
                'tooltip': 'Determine size: (height,width)'
            },
        }
        return config

    def plugin_meta_updated(self):
        """
        Whenever the meta information is updated this function is called (if implemented).

        :return:
        """

        #dplugin_info = self.dplugin_info
        pass




class ControllerOrtdStart(QWizardPage):
    def __init__(self,api = None, uname= None, parent = None, ortd_uname = None, config = None):
        QWizardPage.__init__(self, parent)
        self.config = config
        self.api = api
        self.ortd_uname = ortd_uname
        self.uname = uname
        label = QLabel("Press 'Next' to start ORTD interaction")
        label.setWordWrap(True)
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

    def validatePage(self):

        IP =  self.config ['1:address']['value']
        out_port = self.config ['2:source_port']['value']
        in_port  = self.config ['3:out_port']['value']

        ortd_cfg ={
            'address': {
                'value': IP,
                'advanced': '1'
            },
            'source_port': {
                'value': out_port,
                'advanced': '1'
            },
            'out_port': {
                'value': in_port,
                'advanced': '1'
            }
        }


        self.api.do_create_plugin('ORTD_UDP', self.ortd_uname, ortd_cfg, True)

        self.thread = threading.Thread(target=self.subscribe_control_signal)
        self.thread.start()

        return True

    def subscribe_control_signal(self):

        self.api.do_subscribe_uname(self.uname,self.ortd_uname, 'ControllerSignals', signals=['ControlSignalReset',
                                                                                              'ControlSignalCreate',
                                                                                              'ControlSignalSub',
                                                                                              'ControllerSignalParameter',
                                                                                              'ControllerSignalClose',
                                                                                              'ActiveTab'])
        self.api.do_set_parameter_uname(self.ortd_uname, 'triggerConfiguration', '1')


class ControllerWorking(QWizardPage):
    def __init__(self,api = None, uname= None, parent = None):
        QWizardPage.__init__(self, parent)
        self. api = api

        self.setTitle("ORTD Controller")
        label = QLabel("Controller plugin is working")
        label.setWordWrap(True)

        label2 = QLabel("")

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(label2)

        self.setLayout(layout)

    def validatePage(self):
        return False
