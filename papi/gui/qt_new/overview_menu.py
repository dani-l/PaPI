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
from papi.gui.qt_new.item import PaPITreeItem, PaPIRootItem, PaPItreeModel
from papi.gui.qt_new.item import DPluginTreeItem, DBlockTreeItem, DParameterTreeItem

__author__ = 'knuths'

from papi.ui.gui.qt_new.overview import Ui_Overview
from papi.gui.qt_new.create_plugin_dialog import CreatePluginDialog
from PySide.QtGui import QMainWindow, QStandardItem, QStandardItemModel, QMenu, QAbstractItemView, QAction
from papi.constants import PLUGIN_PCP_IDENTIFIER, PLUGIN_DPP_IDENTIFIER, PLUGIN_VIP_IDENTIFIER, PLUGIN_IOP_IDENTIFIER
from papi.constants import PLUGIN_ROOT_FOLDER_LIST
from PySide.QtCore import *
from papi.data.DPlugin import DPlugin, DBlock

from yapsy.PluginManager import PluginManager


class OverviewPluginMenu(QMainWindow, Ui_Overview):

    def __init__(self, gui_api, parent=None):
        super(OverviewPluginMenu, self).__init__(parent)
        self.setupUi(self)
        self.dgui = gui_api.gui_data

        self.gui_api = gui_api

        self.setWindowTitle("OverviewMenu")

        # ----------------------------------
        # Build structure of plugin tree
        # ----------------------------------

        self.model = PaPItreeModel()
        self.model.setHorizontalHeaderLabels(['Name'])

        self.pluginTree.setModel(self.model)
        self.pluginTree.setUniformRowHeights(True)

        self.visual_root = PaPIRootItem('ViP')
        self.io_root = PaPIRootItem('IOP')
        self.dpp_root = PaPIRootItem('DPP')
        self.pcp_root = PaPIRootItem('PCP')

        self.model.appendRow(self.visual_root)
        self.model.appendRow(self.io_root)
        self.model.appendRow(self.dpp_root)
        self.model.appendRow(self.pcp_root)

        # -----------------------------------
        # Build structure of parameter tree
        # -----------------------------------

        self.pModel = PaPItreeModel()
        self.pModel.setHorizontalHeaderLabels(['Name'])
        self.parameterTree.setModel(self.pModel)
        self.parameterTree.setUniformRowHeights(True)

        # -----------------------------------
        # Build structure of block tree
        # -----------------------------------

        self.bModel = PaPItreeModel()
        self.bModel.setHorizontalHeaderLabels(['Name'])
        self.blockTree.setModel(self.bModel)
        self.blockTree.setUniformRowHeights(True)

        # -----------------------------------
        # Build structure of subscriber tree
        # -----------------------------------

        self.subscriberModel = PaPItreeModel()
        self.subscriberModel.setHorizontalHeaderLabels(['Subscriber'])
        self.subscribersTree.setModel(self.subscriberModel)
        self.subscribersTree.setUniformRowHeights(True)

        # -----------------------------------
        # Build structure of subscriptions tree
        # -----------------------------------

        self.subscriptionModel = PaPItreeModel()
        self.subscriptionModel.setHorizontalHeaderLabels(['Subscription'])
        self.subscriptionsTree.setModel(self.subscriptionModel)
        self.subscriptionsTree.setUniformRowHeights(True)

        # -----------------------------------
        # signal/slots
        # -----------------------------------

        self.pluginTree.clicked.connect(self.pluginItemChanged)

        # ----------------------------------
        # Add context menu
        # ----------------------------------
        self.blockTree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.blockTree.customContextMenuRequested.connect(self.open_context_menu_block_tree)


    def setDGui(self, dgui):
        self.dgui = dgui

    def pluginItemChanged(self, index):
        dplugin = self.pluginTree.model().data(index, Qt.UserRole)

        if dplugin is None:
            return

        # ------------------------------------
        # Get all needed dplugin information
        # ------------------------------------

        self.unameEdit.setText(dplugin.uname)
        self.usedpluginEdit.setText(dplugin.plugin_identifier)
        self.stateEdit.setText(dplugin.state)
        self.typeEdit.setText(dplugin.type)
        self.alivestateEdit.setText(dplugin.alive_state)

        self.bModel.clear()
        self.pModel.clear()
        self.subscriberModel.clear()
        self.subscriptionModel.clear()

        self.bModel.setHorizontalHeaderLabels(['Name'])
        self.pModel.setHorizontalHeaderLabels(['Name'])
        self.subscriberModel.setHorizontalHeaderLabels(['Subscriber'])
        self.subscriptionModel.setHorizontalHeaderLabels(['Subscription'])

        # ---------------------------
        # Add DBlocks
        # ---------------------------

        dblock_ids = dplugin.get_dblocks()

        for dblock_id in dblock_ids:
            dblock = dblock_ids[dblock_id]

            block_item = DBlockTreeItem(dblock)
            self.bModel.appendRow(block_item)

            # -------------------------
            # Add Signals
            # -------------------------

            signal_names = dblock.get_signals()

            for signal_index in range(len(signal_names)):
                if signal_index != 0:
                    signal_name = signal_names[signal_index]
                    signal_item = PaPITreeItem(signal_index, signal_name)
                    block_item.appendRow(signal_item)

            # for signal_name in signal_names:
            #     signal_item = PaPITreeItem(signal_name, signal_name)
            #     signals_item.appendRow(signal_item)

            # -------------------------
            # Add Subscribers
            # -------------------------

            subscriber_ids = dblock.get_subscribers()

            for subscriber_id in subscriber_ids:
                subscriber = self.dgui.get_dplugin_by_id(subscriber_id)
                subscriber_item = DPluginTreeItem(subscriber)

                block_item = DBlockTreeItem(dblock)

                subscriber_item.appendRow(block_item)

                self.subscriberModel.appendRow(subscriber_item)




        # -------------------------
        # Add Subscriptions
        # -------------------------

        dplugin_sub_ids = dplugin.get_subscribtions()

        for dplugin_sub_id in dplugin_sub_ids:

            dblock_names = dplugin_sub_ids[dplugin_sub_id]
            dplugin_sub = self.gui_api.gui_data.get_dplugin_by_id(dplugin_sub_id)
            dplugin_sub_item = DPluginTreeItem(dplugin_sub)
            self.subscriptionModel.appendRow(dplugin_sub_item)

            for dblock_name in dblock_names:

                dblock_sub = dplugin_sub.get_dblock_by_name(dblock_name)
                dblock_sub_item = DBlockTreeItem(dblock_sub)
                dplugin_sub_item.appendRow(dblock_sub_item)

                subscription =  dblock_names[dblock_name]
                signals = subscription.get_signals()

                for signal in signals:

                    signal_item = QStandardItem(str(signal))
                    dblock_sub_item.appendRow(signal_item)


        # --------------------------
        # Add DParameters
        # --------------------------

        dparameter_names = dplugin.get_parameters()
        for dparameter_name in dparameter_names:
            dparameter = dparameter_names[dparameter_name]
            dparameter_item = DParameterTreeItem(dparameter)
            self.pModel.appendRow(dparameter_item)

            dparameter_item_value = PaPITreeItem(dparameter, str(dparameter.value))
            self.pModel.appendColumn([dparameter_item_value])
            self.parameterTree.resizeColumnToContents(0)
            self.parameterTree.resizeColumnToContents(1)


        self.blockTree.expandAll()
        self.parameterTree.expandAll()

        # http://srinikom.github.io/pyside-docs/PySide/QtGui/QAbstractItemView.html \
        # #PySide.QtGui.PySide.QtGui.QAbstractItemView.SelectionMode
        self.blockTree.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def show_create_plugin_dialog(self):
        index = self.pluginTree.currentIndex()
        item = self.pluginTree.model().data(index, Qt.UserRole)

        if item is not None:
            self.plugin_create_dialog.set_plugin(item)

            self.plugin_create_dialog.show()

    def open_context_menu_block_tree(self, position):
        '''

        :param position:
        :return:
        '''

        index = self.blockTree.indexAt(position)

        if index.isValid() is False:
            return None

        if self.pluginTree.isIndexHidden(index):
            return

        item = self.blockTree.model().data(index, Qt.UserRole)

        if isinstance(item, DPlugin) or isinstance(item, DBlock):
            return

        index_sel = self.pluginTree.currentIndex()
        dplugin_sel = self.pluginTree.model().data(index_sel, Qt.UserRole)

        if dplugin_sel is not None:

            sub_menu = QMenu('Add Subscription')
            dplugin_ids = self.dgui.get_all_plugins()

            for dplugin_id in dplugin_ids:
                dplugin = dplugin_ids[dplugin_id]

                if dplugin_sel.id != dplugin_id:
                    action = QAction(self.tr(dplugin.uname), self)
                    sub_menu.addAction(action)
                    dplugin_uname = dplugin.uname
                    action.triggered.connect(lambda: self.add_subscription_action(self.tr(dplugin_uname)))

            menu = QMenu()
            menu.addMenu(sub_menu)

            menu.exec_(self.blockTree.viewport().mapToGlobal(position))

    def open_context_menu_subscriber_tree(self, position):
        pass

    def open_context_menu_susbcription_tree(self, position):
        pass

    def open_context_menu_parameter_tree(self, position):
        pass

    def add_subscription_action(self, dplugin_uname):
        """

        :rtype :
        """

        subscriber_id = None
        source_id = None
        block_name = None
        signals = []

        dplugin = self.gui_api.gui_data.get_dplugin_by_uname(dplugin_uname)

        indexes = self.blockTree.selectedIndexes()

        print('Add Subscriotion for ' + dplugin.uname)
        print('There are ' + str(len(indexes)) + " signals to subscribe")
        for index in indexes:
            if index.isValid():

                signal_index = self.blockTree.model().data(index, Qt.UserRole)
                signals.append(signal_index)

        index_dblock = index.parent()

        dblock = self.blockTree.model().data(index_dblock, Qt.UserRole)

        index = self.pluginTree.currentIndex()

        dplugin_source = self.pluginTree.model().data(index, Qt.UserRole)

        self.gui_api.do_subscribe(dplugin.id, dplugin_source.id, dblock.name, signals)

    def showEvent(self, *args, **kwargs):
        dplugin_ids = self.dgui.get_all_plugins()

        #Add DPlugins in QTree

        for dplugin_id in dplugin_ids:
            dplugin = dplugin_ids[dplugin_id]

            # ------------------------------
            # Sort DPluginItem in TreeWidget
            # ------------------------------
            plugin_item = DPluginTreeItem(dplugin)

            if dplugin.type == PLUGIN_VIP_IDENTIFIER:
                self.visual_root.appendRow(plugin_item)
            if dplugin.type == PLUGIN_IOP_IDENTIFIER:
                 self.io_root.appendRow(plugin_item)
            if dplugin.type == PLUGIN_DPP_IDENTIFIER:
                self.dpp_root.appendRow(plugin_item)
            if dplugin.type == PLUGIN_PCP_IDENTIFIER:
                self.pcp_root.appendRow(plugin_item)

            # plugin_item.dplugin = dplugin
            # plugin_item.setText(self.get_column_by_name("PLUGIN"), str(dplugin.uname) )
            #
            # # -------------------------------
            # # Set amount of blocks and parameters as meta information
            # # -------------------------------
            # dparameter_names = dplugin.get_parameters()
            # dblock_ids = dplugin.get_dblocks()
            #
            # plugin_item.setText(self.get_column_by_name("#PARAMETERS"), str(len(dparameter_names.keys())))
            # plugin_item.setText(self.get_column_by_name("#BLOCKS"), str(len(dblock_ids.keys())))
