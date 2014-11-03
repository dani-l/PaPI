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
Sven Knuth, Stefan Ruppin
"""

__author__ = 'knuths'

import sys
import time
import os

from PySide.QtGui               import QMainWindow, QApplication, QFileDialog
from PySide.QtGui               import QIcon
from PySide.QtCore              import QSize, Qt

from papi.ui.gui.qt_new.main           import Ui_QtNewMain
from papi.data.DGui             import DGui
from papi.ConsoleLog            import ConsoleLog

from papi.constants import GUI_PAPI_WINDOW_TITLE, GUI_WOKRING_INTERVAL, GUI_PROCESS_CONSOLE_IDENTIFIER, \
    GUI_PROCESS_CONSOLE_LOG_LEVEL, GUI_START_CONSOLE_MESSAGE, GUI_WAIT_TILL_RELOAD

from papi.constants import CONFIG_DEFAULT_FILE

from papi.gui.gui_api import Gui_api
from papi.gui.gui_event_processing import GuiEventProcessing
import pyqtgraph as pg
from pyqtgraph import QtCore

from papi.gui.qt_new.create_plugin_menu import CreatePluginMenu
from papi.gui.qt_new.overview_menu import OverviewPluginMenu

from threading import Thread

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=False)


class GUI(QMainWindow, Ui_QtNewMain):

    def __init__(self, core_queue, gui_queue,gui_id, gui_data = None, parent=None):
        super(GUI, self).__init__(parent)
        self.setupUi(self)

        if gui_data is None:
            self.gui_data = DGui()
        else:
            self.gui_data = gui_data

        self.gui_api = Gui_api(self.gui_data, core_queue, gui_id)

        self.gui_event_processing = GuiEventProcessing(self.gui_data, core_queue, gui_id, gui_queue)

        self.gui_event_processing.added_dplugin.connect(self.add_dplugin)
        self.gui_event_processing.removed_dplugin.connect(self.remove_dplugin)
        self.gui_event_processing.dgui_changed.connect(self.changed_dgui)
        self.setWindowTitle(GUI_PAPI_WINDOW_TITLE)

        self.core_queue = core_queue
        self.gui_queue = gui_queue

        self.gui_id = gui_id

        self.count = 0

        self.log = ConsoleLog(GUI_PROCESS_CONSOLE_LOG_LEVEL, GUI_PROCESS_CONSOLE_IDENTIFIER)

        self.log.printText(1,GUI_START_CONSOLE_MESSAGE + ' .. Process id: '+str(os.getpid()))

        self.last_config = None

        # -------------------------------------
        # Create placeholder
        # -------------------------------------
        self.overview_menu = None
        self.create_plugin_menu = None
        # -------------------------------------
        # Create callback functions for buttons
        # -------------------------------------
        self.loadButton.clicked.connect(self.load_triggered)
        self.saveButton.clicked.connect(self.save_triggered)

        # self.buttonCreatePlugin.clicked.connect(self.create_plugin)
        # self.buttonCreateSubscription.clicked.connect(self.create_subscription)
        # self.buttonCreatePCPSubscription.clicked.connect(self.create_pcp_subscription)
        # self.buttonShowOverview.clicked.connect(self.ap_overview)
        # self.buttonExit.clicked.connect(self.close)

        # -------------------------------------
        # Create actions
        # -------------------------------------

        self.actionLoad.triggered.connect(self.load_triggered)
        self.actionSave.triggered.connect(self.save_triggered)

        self.actionOverview.triggered.connect(self.show_overview_menu)
        self.actionCreate.triggered.connect(self.show_create_plugin_menu)

        self.actionResetPaPI.triggered.connect(self.reset_papi)
        self.actionReloadConfig.triggered.connect(self.reload_config)
        # -------------------------------------
        # Create Icons for buttons
        # -------------------------------------

        load_icon = QIcon.fromTheme("document-open")
        save_icon = QIcon.fromTheme("document-save")

        # addplugin_icon = QIcon.fromTheme("list-add")
        # close_icon = QIcon.fromTheme("application-exit")
        # overview_icon = QIcon.fromTheme("view-fullscreen")
        # addsubscription_icon = QIcon.fromTheme("list-add")

        # -------------------------------------
        # Set Icons for buttons
        # -------------------------------------

        self.loadButton.setIconSize(QSize(30, 30))
        self.loadButton.setIcon(load_icon)

        self.saveButton.setIconSize(QSize(30, 30))
        self.saveButton.setIcon(save_icon)

        # self.buttonCreatePlugin.setIconSize(QSize(30, 30))
        # self.buttonCreatePlugin.setIcon(addplugin_icon)
        #
        # self.buttonExit.setIcon(close_icon)
        # self.buttonExit.setIconSize(QSize(30, 30))
        #
        # self.buttonShowOverview.setIcon(overview_icon)
        # self.buttonShowOverview.setIconSize(QSize(30, 30))
        #
        # self.buttonCreateSubscription.setIcon(addsubscription_icon)
        # self.buttonCreateSubscription.setIconSize(QSize(30, 30))
        #
        # self.buttonCreatePCPSubscription.setIcon(addsubscription_icon)
        # self.buttonCreatePCPSubscription.setIconSize(QSize(30, 30))

        # -------------------------------------
        # Set Tooltipps for buttons
        # -------------------------------------

        # self.buttonExit.setToolTip("Exit PaPI")
        # self.buttonCreatePlugin.setToolTip("Add New Plugin")
        # self.buttonCreateSubscription.setToolTip("Create New Subscription")
        # self.buttonCreatePCPSubscription.setToolTip("Create New PCP Subscription")
        #
        # self.buttonShowOverview.setToolTip("Show Overview")

        # -------------------------------------
        # Set TextName to ''
        # -------------------------------------

        # self.buttonExit.setText('')
        # self.buttonCreatePlugin.setText('')
        # self.buttonCreateSubscription.setText('')
        # self.buttonShowLicence.setText('')
        # self.buttonShowOverview.setText('')

    def run(self):
        # create a timer and set interval for processing events with working loop
        QtCore.QTimer.singleShot(GUI_WOKRING_INTERVAL, lambda: self.gui_event_processing.gui_working(self.closeEvent))


    def dbg(self):
        print("Action")

    def menu_license(self):
        pass

    def menu_quit(self):
        pass

    def show_create_plugin_menu(self):
        self.create_plugin_menu = CreatePluginMenu(self.gui_api)

        self.create_plugin_menu.show()
        # self.create_plugin_menu.raise_()
        # self.create_plugin_menu.activateWindow()

        # del self.create_plugin_menu
        #
        # self.create_plugin_menu = None

    def show_overview_menu(self):
        self.overview_menu = OverviewPluginMenu(self.gui_api)
        self.overview_menu.show()

    def load_triggered(self):

        fileName = QFileDialog.getOpenFileName(self,
            self.tr("PaPI-Cfg"), CONFIG_DEFAULT_FILE, self.tr("PaPI-Cfg (*.xml)"))

        if fileName[0] != '':
            self.last_config = fileName[0]
            self.gui_api.do_load_xml(fileName[0])

    def save_triggered(self):

        fileName = QFileDialog.getSaveFileName(self,
            self.tr("PaPI-Cfg"), CONFIG_DEFAULT_FILE , self.tr("PaPI-Cfg (*.xml)"))

        if fileName[0] != '':
            self.gui_api.do_save_xml_config(fileName[0])

    def closeEvent(self, *args, **kwargs):
        self.gui_api.do_close_program()
        if self.create_plugin_menu is not None:
            self.create_plugin_menu.close()

        if self.overview_menu is not None:
            self.overview_menu.close()

        self.close()

    def add_dplugin(self, dplugin):
        sub_window = dplugin.plugin.get_sub_window()
        self.widgetArea.addSubWindow(sub_window)
        sub_window.show()
        # see http://qt-project.org/doc/qt-4.8/qt.html#WindowType-enum

        sub_window.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowMinMaxButtonsHint | Qt.WindowTitleHint )

    def remove_dplugin(self, dplugin):
        self.widgetArea.removeSubWindow(dplugin.plugin.get_sub_window())

    def changed_dgui(self):
        if self.overview_menu is not None:
            self.overview_menu.refresh_action()

    def reload_config(self):
        """
        This function is used to reset PaPI and to reload the last loaded configuration file.
        :return:
        """
        if self.last_config is not None:
            self.reset_papi()
            QtCore.QTimer.singleShot(GUI_WAIT_TILL_RELOAD, lambda: self.gui_api.do_load_xml(self.last_config))

    def reset_papi(self):
        """
        This function is called to reset PaPI. That means all subscriptions were canceled and all plugins were removed.
        :return:
        """
        self.gui_api.do_reset_papi()

def startGUI(CoreQueue, GUIQueue,gui_id):
    """
    Function to call to start gui operation
    :param CoreQueue: link to queue of core
    :type CoreQueue: Queue
    :param GUIQueue: queue where gui receives messages
    :type GUIQueue: Queue
    :param gui_id: id of gui for events
    :type gui_id: int
    :return:
    """
    app = QApplication(sys.argv)
    gui = GUI(CoreQueue, GUIQueue,gui_id)
    gui.run()
    gui.show()
    app.exec_()

def startGUI_TESTMOCK(CoreQueue, GUIQueue,gui_id, data_mock):
    """
    Function to call to start gui operation
    :param CoreQueue: link to queue of core
    :type CoreQueue: Queue
    :param GUIQueue: queue where gui receives messages
    :type GUIQueue: Queue
    :param gui_id: id of gui for events
    :type gui_id: int
    :return:
    """
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)

    gui = GUI(CoreQueue, GUIQueue,gui_id, data_mock)

    gui.run()
    gui.show()
    app.exec_()

if __name__ == '__main__':
    # main of GUI, just for stand alone gui testing
    app = QApplication(sys.argv)
    frame = GUI(None,None,None)
    frame.show()
    app.exec_()
