#!/usr/bin/python3
# -*- coding: utf-8 -*-

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
Sven Knuth
"""

from PySide.QtCore import *
from PySide.QtGui import *

from papi.ui.gui.qt_new.CreateRecording import Ui_CreateRecording
from PySide.QtGui import QMainWindow
from papi.gui.qt_new.custom import CustomField

from papi.gui.qt_new.item import CustomFieldModel, CustomFieldItem, CustomFieldDelegate, \
    StructTreeModel, StructTreeNode

class CreateRecordingConfig(QMainWindow, Ui_CreateRecording):
    def __init__(self, gui_api, dgui):
        super(CreateRecordingConfig, self).__init__()
        self.setupUi(self)
        self.gui_api = gui_api
        self.dgui = dgui

        # -----------------------------------------
        # Initiate first tab: Fields
        # -----------------------------------------

        self.addFieldButton.clicked.connect(self.add_button_triggered)
        self.previewButton.clicked.connect(self.preview_button_triggered)

        self.field_model = CustomFieldModel()
        self.field_model.dataChanged.connect(self.custom_field_edited)
        self.field_model.setHorizontalHeaderLabels(['Field', 'Size', 'Remove'])

        self.customFieldTable.setModel(self.field_model)
        self.customFieldTable.clicked.connect(self.custom_field_table_clicked)
        #self.customFieldTable.itemDelegateForColumn(2, CustomFieldDelegate())

        self.customFieldTable.setItemDelegate(CustomFieldDelegate())
#        self.customFieldTable.setItemDelegateForColumn(2, CustomFieldDelegate())
        # -------------------------------------------

        self.struct_model = StructTreeModel()
        self.structureView.setModel(self.struct_model)
        self.struct_model.setHorizontalHeaderLabels(['Name', 'Size'])
        self.root_struct = StructTreeNode(CustomField('Data', size=''), 0)

        self.struct_model.appendRow(self.root_struct)

        # -----------------------------------------
        # Initiate second tab: Subscription
        # -----------------------------------------

        self.previewButton_sub.clicked.connect(self.preview_sub_button_triggered)

        self.struct_model_sub = StructTreeModel()
        self.struct_model_sub.setHorizontalHeaderLabels(['Name', 'Size'])
        self.structureView_sub.setModel(self.struct_model_sub)

        self.root_struct_sub = StructTreeNode(CustomField('Data', size=''), 0)

        self.root_struct_sub = StructTreeNode(CustomField(), 0)

        self.struct_model_sub.appendRow(self.root_struct_sub)

        self.structureView_sub.expandAll()
        self.structureView_sub.resizeColumnToContents(0)
        self.structureView_sub.resizeColumnToContents(1)

        self.structureView_sub.clicked.connect(self.structureView_sub_item_changed)


        # ---------------------------------------------

        self.selectionGrid.setAlignment(Qt.AlignTop)

    def showEvent(self, *args, **kwargs):
        pass

    def add_button_triggered(self):
        custom_field_item = CustomFieldItem(CustomField())

        self.field_model.appendRow(custom_field_item)
        self.customFieldTable.resizeColumnsToContents()

        for i in range(self.struct_model.rowCount()):
            index = self.struct_model.index(i, 2)
            #print(index)
            button = QPushButton('Remove')
            #self.customFieldTable.setIndexWidget(index, button)

    def preview_button_triggered(self):

        self.struct_model.clear()
        self.struct_model.setHorizontalHeaderLabels(['Name', 'Size'])

        self.root_struct = StructTreeNode(CustomField('Data', size=''), 0)
        self.struct_model.appendRow(self.root_struct)

        for i in range(self.field_model.rowCount()):
            field = self.field_model.item(i).object

            self.root_struct.appendRow(field)

        self.structureView.expandAll()
        self.structureView.resizeColumnToContents(0)
        self.structureView.resizeColumnToContents(1)

    def preview_sub_button_triggered(self):

        self.struct_model_sub.clear()
        self.struct_model_sub.setHorizontalHeaderLabels(['Name', 'Size'])

        self.root_struct_sub = StructTreeNode(CustomField('Data', size=''), 0)
        self.struct_model_sub.appendRow(self.root_struct_sub)

        for i in range(self.field_model.rowCount()):
            field = self.field_model.item(i).object
            self.root_struct_sub.appendRow(field)

        self.structureView_sub.expandAll()
        self.structureView_sub.resizeColumnToContents(0)
        self.structureView_sub.resizeColumnToContents(1)

    def custom_field_table_clicked(self, index):

        if index.isValid() is False:
            return None

        col = index.column()

        if col == 2:
            self.field_model.removeRow(index.row())

        #self.customFieldTable.

    def custom_field_edited(self, index, none):
        print('Edited !!')

    def structureView_sub_item_changed(self, index):
        if index.isValid() is False:
            return None

        item = self.structureView_sub.model().data(index, Qt.UserRole)

        if item is None:
            return


        self.selectionGrid.addWidget(QLabel('Plugin'), 0, 0)
        self.selectionGrid.addWidget(QLabel('Block' ), 0, 1)
        self.selectionGrid.addWidget(QLabel('Signal'), 0, 2)

        for i in range(1, int(item.size)+1):
            boxPlugins = QComboBox()
            boxBlocks = QComboBox()
            boxSignals = QComboBox()

            boxPlugins.currentIndexChanged.connect( self.selection_changed_plugin)
            boxBlocks.currentIndexChanged.connect(self.selection_changed_block)

            self.selectionGrid.addWidget(boxPlugins, i, 0)
            self.selectionGrid.addWidget(boxBlocks, i, 1)
            self.selectionGrid.addWidget(boxSignals, i, 2)


            dplugin_ids = self.dgui.get_all_plugins()
            for dplugin_id in dplugin_ids:
                dplugin = dplugin_ids[dplugin_id]
                boxPlugins.addItem(dplugin.uname)

    def selection_changed_plugin(self, index):
        print(index)

    def selection_changed_block(self, index):
        print(index)