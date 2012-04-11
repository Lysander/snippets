#!/usr/bin/env python

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
    ~~~~~~~~~~~~~~~~~
    signal_mapping.py
    ~~~~~~~~~~~~~~~~~
    
    Simple demo that shows how to add additional objects to a Qt4 signal-slot
    connection using `partial`.
    
    .. moduleauthor:: Christian Hausknecht <christian.hausknecht@gmx.de>
"""

import sys
from PyQt4 import QtGui, uic, QtCore
from functools import partial


PROPERTIES = ["MU", "KL", "IN"]


class SignalMapper(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        form = QtGui.QFormLayout(self)
        for tag in PROPERTIES:
            spin = QtGui.QSpinBox(self)
            form.addRow(tag, spin)
            # here the "magic" happens.
            spin.valueChanged[int].connect(partial(self.slot_show, spin, tag))
        self.info = QtGui.QLabel(self)
        form.addRow(self.info)

    def slot_show(self, spin, tag, value):
          self.info.setText("{0} changed to {1}".format(tag, value))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    widget = SignalMapper()
    widget.show()
    sys.exit(app.exec_())
