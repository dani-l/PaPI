# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/gui/default/PluginOverviewMenu.ui'
#
# Created: Wed Sep 23 16:34:27 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PluginOverviewMenu(object):
    def setupUi(self, PluginOverviewMenu):
        PluginOverviewMenu.setObjectName("PluginOverviewMenu")
        PluginOverviewMenu.resize(803, 614)
        self.centralwidget = QtWidgets.QWidget(PluginOverviewMenu)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pluginTree = QtWidgets.QTreeView(self.centralwidget)
        self.pluginTree.setObjectName("pluginTree")
        self.verticalLayout.addWidget(self.pluginTree)
        self.pluginSearchText = QtWidgets.QLineEdit(self.centralwidget)
        self.pluginSearchText.setObjectName("pluginSearchText")
        self.verticalLayout.addWidget(self.pluginSearchText)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.pluginWidget = QtWidgets.QWidget(self.centralwidget)
        self.pluginWidget.setEnabled(False)
        self.pluginWidget.setObjectName("pluginWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.pluginWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setHorizontalSpacing(6)
        self.formLayout.setObjectName("formLayout")
        self.unameLabel = QtWidgets.QLabel(self.pluginWidget)
        self.unameLabel.setObjectName("unameLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.unameLabel)
        self.unameEdit = QtWidgets.QLineEdit(self.pluginWidget)
        self.unameEdit.setObjectName("unameEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.unameEdit)
        self.usedpluginLabel = QtWidgets.QLabel(self.pluginWidget)
        self.usedpluginLabel.setObjectName("usedpluginLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.usedpluginLabel)
        self.usedpluginEdit = QtWidgets.QLineEdit(self.pluginWidget)
        self.usedpluginEdit.setObjectName("usedpluginEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.usedpluginEdit)
        self.stateLabel = QtWidgets.QLabel(self.pluginWidget)
        self.stateLabel.setObjectName("stateLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.stateLabel)
        self.stateEdit = QtWidgets.QLineEdit(self.pluginWidget)
        self.stateEdit.setObjectName("stateEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.stateEdit)
        self.typeLabel = QtWidgets.QLabel(self.pluginWidget)
        self.typeLabel.setObjectName("typeLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.typeLabel)
        self.typeEdit = QtWidgets.QLineEdit(self.pluginWidget)
        self.typeEdit.setObjectName("typeEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.typeEdit)
        self.alivestateLabel = QtWidgets.QLabel(self.pluginWidget)
        self.alivestateLabel.setObjectName("alivestateLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.alivestateLabel)
        self.alivestateEdit = QtWidgets.QLineEdit(self.pluginWidget)
        self.alivestateEdit.setObjectName("alivestateEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.alivestateEdit)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.tabWidget_2 = QtWidgets.QTabWidget(self.pluginWidget)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.parameterTab = QtWidgets.QWidget()
        self.parameterTab.setObjectName("parameterTab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.parameterTab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.parameterTree = QtWidgets.QTreeView(self.parameterTab)
        self.parameterTree.setObjectName("parameterTree")
        self.verticalLayout_4.addWidget(self.parameterTree)
        self.tabWidget_2.addTab(self.parameterTab, "")
        self.blockTab = QtWidgets.QWidget()
        self.blockTab.setObjectName("blockTab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.blockTab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.showInternalNameCheckBox = QtWidgets.QCheckBox(self.blockTab)
        self.showInternalNameCheckBox.setObjectName("showInternalNameCheckBox")
        self.verticalLayout_5.addWidget(self.showInternalNameCheckBox)
        self.blockTree = QtWidgets.QTreeView(self.blockTab)
        self.blockTree.setObjectName("blockTree")
        self.verticalLayout_5.addWidget(self.blockTree)
        self.tabWidget_2.addTab(self.blockTab, "")
        self.connectionTab_2 = QtWidgets.QWidget()
        self.connectionTab_2.setObjectName("connectionTab_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.connectionTab_2)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.connectionTree = QtWidgets.QTreeView(self.connectionTab_2)
        self.connectionTree.setObjectName("connectionTree")
        self.verticalLayout_7.addWidget(self.connectionTree)
        self.tabWidget_2.addTab(self.connectionTab_2, "")
        self.verticalLayout_2.addWidget(self.tabWidget_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pauseButton = QtWidgets.QPushButton(self.pluginWidget)
        self.pauseButton.setObjectName("pauseButton")
        self.horizontalLayout_2.addWidget(self.pauseButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.stopButton = QtWidgets.QPushButton(self.pluginWidget)
        self.stopButton.setObjectName("stopButton")
        self.horizontalLayout_2.addWidget(self.stopButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.playButton = QtWidgets.QPushButton(self.pluginWidget)
        self.playButton.setObjectName("playButton")
        self.horizontalLayout_2.addWidget(self.playButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addWidget(self.pluginWidget)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        PluginOverviewMenu.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(PluginOverviewMenu)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 803, 25))
        self.menubar.setObjectName("menubar")
        self.menuAction = QtWidgets.QMenu(self.menubar)
        self.menuAction.setObjectName("menuAction")
        PluginOverviewMenu.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(PluginOverviewMenu)
        self.statusbar.setObjectName("statusbar")
        PluginOverviewMenu.setStatusBar(self.statusbar)
        self.actionRefresh = QtWidgets.QAction(PluginOverviewMenu)
        self.actionRefresh.setObjectName("actionRefresh")
        self.menuAction.addAction(self.actionRefresh)
        self.menubar.addAction(self.menuAction.menuAction())

        self.retranslateUi(PluginOverviewMenu)
        self.tabWidget_2.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(PluginOverviewMenu)

    def retranslateUi(self, PluginOverviewMenu):
        _translate = QtCore.QCoreApplication.translate
        PluginOverviewMenu.setWindowTitle(_translate("PluginOverviewMenu", "MainWindow"))
        self.pluginSearchText.setPlaceholderText(_translate("PluginOverviewMenu", "Search for ..."))
        self.unameLabel.setText(_translate("PluginOverviewMenu", "Unique name"))
        self.usedpluginLabel.setText(_translate("PluginOverviewMenu", "Used plugin"))
        self.stateLabel.setText(_translate("PluginOverviewMenu", "State"))
        self.typeLabel.setText(_translate("PluginOverviewMenu", "Type"))
        self.alivestateLabel.setText(_translate("PluginOverviewMenu", "Alive state"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.parameterTab), _translate("PluginOverviewMenu", "Parameters"))
        self.showInternalNameCheckBox.setText(_translate("PluginOverviewMenu", "Show internal signal names"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.blockTab), _translate("PluginOverviewMenu", "Blocks/Events"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.connectionTab_2), _translate("PluginOverviewMenu", "Connections"))
        self.pauseButton.setText(_translate("PluginOverviewMenu", "PAUSE"))
        self.stopButton.setText(_translate("PluginOverviewMenu", "STOP"))
        self.playButton.setText(_translate("PluginOverviewMenu", "PLAY"))
        self.menuAction.setTitle(_translate("PluginOverviewMenu", "Actions"))
        self.actionRefresh.setText(_translate("PluginOverviewMenu", "Refresh"))

