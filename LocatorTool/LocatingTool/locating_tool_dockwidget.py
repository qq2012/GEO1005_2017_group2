# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LocatingToolDockWidget
                                 A QGIS plugin
 Finds suitable areas for a mobile control center
                             -------------------
        begin                : 2017-12-15
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Group 2
        email                : group2@group2company.enterprise
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal

from . import utility_functions as uf

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'locating_tool_dockwidget_base.ui'))


class LocatingToolDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, iface, parent=None):
        """Constructor."""
        super(LocatingToolDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        #define globals
        self.iface = iface
        self.canvas = self.iface.mapCanvas()

        # set up GUI operation signals
        # data
        # self.iface.projectRead.connect(self.updateLayers)
        # self.iface.newProjectCreated.connect(self.updateLayers)
        # self.iface.legendInterface().itemRemoved.connect(self.updateLayers)
        # self.iface.legendInterface().itemAdded.connect(self.updateLayers)

        self.openFireButton.clicked.connect(self.openFire)


    def openFire(self,filename=""):
        scenario_open = False
        # scenario_file = os.path.join(u'/Users/jorge/github/GEO1005','sample_data','time_test.qgs')
        # check if file exists
        # if os.path.isfile(scenario_file):
        #    self.iface.addProject(scenario_file)
        #    scenario_open = True

        last_dir = uf.getLastDir("SDSS")
        new_file = QtGui.QFileDialog.getOpenFileName(self, "", last_dir, "(*.qgs)")
        if new_file:
            self.iface.addProject(unicode(new_file))
            scenario_open = True
        if scenario_open:
            self.updateLayers()


    def closeEvent(self, event):
        # disconnect interface signals
        try:
            self.iface.projectRead.disconnect(self.updateLayers)
            self.iface.newProjectCreated.disconnect(self.updateLayers)
            self.iface.legendInterface().itemRemoved.disconnect(self.updateLayers)
            self.iface.legendInterface().itemAdded.disconnect(self.updateLayers)
        except:
            pass

        self.closingPlugin.emit()
        event.accept()

