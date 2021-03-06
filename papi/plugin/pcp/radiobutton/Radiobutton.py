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

You should have received a copy of the GNU General Public License
along with PaPI.  If not, see <http://www.gnu.org/licenses/>.

Contributors
Sven Knuth
"""





from PyQt5.QtWidgets import QSlider,QVBoxLayout, QWidget, QLabel, QRadioButton
from PyQt5 import QtCore

from papi.data.DPlugin import DEvent
from papi.data.DParameter import DParameter
from papi.plugin.base_classes.vip_base import vip_base
import papi.constants as pc

class Radiobutton(vip_base):
    def cb_initialize_plugin(self):

        self.event_choice = DEvent('Choice')

        self.pl_send_new_event_list([self.event_choice])

        self.config = self.pl_get_current_config_ref()
        para_list = []

        self.para_texts    = DParameter('texts', default=self.config['option_texts']['value'])
        self.para_values   = DParameter('values', default=self.config['option_values']['value'])

        para_list.append(self.para_texts)
        para_list.append(self.para_values)

        self.pl_send_new_parameter_list(para_list)

        self.central_widget = QWidget()

        self.option_texts = []
        self.option_values = []
        self.pre_selected_index = None

        if isinstance(self.config['selected_index']['value'], str):
            if self.config['selected_index']['value'] != '':
                self.pre_selected_index = int(self.config['selected_index']['value'])

        self.pl_set_widget_for_internal_usage(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.buttons = []

        self.set_option_texts(self.config['option_texts']['value'])
        self.set_option_values(self.config['option_values']['value'])

        self.update_widget()

        return True

    def set_option_values(self, values):

        if isinstance(values, str):
            self.option_values = str.split(values, ',')

            for i in range(len(self.option_values)):
                self.option_values[i] = self.option_values[i].lstrip().rstrip()

    def set_option_texts(self, texts):

        if isinstance(texts, str):
            self.option_texts = str.split(texts, ',')

            for i in range(len(self.option_texts)):
                self.option_texts[i] = self.option_texts[i].lstrip().rstrip()

    def update_widget(self):

        for button in self.buttons:
            self.layout.removeWidget(button)
            button.deleteLater()

        self.buttons = []

        for i in range(len(self.option_texts)):
            button = QRadioButton(self.option_texts[i])

            button.released.connect(self.button_released)

            if i == self.pre_selected_index:
                button.setChecked(True)

            self.buttons.append(button)
            self.layout.addWidget(button)

        self.central_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.central_widget.customContextMenuRequested.connect(self.show_context_menu)

        return self.central_widget

    def show_context_menu(self, pos):
        gloPos = self.central_widget.mapToGlobal(pos)
        self.cmenu = self.pl_create_control_context_menu()
        self.cmenu.exec_(gloPos)

    def button_released(self):
        for i in range(len(self.buttons)):
            if self.buttons[i].isChecked():
                self.config['selected_index']['value'] = str(i)
                if len(self.option_values) == len(self.option_texts):
                    self.pl_emit_event(self.option_values[i], self.event_choice)
                else:
                    self.pl_emit_event(self.option_texts[i], self.event_choice)

    def cb_set_parameter(self, parameter_name, parameter_value):


        if parameter_name == self.para_texts.name:
            self.config['option_texts']['value'] = parameter_value
            self.set_option_texts(parameter_value)
            self.update_widget()

        if parameter_name == self.para_values.name:
            self.config['option_values']['value'] = parameter_value
            self.set_option_values(parameter_value)


    def cb_plugin_meta_updated(self):
        pass

    def cb_get_plugin_configuration(self):
        config = {
            'option_texts': {
                'display_text' : 'Displayed Option',
                'value': 'Option Text 1, Option Text 2, Option Text 3',
                'tooltip': 'This text is seen by the user. Must be separated by commas.'
            },
            'option_values': {
                'display_text' : 'Value per Option',
                'value': '',
                'tooltip': 'It is possible to set a value for every option. '
                           'The corresponding value is send instead of the displayed text. '
            },
            'selected_index': {
                'display_text' : 'Preselected Option',
                'value' : '',
                'regex' : pc.REGEX_SINGLE_INT,
                'tooltip': 'Preselect an option by its index.',
                'advanced' : '1'
            },
            'name': {
                'display_text' : 'Plugin Name',
                'value': 'RadioButton Label',
                'tooltip': 'Used for window title'
            }}
        return config

    def cb_quit(self):
        pass

    def cb_new_parameter_info(self, dparameter_object):
        if isinstance(dparameter_object, DParameter):
            value = dparameter_object.default
            if str(value) in self.option_values:
                self.pre_selected_index = self.option_values.index(str(value))
                self.update_widget()