__author__ = 'fescycling'

from PyQt5.QtWidgets    import QLineEdit, QMainWindow, QMenu, QAbstractItemView, QAction, QTreeView, QVBoxLayout
from PyQt5.QtCore import Qt, QRegExp

from papi.gui.default.item import DParameterTreeModel, DParameterTreeItem

class ParameterWindow(QMainWindow):
    def __init__(self, dplugin, api, pl_win_name = '',parent = None):
        QMainWindow.__init__(self, parent)

        # Build the tree for the parameters
        self.parameterTree = QTreeView(self)
        self.parameterTree.setObjectName("parameterTree")
        # Add it as the central widget
        self.setCentralWidget(self.parameterTree)
        # Add the DParameterTreeModel to the parameter tree
        self.dparameterModel = DParameterTreeModel()
        self.dparameterModel.setHorizontalHeaderLabels(['Name',''])
        self.parameterTree.setModel(self.dparameterModel)
        self.parameterTree.setUniformRowHeights(True)
        # connect the callback function for value changes
        self.dparameterModel.dataChanged.connect(self.data_changed_parameter_model)

        self.dpluign_object = dplugin
        self.api = api

        self.setWindowTitle(pl_win_name+' Parameter')



    def show_paramters(self, para_list):
        """
        Shows the list of parameters and values in the parameter window
        :param para_list:
        :return:
        """
        for dparameter_name in sorted(para_list):
            dparameter = para_list[dparameter_name]
            dparameter_item = DParameterTreeItem(dparameter)
            self.dparameterModel.appendRow(dparameter_item)
            self.parameterTree.resizeColumnToContents(0)
            self.parameterTree.resizeColumnToContents(1)
        self.parameterTree.expandAll()

        fh = self.parameterTree.fontMetrics().height()

        if len(para_list.keys()) > 8:
            self.setFixedHeight(fh*9+fh+25)
        else:
             self.setFixedHeight(fh*len(para_list.keys())+fh+fh+25)




    def data_changed_parameter_model(self, index, n):
        """
        This function is called when a dparameter value is changed by editing the 'value'-column.

        :param index: Index of current changed dparameter
        :param n: None
        :return:
        """

        dparameter = self.parameterTree.model().data(index, Qt.UserRole)

        self.api.do_set_parameter(self.dpluign_object.id, dparameter.name, dparameter.value)
