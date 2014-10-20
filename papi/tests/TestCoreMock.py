__author__ = 'stefan'

import unittest
from threading import Thread
import time

from papi.data.DGui import DGui
from papi.core import Core
from papi.gui.qt_dev.gui_main import startGUI_TESTMOCK
from papi.gui.gui_api import Gui_api
from papi.PapiEvent import PapiEvent
from threading import Thread
from multiprocessing import Queue
import papi.constants as const

import time


class dummyProcess(object):
    def __init__(self):
        self.pid = 10
    def join(self):
        pass


class TestCoreMock(unittest.TestCase):

    DELAY_TIME = 0.3

    def test_create_plugin_sub(self):
        # create a Plot and Sinus plugin
        self.gui_api.do_create_plugin('Plot','Plot1')
        self.gui_api.do_create_plugin('Sinus','Sin1')


        time.sleep(TestCoreMock.DELAY_TIME)
        #
        self.assertIsNotNone(self.core_data.get_dplugin_by_uname('Plot1'))
        self.assertIsNotNone(self.gui_data.get_dplugin_by_uname('Plot1'))
        self.assertIsNotNone(self.core_data.get_dplugin_by_uname('Sin1'))
        self.assertIsNotNone(self.gui_data.get_dplugin_by_uname('Sin1'))

        self.gui_api.do_subscribe_uname('Plot1','Sin1','SinMit_f3',[1])

        time.sleep(TestCoreMock.DELAY_TIME)

        subs = self.gui_data.get_dplugin_by_uname('Plot1').get_subscribtions()
        for id in subs:
            dsub = self.gui_data.get_dplugin_by_id(id)
            self.assertEqual('Sin1',dsub.uname)

    def test_do_create_api(self):


        self.gui_api.do_create_plugin('Plot','Plot1')
        self.gui_api.do_create_plugin('Sinus','Sin1')


        time.sleep(TestCoreMock.DELAY_TIME)
        #
        self.assertIsNotNone(self.core_data.get_dplugin_by_uname('Plot1'))
        self.assertIsNotNone(self.gui_data.get_dplugin_by_uname('Plot1'))
        self.assertIsNotNone(self.core_data.get_dplugin_by_uname('Sin1'))
        self.assertIsNotNone(self.gui_data.get_dplugin_by_uname('Sin1'))

        self.assertEqual(self.core_data.get_dplugins_count(), 2, 'Core PL Count not 2')
        self.assertEqual(self.gui_data.get_dplugins_count(), 2, 'Gui PL Count not 2')

        self.assertIsNone(self.core_data.get_dplugin_by_uname('Sinus'))
        self.assertIsNone(self.gui_data.get_dplugin_by_uname('Sinus'))

    def test_delete_plugin_no_VIP_PCP(self):
        PL_1_NAME = 'Sin1'
        PL_1_IDENT = 'Sinus'
        self.gui_api.do_create_plugin(PL_1_IDENT,PL_1_NAME)

        time.sleep(TestCoreMock.DELAY_TIME)

        self.assertIsNotNone(self.core_data.get_dplugin_by_uname(PL_1_NAME), 'No Plugin in CoreData with uname '+PL_1_NAME)
        self.assertIsNotNone(self.gui_data.get_dplugin_by_uname(PL_1_NAME), 'No Plugin in GuiData with uname '+PL_1_NAME)
        self.assertEqual(self.core_data.get_dplugins_count(), 1, 'Core PL Count not 1')
        self.assertEqual(self.gui_data.get_dplugins_count(), 1, 'Gui PL Count not 1')

        self.gui_api.do_delete_plugin_uname(PL_1_NAME)

        time.sleep(TestCoreMock.DELAY_TIME)

        self.assertIsNone(self.core_data.get_dplugin_by_uname(PL_1_NAME), 'Plugin still in core_data')
        self.assertIsNone(self.gui_data.get_dplugin_by_uname(PL_1_NAME), 'Plugin still in gui_data')
        self.assertEqual(self.core_data.get_dplugins_count(), 0, 'Core PL Count not 0')
        self.assertEqual(self.gui_data.get_dplugins_count(), 0, 'Gui PL Count not 0')

    def test_delete_plugin_is_VIP_PCP(self):
        PL_1_NAME = 'Plot1'
        PL_1_IDENT = 'Plot'
        self.gui_api.do_create_plugin(PL_1_IDENT,PL_1_NAME)

        time.sleep(TestCoreMock.DELAY_TIME)

        self.assertIsNotNone(self.core_data.get_dplugin_by_uname(PL_1_NAME), 'No Plugin in CoreData with uname '+PL_1_NAME)
        self.assertIsNotNone(self.gui_data.get_dplugin_by_uname(PL_1_NAME), 'No Plugin in GuiData with uname '+PL_1_NAME)
        self.assertEqual(self.core_data.get_dplugins_count(), 1, 'Core PL Count not 1')
        self.assertEqual(self.gui_data.get_dplugins_count(), 1, 'Gui PL Count not 1')

        self.gui_api.do_delete_plugin_uname(PL_1_NAME)

        time.sleep(TestCoreMock.DELAY_TIME)

        self.assertIsNone(self.core_data.get_dplugin_by_uname(PL_1_NAME), 'Plugin still in core_data')
        self.assertIsNone(self.gui_data.get_dplugin_by_uname(PL_1_NAME), 'Plugin still in gui_data')
        self.assertEqual(self.core_data.get_dplugins_count(), 0, 'Core PL Count not 0')
        self.assertEqual(self.gui_data.get_dplugins_count(), 0, 'Gui PL Count not 0')

    def test_reset_papi_1(self):
        PL_1_NAME = 'Plot1'
        PL_1_IDENT = 'Plot'
        self.gui_api.do_create_plugin(PL_1_IDENT,PL_1_NAME)

        time.sleep(TestCoreMock.DELAY_TIME)

        self.assertIsNotNone(self.core_data.get_dplugin_by_uname(PL_1_NAME), 'No Plugin in CoreData with uname '+PL_1_NAME)
        self.assertIsNotNone(self.gui_data.get_dplugin_by_uname(PL_1_NAME), 'No Plugin in GuiData with uname '+PL_1_NAME)
        self.assertEqual(self.core_data.get_dplugins_count(), 1, 'Core PL Count not 1')
        self.assertEqual(self.gui_data.get_dplugins_count(), 1, 'Gui PL Count not 1')

        self.gui_api.do_reset_papi()

        time.sleep(TestCoreMock.DELAY_TIME)

        self.assertIsNone(self.core_data.get_dplugin_by_uname(PL_1_NAME), 'Plugin still in core_data')
        self.assertIsNone(self.gui_data.get_dplugin_by_uname(PL_1_NAME), 'Plugin still in gui_data')
        self.assertEqual(self.core_data.get_dplugins_count(), 0, 'Core PL Count not 0')
        self.assertEqual(self.gui_data.get_dplugins_count(), 0, 'Gui PL Count not 0')

    def test_reset_papi_2(self):

        Plugins = [ ['Plot1', 'Plot'], ['Sinus1', 'Sinus'], ['Add1', 'Add'], ['Butt', 'Button'] ]

        for pl in Plugins:
            self.gui_api.do_create_plugin(pl[1], pl[0])

        time.sleep(TestCoreMock.DELAY_TIME)

        for pl in Plugins:
            self.assertIsNotNone(self.core_data.get_dplugin_by_uname(pl[0]), 'No Plugin in CoreData with uname '+pl[0])
            self.assertIsNotNone(self.gui_data.get_dplugin_by_uname(pl[0]), 'No Plugin in GuiData with uname '+pl[0])


        self.assertEqual(self.core_data.get_dplugins_count(), len(Plugins), 'Core PL Count not correct')
        self.assertEqual(self.gui_data.get_dplugins_count(), len(Plugins), 'Gui PL Count not correct')


        self.gui_api.do_reset_papi()


        time.sleep(TestCoreMock.DELAY_TIME)

        for pl in Plugins:
            self.assertIsNone(self.core_data.get_dplugin_by_uname(pl[0]), 'Plugin in CoreData with uname '+pl[0])
            self.assertIsNone(self.gui_data.get_dplugin_by_uname(pl[0]), 'Plugin in GuiData with uname '+pl[0])


        self.assertEqual(self.core_data.get_dplugins_count(), 0, 'Core PL Count not correct')
        self.assertEqual(self.gui_data.get_dplugins_count(), 0, 'Gui PL Count not correct')

    def test_stopReset_iop(self):

        Plugins = [ ['Plot1', 'Plot'], ['Sinus1', 'Sinus'], ['Add1', 'Add'], ['Butt', 'Button'] ]

        for pl in Plugins:
            self.gui_api.do_create_plugin(pl[1], pl[0])

        time.sleep(TestCoreMock.DELAY_TIME)

        for pl in Plugins:
            self.assertIsNotNone(self.core_data.get_dplugin_by_uname(pl[0]), 'No Plugin in CoreData with uname '+pl[0])
            self.assertIsNotNone(self.gui_data.get_dplugin_by_uname(pl[0]), 'No Plugin in GuiData with uname '+pl[0])


        self.assertEqual(self.core_data.get_dplugins_count(), len(Plugins), 'Core PL Count not correct')
        self.assertEqual(self.gui_data.get_dplugins_count(), len(Plugins), 'Gui PL Count not correct')


        self.gui_api.do_stopReset_plugin_uname('Sinus1')

        time.sleep(TestCoreMock.DELAY_TIME)

        for pl in Plugins:
            self.assertIsNotNone(self.core_data.get_dplugin_by_uname(pl[0]), 'No Plugin in CoreData with uname '+pl[0])
            self.assertIsNotNone(self.gui_data.get_dplugin_by_uname(pl[0]), 'No Plugin in GuiData with uname '+pl[0])

    def test_stopReset_restart_iop(self):

        Plugins = [  ['Sinus1', 'Sinus'] ]

        for pl in Plugins:
            self.gui_api.do_create_plugin(pl[1], pl[0])

        time.sleep(TestCoreMock.DELAY_TIME)

        for pl in Plugins:
            self.assertIsNotNone(self.core_data.get_dplugin_by_uname(pl[0]), 'No Plugin in CoreData with uname '+pl[0])
            self.assertIsNotNone(self.gui_data.get_dplugin_by_uname(pl[0]), 'No Plugin in GuiData with uname '+pl[0])


        self.assertEqual(self.core_data.get_dplugins_count(), len(Plugins), 'Core PL Count not correct')
        self.assertEqual(self.gui_data.get_dplugins_count(), len(Plugins), 'Gui PL Count not correct')


        self.gui_api.do_stopReset_plugin_uname('Sinus1')

        time.sleep(TestCoreMock.DELAY_TIME)

        for pl in Plugins:
            self.assertIsNotNone(self.core_data.get_dplugin_by_uname(pl[0]), 'No Plugin in CoreData with uname '+pl[0])
            self.assertIsNotNone(self.gui_data.get_dplugin_by_uname(pl[0]), 'No Plugin in GuiData with uname '+pl[0])

        self.assertEqual(self.core_data.get_dplugin_by_uname('Sinus1').state, const.PLUGIN_STATE_STOPPED)
        self.assertEqual(self.gui_data.get_dplugin_by_uname('Sinus1').state, const.PLUGIN_STATE_STOPPED)


        self.gui_api.do_start_plugin_uname('Sinus1')

        time.sleep(TestCoreMock.DELAY_TIME)

        self.assertEqual(self.core_data.get_dplugin_by_uname('Sinus1').state, const.PLUGIN_STATE_START_SUCCESFUL)
        self.assertEqual(self.gui_data.get_dplugin_by_uname('Sinus1').state, const.PLUGIN_STATE_START_SUCCESFUL)



















    def setUp(self):
        core = Core(use_gui=False)
        core.gui_process = dummyProcess()
        core.gui_alive = True

        self.core_thread = Thread(target=core.run)
        self.core_thread.start()


        self.gui_data = DGui()

        self.gui_thread = Thread(target=startGUI_TESTMOCK, args=[core.core_event_queue, core.gui_event_queue, core.gui_id, self.gui_data])
        self.gui_thread.start()


        # get data and queues
        self.core_queue = core.core_event_queue
        self.gui_queue = core.gui_event_queue
        self.core_data = core.core_data

        self.gui_api = Gui_api(self.gui_data, self.core_queue, core.gui_id)

        time.sleep(1)

    def tearDown(self):
        # close Gui
        self.gui_queue.put(  PapiEvent(1,1,'instr_event','test_close', None)  )

        # wait for close
        # time.sleep(1)

        # join threads
        self.gui_thread.join()
        self.core_thread.join()


if __name__ == "__main__":
    unittest.main();