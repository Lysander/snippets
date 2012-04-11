#!/usr/bin/env python2
# coding: utf-8

#
#  Copyright (C) 2011  Christian Hausknecht
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
    ~~~~~~~~~~~~~~~~~~~~~~~
    progress_table_delegate
    ~~~~~~~~~~~~~~~~~~~~~~~
    
    .. module:: progress_table_delegate
        :platform: Linux, Windows
        :synopsis: Simple demonstration how to use a delegate. This one shows
                   a QProgressBar-Widget inside a QTreeView

    .. moduleauthor:: Christian Hausknecht <christian.hausknecht@gmx.de>
"""

import sys
from PyQt4 import QtGui, uic, QtCore, Qt


class ProgressDelegate(QtGui.QStyledItemDelegate):
    """
    the delegate class which renders the delegate in den `paint` method.
    """
    
    def __init__(self, parent = None):
        QtGui.QStyledItemDelegate.__init__(self, parent)
       
    def paint(self, painter, option, index):
        if index.column() == 1:
            # FIXME: This looks dirty. There must be a better solution
            progress = int(index.data().toInt()[0])

            progressBarOption = QtGui.QStyleOptionProgressBar()
            progressBarOption.rect = option.rect
            progressBarOption.minimum = 0
            progressBarOption.maximum = 100
            progressBarOption.progress = progress
            progressBarOption.text = unicode("{0}%".format(progress))
            progressBarOption.textVisible = True

            QtGui.QApplication.style().drawControl(QtGui.QStyle.CE_ProgressBar,
                                            progressBarOption, painter, None)
        else:
            QtGui.QItemDelegate.paint(self, painter, option, index) 
        

class TalentWidget(QtGui.QWidget):
    """
    Just a small demo widget with a tree view.
    """

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.ui = uic.loadUi("treeviewdemo.ui", self)
        self.resize(320, 240)
        # Here we define the delegate for a specific column.
        self.tree.setItemDelegateForColumn(1, ProgressDelegate(self))
        self.tree.setModel(create_model(self.tree))


def create_model(parent):
    model = QtGui.QStandardItemModel(parent)
    model.setHorizontalHeaderLabels(["Probe", "Wert"])
    for item in (("Test1", 42), ("Test2", 100), ("Test3", 33)):
        model.appendRow(map(QtGui.QStandardItem, map(unicode, item)))
    return model


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    widget = TalentWidget()
    widget.show()
    sys.exit(app.exec_())
