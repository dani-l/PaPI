#!/usr/bin/python3
# -*- coding: latin-1 -*-

"""
Copyright (C) 2014 Technische Universitšt Berlin,
Fakultšt IV - Elektrotechnik und Informatik,
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

Contributors
Sven Knuth
"""

__author__ = 'knuths'

from PyQt5.QtWidgets    import QMdiSubWindow, QAction, QToolBar,QTreeView, QMenu
from PyQt5.QtCore       import Qt, QRegExp, pyqtSignal
from PyQt5.QtGui        import QStandardItemModel, QStandardItem, QPixmap, QBrush, QColor, QIcon, QDragEnterEvent, QDropEvent
from papi.data.DPlugin import *
from papi.data.DSignal import DSignal
from papi.gui.default import get16Pixmap
from papi.yapsy.PluginInfo import PluginInfo


# ------------------------------------
# Item Object
# ------------------------------------


class PaPITreeItem(QStandardItem):
    def __init__(self, object,  name):
        super(PaPITreeItem, self).__init__(name)
        self.object = object
        self.name = name
        self.tool_tip = "Plugin: " + self.name

    def data(self, role):
        """
        For Qt.Role see 'http://qt-project.org/doc/qt-4.8/qt.html#ItemDataRole-enum'
        :param role:
        :return:
        """

        if role == Qt.ToolTipRole:
            return self.tool_tip

        if role == Qt.DisplayRole:
            return self.name

        if role == Qt.DecorationRole:
            return self.get_decoration()

        if role == Qt.UserRole:
            return self.object

        return None

    def get_decoration(self):
        return None


class PaPIRootItem(QStandardItem):
    def __init__(self, name):
        super(PaPIRootItem, self).__init__(name)
        self.setEditable(False)
        self.setSelectable(False)
        self.name = name

    def data(self, role):
        """
        For Qt.Role see 'http://qt-project.org/doc/qt-4.8/qt.html#ItemDataRole-enum'
        :param role:
        :return:
        """

        # if role == Qt.ToolTipRole:
        #     return self.tool_tip

        if role == Qt.DisplayRole:
            return self.name + " (" + str(self.rowCount()) + ")"

        # if role == Qt.DecorationRole:
        #     return self.get_decoration()

        # if role == Qt.UserRole:
        #     return self.object

        return None

    def clean(self):
        """
        This function is called to remove all rows which contain an item marked as 'deleted'.
        This only works with items having an state-attribute e.g. DPlugin.

        :return:
        """
        for row in range(self.rowCount()):
            treeItem = self.child(row)
            if treeItem is not None:
                item = treeItem.data(Qt.UserRole)
                if hasattr(item, 'state'):
                    if item.state == 'deleted':
                        self.removeRow(row)

    def hasItem(self, sItem):
        """
        Used to check if an item is already part of this Tree

        :param sItem: Searched for this item
        :return:
        """
        for row in range(self.rowCount()):
            treeItem = self.child(row)
            if treeItem is not None:
                item = treeItem.data(Qt.UserRole)
                if item == sItem:
                    return True

# ------------------------------------
# Model Objects
# ------------------------------------


class PaPITreeModel(QStandardItemModel):
    def __init__(self, parent=None):
        super(PaPITreeModel, self).__init__(parent)

    def flags(self, index):
        row = index.row()
        col = index.column()

        parent = index.parent()

        if not parent.isValid():
            return Qt.ItemIsEnabled

        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled

# ------------------------------------
# Item Custom
# ------------------------------------


class PluginTreeItem(PaPITreeItem):
    def __init__(self,  plugin_info):
        super(PluginTreeItem, self).__init__(plugin_info, plugin_info.name)
        self.plugin_info = plugin_info
        self.setEditable(False)

    def get_decoration(self):
        l = len(self.object.name)
        path = self.object.path[:-l]
        path += 'box.png'
        px = QPixmap(path)
        return px

    def data(self, role):

        if role == Qt.BackgroundRole:
            if not self.object.loadable:
                return QBrush(QColor(255,0,0,50))

        return super(PluginTreeItem, self).data(role)

class DPluginTreeItem(PaPITreeItem):
    def __init__(self,  dplugin: DPlugin):
        super(DPluginTreeItem, self).__init__(dplugin, dplugin.uname)
        self.dplugin = dplugin
        self.name = dplugin.uname
        self.setEditable(False)

    def get_decoration(self):
        l = len(self.dplugin.plugin_identifier)
        path = self.dplugin.path[:-l]
        path += 'box.png'
        px = QPixmap(path)
        return px

class DParameterTreeItem(PaPITreeItem):
    def __init__(self,  dparameter: DParameter):
        super(DParameterTreeItem, self).__init__(dparameter, str(dparameter.value))
        self.dparameter = dparameter
        self.setEditable(False)
        self.tool_tip = dparameter.name

    def get_decoration(self):
        return None


class DBlockTreeItem(PaPITreeItem):
    def __init__(self,  dblock: DBlock):
        super(DBlockTreeItem, self).__init__(dblock, dblock.name)
        self.dblock = dblock
        self.setSelectable(False)
        self.setEditable(False)

        self.tool_tip = "DBlock: " + dblock.name

        if isinstance(dblock, DEvent):
            brush = QBrush()
            brush.setColor(Qt.magenta)
            self.tool_tip = "DEvent: " + dblock.name
            self.setForeground(brush)
            self.setSelectable(True)


    def get_decoration(self):

        if isinstance(self.object, DEvent):
            return get16Pixmap("events.png")

        if isinstance(self.object, DBlock):
            return get16Pixmap("transmit.png")

        return None


class DSignalTreeItem(PaPITreeItem):
    def __init__(self,  dsignal: DSignal, check_box):
        super(DSignalTreeItem, self).__init__(dsignal, dsignal.dname)
        self.dsignal = dsignal
        self.setSelectable(False)
        self.setEditable(False)
        self.tool_tip = "InternalName: " + dsignal.uname
        self.check_box = check_box

    def get_decoration(self):
        return None

    def data(self, role):
        """
        For Qt.Role see 'http://qt-project.org/doc/qt-4.8/qt.html#ItemDataRole-enum'
        :param role:
        :return:
        """

        if role == Qt.ToolTipRole:
            return self.tool_tip

        if role == Qt.DisplayRole:
            if self.check_box.isChecked():
                return self.dsignal.uname
            else:
                return self.dsignal.dname

        if role == Qt.DecorationRole:
            return self.get_decoration()

        if role == Qt.UserRole:
            return self.object

        if role == Qt.EditRole:
            return self.dsignal.dname

        return None

# ------------------------------------
# Model Custom
# ------------------------------------


class PluginTreeModel(PaPITreeModel):
    """
    This model is used to handle Plugin objects in TreeView created by the yapsy plugin manager.
    """
    def __init__(self, parent=None):
        super(PluginTreeModel, self).__init__(parent)

class DPluginTreeModel(PaPITreeModel):
    """
    This model is used to handle DPlugin objects in TreeView.
    """
    def __init__(self, parent=None):
        super(DPluginTreeModel, self).__init__(parent)


class DParameterTreeModel(PaPITreeModel):
    """
    This model is used to handle DParameter objects in TreeView.
    """
    def __init__(self, parent=None):
        super(DParameterTreeModel, self).__init__(parent)

    def flags(self, index):
        """
        This function returns the flags for a specific index.

        For Qt.ItemFlags see 'http://qt-project.org/doc/qt-4.8/qt.html#ItemFlag-enum'
        :param index:
        :return:
        """
        row = index.row()
        col = index.column()

        parent = index.parent()

        # if not parent.isValid():
        #     return ~Qt.ItemIsSelectable & ~Qt.ItemIsEditable

        if col == 0:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled

        if col == 1:
            return Qt.ItemIsEditable | Qt.ItemIsEnabled

    def data(self, index, role):
        """
        For Qt.Role see 'http://qt-project.org/doc/qt-4.8/qt.html#ItemDataRole-enum'
        :param index:
        :param role:
        :return:
        """

        if not index.isValid():
            return None

        row = index.row()
        col = index.column()

        if role == Qt.ToolTipRole:
            return super(DParameterTreeModel, self).data(index, Qt.ToolTipRole)

        if role == Qt.DisplayRole:

            if col == 0:
                dparameter = super(DParameterTreeModel, self).data(index, Qt.UserRole)
                return dparameter.name
            if col == 1:
                index_sibling = index.sibling(row, col-1)
                dparameter = super(DParameterTreeModel, self).data(index_sibling, Qt.UserRole)
                return dparameter.value

        if role == Qt.DecorationRole:
            if col == 0:
                return super(DParameterTreeModel, self).data(index, Qt.DecorationRole)
            if col == 1:
                return QIcon.fromTheme("edit-clear")

        if role == Qt.UserRole:
            return super(DParameterTreeModel, self).data(index, Qt.UserRole)

        if role == Qt.EditRole:
            if col == 1:
                index_sibling = index.sibling(row, col-1)
                dparameter = super(DParameterTreeModel, self).data(index_sibling, Qt.UserRole)
                return str(dparameter.value)

        return None

    def setData(self, index, value, role):
        """
        This function is called when a content in a row is edited by the user.

        :param index: Current selected index.
        :param value: New value from user
        :param role:
        :return:
        """

        if not index.isValid():
            return None

        row = index.row()
        col = index.column()

        if role == Qt.EditRole:
            if col == 1:
                index_sibling = index.sibling(row, col-1)
                dparameter = super(DParameterTreeModel, self).data(index_sibling, Qt.UserRole)

                if dparameter.regex is not None:
                    rx = QRegExp(dparameter.regex)
                    if rx.exactMatch(value):
                        dparameter.value = value
                        self.dataChanged.emit(index_sibling, index_sibling)
                else:
                    dparameter.value = value
                    self.dataChanged.emit(index_sibling, index_sibling)

                return True

        return False


class DBlockTreeModel(PaPITreeModel):
    def __init__(self, check_box, parent=None):
        super(DBlockTreeModel, self).__init__(parent)
        self.check_box = check_box

    def flags(self, index):
        """
        This function returns the flags for a specific index.

        For Qt.ItemFlags see 'http://qt-project.org/doc/qt-4.8/qt.html#ItemFlag-enum'
        :param index:
        :return:
        """
        parent = index.parent()
        flags = parent.flags()


        if not parent.isValid():
            flags ^= Qt.ItemIsSelectable
            flags ^= Qt.ItemIsEditable
            return flags



        if parent.isValid():
            if self.check_box.isChecked():
                flags ^= Qt.ItemIsEditable
                return flags
            else:
                flags |= Qt.ItemIsSelectable
                flags |= Qt.ItemIsEnabled
                flags |= Qt.ItemIsEditable
                return flags


    def setData(self, index, value, role):
        """
        This function is called when a content in a row is edited by the user.

        :param index: Current selected index.
        :param value: New value from user
        :param role:
        :return:
        """

        if not index.isValid():
            return None

        row = index.row()
        col = index.column()

        if role == Qt.EditRole:

                dsignal = super(DBlockTreeModel, self).data(index, Qt.UserRole)

                if value != dsignal.dname:
                    dsignal.dname = value
                    self.dataChanged.emit(index, index)

                return True

        return False

class CustomFieldModel(QStandardItemModel):
    def __init__(self, parent=None):
        super(CustomFieldModel, self).__init__(parent)

    def data(self, index, role):
        """
        For Qt.Role see 'http://qt-project.org/doc/qt-4.8/qt.html#ItemDataRole-enum'
        :param index:
        :param role:
        :return:
        """

        if not index.isValid():
            return None

        row = index.row()
        col = index.column()

        if role == Qt.ToolTipRole:
            return super(CustomFieldModel, self).data(index, Qt.ToolTipRole)

        if role == Qt.DisplayRole:

            if col == 0:
                field = super(CustomFieldModel, self).data(index, Qt.UserRole)
                return field.desc
            if col == 1:
                index_sibling = index.sibling(row, col-1)
                field = super(CustomFieldModel, self).data(index_sibling, Qt.UserRole)
                return field.size
            if col == 2:
                return None

        if role == Qt.DecorationRole:
            pass

        if role == Qt.UserRole:
            pass

        if role == Qt.EditRole:
            if col == 0:
                field = super(CustomFieldModel, self).data(index, Qt.UserRole)
                return field.desc
            if col == 1:
                index_sibling = index.sibling(row, col-1)
                field = super(CustomFieldModel, self).data(index_sibling, Qt.UserRole)
                return field.size
            if col == 2:
                return None

        return None

    def setData(self, index, value, role):
        """
        This function is called when a content in a row is edited by the user.

        :param index: Current selected index.
        :param value: New value from user
        :param role:
        :return:
        """

        if not index.isValid():
            return None

        row = index.row()
        col = index.column()

        if role == Qt.EditRole:

            if col == 0:

                field = super(CustomFieldModel, self).data(index, Qt.UserRole)
                field.desc = value
                self.dataChanged.emit(index, None)

                return True

            if col == 1:
                index_sibling = index.sibling(row, col-1)
                field = super(CustomFieldModel, self).data(index_sibling, Qt.UserRole)
                field.size = value
                self.dataChanged.emit(index, None)

        return False


class StructTreeModel(PaPITreeModel):
    """
    This model is used to handle Plugin objects in TreeView created by the yapsy plugin manager.
    """
    def __init__(self, parent=None):
        super(StructTreeModel, self).__init__(parent)

    def data(self, index, role):
        """
        For Qt.Role see 'http://qt-project.org/doc/qt-4.8/qt.html#ItemDataRole-enum'
        :param index:
        :param role:
        :return:
        """

        if not index.isValid():
            return None

        row = index.row()
        col = index.column()

        if role == Qt.ToolTipRole:
            return super(StructTreeModel, self).data(index, Qt.ToolTipRole)

        if role == Qt.DisplayRole:

            if col == 0:
                item = super(StructTreeModel, self).data(index, Qt.UserRole)
                if item is None:
                    return super(StructTreeModel, self).data(index, Qt.DisplayRole)
                return item.desc

            return 'Quark'
            if col == 1:
                index_sibling = index.sibling(row, col-1)
                item = super(StructTreeModel, self).data(index_sibling, Qt.UserRole)
                return item.size
            if col == 2:
                return None

        if role == Qt.DecorationRole:
            pass

        if role == Qt.UserRole:
            pass

        if role == Qt.EditRole:
            if col == 0:
                item = super(StructTreeModel, self).data(index, Qt.UserRole)
                return item.field
            if col == 1:
                index_sibling = index.sibling(row, col-1)
                item = super(StructTreeModel, self).data(index_sibling, Qt.UserRole)
                return item.size
            if col == 2:
                return None

        return None

class StructRootNode(QStandardItem):
    """
    This model is used to handle Plugin objects in TreeView created by the yapsy plugin manager.
    """
    def __init__(self, name, parent=None):
        super(StructRootNode, self).__init__(name)
        self.nodes = {}
        self.size = ''
        self.field = 'Data'

    def appendRow(self, field):

        elements = str.split(field.desc, "::")

        # Create new sub node for this element

        if elements[0] not in self.nodes:

#            sub_elements = str.split(field.desc, "::", 1)
            #field.desc = sub_elements[1]
            struct_node = StructTreeNode(field, 0)
            self.nodes[elements[0]] = struct_node

            super(StructRootNode, self).appendRow(struct_node)

        # There is already a subnode for this element

        if elements[0] in self.nodes:
            self.nodes[elements[0]].appendRow(field)


class StructTreeNode(QStandardItem):
    """
    This model is used to handle Plugin objects in TreeView created by the yapsy plugin manager.
    """
    def __init__(self, field, level, parent=None):

        elements = str.split(field.desc, "::")

        self.nodes = {}
        self.level = level
        self.time_identifier = 'time'
        self.ptime_identifier = 'ptime'
        self.size = ''
        self.field = ''
        self.object = field

        super(StructTreeNode, self).__init__(elements[self.level])

        self.appendRow(field)

    def appendRow(self, field):

        elements = str.split(field.desc, "::")

        # Node is responsible for the first element

        if len(elements) > self.level + 1:

            if self.time_identifier not in self.nodes:
                struct_node = QStandardItem(self.time_identifier)
                self.nodes[self.time_identifier] = struct_node
                super(StructTreeNode, self).appendRow(struct_node)

            if self.ptime_identifier not in self.nodes:
                struct_node = QStandardItem(self.ptime_identifier)
                self.nodes[self.ptime_identifier] = struct_node
                super(StructTreeNode, self).appendRow(struct_node)

            if elements[self.level + 1] not in self.nodes:
                struct_node = StructTreeNode(field, self.level + 1)
                self.nodes[elements[self.level + 1]] = struct_node
                super(StructTreeNode, self).appendRow(struct_node)

            if elements[self.level + 1] in self.nodes:
                self.nodes[elements[self.level + 1]].appendRow(field)
        else:
            self.size = '3x1'
            self.field = elements[self.level]

    def data(self, role):
        """
        For Qt.Role see 'http://qt-project.org/doc/qt-4.8/qt.html#ItemDataRole-enum'
        :param role:
        :return:
        """
        if role == Qt.ToolTipRole:
            return None

        if role == Qt.DisplayRole:
            return self.field

        if role == Qt.DecorationRole:
            return None

        if role == Qt.UserRole:
            return self.object

        if role == Qt.EditRole:
            return None

        return None

# ------------------------------------
# Custom GUI elements
# ------------------------------------


class PaPIMDISubWindow(QMdiSubWindow):
    def __init__(self):
        super(PaPIMDISubWindow, self).__init__()
        self.movable = True

    def mouseMoveEvent(self, event):
        if self.movable:
            super(PaPIMDISubWindow, self).mouseMoveEvent(event)

    def set_movable(self, flag):
        self.movable = flag

class PaPIFavAction(QAction):

    def __init__(self, *args, **kwargs):
        super(PaPIFavAction, self).__init__(*args, **kwargs)

class PaPIToolbar(QToolBar):
    clickedFavouritePlugin = pyqtSignal(PluginInfo)
    removedFavouritePlugin = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(PaPIToolbar, self).__init__(*args, **kwargs)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.customMenu)
    def dragEnterEvent(self, event: QDragEnterEvent):
        source = event.source()
        if isinstance(source, QTreeView):
            if isinstance(source.model(), PaPITreeModel):
                event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        source = event.source()
        if isinstance(source, QTreeView):
            if isinstance(source.model(), PaPITreeModel):
                for index in source.selectedIndexes():
                    plugin_info = source.model().data(index, Qt.UserRole)
                    self.clickedFavouritePlugin.emit(plugin_info)

    def customMenu(self, position):
        menu = QMenu('Menu')
        fav_menu = QMenu('Favourites')
        px = get16Pixmap('star.png')
        hasFavourites = False

        fav_menu.setIcon(QIcon(px))

        for action in self.actions():
            if isinstance(action, PaPIFavAction):
                fav_action = QAction(action.text(), self)
                px = get16Pixmap('delete.png')
                fav_action.setIcon(QIcon(px))
                fav_action.triggered.connect(lambda ignore, p=action: self.removeFavouritePlugin(p))

                fav_menu.addAction(fav_action)
                hasFavourites = True

        menu.addMenu(fav_menu)

        if hasFavourites:
            menu.exec_(self.mapToGlobal(position))

    def removeFavouritePlugin(self, action : PaPIFavAction):
        self.removeAction(action)
        self.removedFavouritePlugin.emit()
