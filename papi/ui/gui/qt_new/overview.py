# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/gui/qt_new/overview.ui'
#
# Created: Mon Dec  1 17:42:16 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Overview(object):
    def setupUi(self, Overview):
        Overview.setObjectName("Overview")
        Overview.resize(803, 614)
        self.centralwidget = QtGui.QWidget(Overview)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pluginTree = QtGui.QTreeView(self.centralwidget)
        self.pluginTree.setObjectName("pluginTree")
        self.horizontalLayout.addWidget(self.pluginTree)
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(False)
        self.tabWidget.setObjectName("tabWidget")
        self.pluginTab = QtGui.QWidget()
        self.pluginTab.setObjectName("pluginTab")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.pluginTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.unameLabel = QtGui.QLabel(self.pluginTab)
        self.unameLabel.setObjectName("unameLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.unameLabel)
        self.unameEdit = QtGui.QLineEdit(self.pluginTab)
        self.unameEdit.setObjectName("unameEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.unameEdit)
        self.usedpluginLabel = QtGui.QLabel(self.pluginTab)
        self.usedpluginLabel.setObjectName("usedpluginLabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.usedpluginLabel)
        self.usedpluginEdit = QtGui.QLineEdit(self.pluginTab)
        self.usedpluginEdit.setObjectName("usedpluginEdit")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.usedpluginEdit)
        self.stateLabel = QtGui.QLabel(self.pluginTab)
        self.stateLabel.setObjectName("stateLabel")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.stateLabel)
        self.stateEdit = QtGui.QLineEdit(self.pluginTab)
        self.stateEdit.setObjectName("stateEdit")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.stateEdit)
        self.typeLabel = QtGui.QLabel(self.pluginTab)
        self.typeLabel.setObjectName("typeLabel")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.typeLabel)
        self.typeEdit = QtGui.QLineEdit(self.pluginTab)
        self.typeEdit.setObjectName("typeEdit")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.typeEdit)
        self.alivestateLabel = QtGui.QLabel(self.pluginTab)
        self.alivestateLabel.setObjectName("alivestateLabel")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.alivestateLabel)
        self.alivestateEdit = QtGui.QLineEdit(self.pluginTab)
        self.alivestateEdit.setObjectName("alivestateEdit")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.alivestateEdit)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.tabWidget_2 = QtGui.QTabWidget(self.pluginTab)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.parameterTab = QtGui.QWidget()
        self.parameterTab.setObjectName("parameterTab")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.parameterTab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.parameterTree = QtGui.QTreeView(self.parameterTab)
        self.parameterTree.setObjectName("parameterTree")
        self.verticalLayout_4.addWidget(self.parameterTree)
        self.tabWidget_2.addTab(self.parameterTab, "")
        self.blockTab = QtGui.QWidget()
        self.blockTab.setObjectName("blockTab")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.blockTab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.blockTree = QtGui.QTreeView(self.blockTab)
        self.blockTree.setObjectName("blockTree")
        self.verticalLayout_5.addWidget(self.blockTree)
        self.tabWidget_2.addTab(self.blockTab, "")
        self.verticalLayout_2.addWidget(self.tabWidget_2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pauseButton = QtGui.QPushButton(self.pluginTab)
        self.pauseButton.setObjectName("pauseButton")
        self.horizontalLayout_2.addWidget(self.pauseButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.stopButton = QtGui.QPushButton(self.pluginTab)
        self.stopButton.setObjectName("stopButton")
        self.horizontalLayout_2.addWidget(self.stopButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.playButton = QtGui.QPushButton(self.pluginTab)
        self.playButton.setObjectName("playButton")
        self.horizontalLayout_2.addWidget(self.playButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.tabWidget.addTab(self.pluginTab, "")
        self.connectionTab = QtGui.QWidget()
        self.connectionTab.setObjectName("connectionTab")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.connectionTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.subscribersTree = QtGui.QTreeView(self.connectionTab)
        self.subscribersTree.setObjectName("subscribersTree")
        self.verticalLayout.addWidget(self.subscribersTree)
        self.subscriptionsTree = QtGui.QTreeView(self.connectionTab)
        self.subscriptionsTree.setObjectName("subscriptionsTree")
        self.verticalLayout.addWidget(self.subscriptionsTree)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.tabWidget.addTab(self.connectionTab, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        Overview.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(Overview)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 803, 25))
        self.menubar.setObjectName("menubar")
        self.menuAction = QtGui.QMenu(self.menubar)
        self.menuAction.setObjectName("menuAction")
        Overview.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(Overview)
        self.statusbar.setObjectName("statusbar")
        Overview.setStatusBar(self.statusbar)
        self.actionRefresh = QtGui.QAction(Overview)
        self.actionRefresh.setObjectName("actionRefresh")
        self.menuAction.addAction(self.actionRefresh)
        self.menubar.addAction(self.menuAction.menuAction())

        self.retranslateUi(Overview)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Overview)

    def retranslateUi(self, Overview):
        Overview.setWindowTitle(QtGui.QApplication.translate("Overview", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.unameLabel.setText(QtGui.QApplication.translate("Overview", "Unique name", None, QtGui.QApplication.UnicodeUTF8))
        self.usedpluginLabel.setText(QtGui.QApplication.translate("Overview", "Used plugin", None, QtGui.QApplication.UnicodeUTF8))
        self.stateLabel.setText(QtGui.QApplication.translate("Overview", "State", None, QtGui.QApplication.UnicodeUTF8))
        self.typeLabel.setText(QtGui.QApplication.translate("Overview", "Type", None, QtGui.QApplication.UnicodeUTF8))
        self.alivestateLabel.setText(QtGui.QApplication.translate("Overview", "Alive state", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.parameterTab), QtGui.QApplication.translate("Overview", "Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.blockTab), QtGui.QApplication.translate("Overview", "Blocks", None, QtGui.QApplication.UnicodeUTF8))
        self.pauseButton.setText(QtGui.QApplication.translate("Overview", "PAUSE", None, QtGui.QApplication.UnicodeUTF8))
        self.stopButton.setText(QtGui.QApplication.translate("Overview", "STOP", None, QtGui.QApplication.UnicodeUTF8))
        self.playButton.setText(QtGui.QApplication.translate("Overview", "PLAY", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.pluginTab), QtGui.QApplication.translate("Overview", "Plugin", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.connectionTab), QtGui.QApplication.translate("Overview", "Connections", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAction.setTitle(QtGui.QApplication.translate("Overview", "Actions", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRefresh.setText(QtGui.QApplication.translate("Overview", "Refresh", None, QtGui.QApplication.UnicodeUTF8))

