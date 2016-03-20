#!/usr/bin/python
# coding: utf-8


import sys
import os
from PyQt4 import QtGui, QtCore


class Settings(QtGui.QDialog):

    """Class for the program settings, modifiable by the user.
    Creates a child window"""

    def __init__(self, parent):

        super(Settings, self).__init__(parent)

        self.parent = parent

        # TEST
        try:
            self.options = self.parent.options
            self.test = False
        except AttributeError:
            self.options = QtCore.QSettings("debug/options.ini", QtCore.QSettings.IniFormat)
            self.test = True

        self.check_journals = []

        self.initUI()
        self.connexion()
        self.defineSlots()


    def connexion(self):

        """Get the settings and restore them"""

        journals_to_parse = self.options.value("journals_to_parse", [])

        # Check the boxes
        if not journals_to_parse:
            return
        else:
            for box in self.check_journals:
                if box.text() in journals_to_parse:
                    box.setCheckState(2)
                else:
                    box.setCheckState(0)


    def defineSlots(self):

        """Establish the slots"""

        # To close the window and save the settings
        self.ok_button.clicked.connect(self.saveSettings)

        # Checkbox to select/unselect all the journals
        self.box_select_all.stateChanged.connect(self.selectUnselectAll)

        # Button "clean database" (erase the unintersting journals from the db)
        # connected to the method of the main window class
        # TO COMMENT to run the module standalone
        if not self.test:
            self.button_clean_db.clicked.connect(self.parent.cleanDb)


    def selectUnselectAll(self, state):

        """Select or unselect all the journals"""

        for box in self.check_journals:
            box.setCheckState(state)


    def initUI(self):

        """Handles the display"""

        self.parent.fen_settings = QtGui.QWidget()
        self.parent.fen_settings.setWindowTitle('Settings')

        self.ok_button = QtGui.QPushButton("OK", self)

        self.tabs = QtGui.QTabWidget()

# ------------------------ GENERAL TAB ------------------------------------------------

        # Scroll area for the journals to check
        self.scroll_check_journals = QtGui.QScrollArea()
        self.scrolling_check_journals = QtGui.QWidget()
        self.vbox_check_journals = QtGui.QVBoxLayout()
        self.scrolling_check_journals.setLayout(self.vbox_check_journals)

        labels_checkboxes = []

        # Get labels of the future check boxes of the journals to be parsed
        for company in os.listdir(os.path.join(self.parent.resource_dir, "journals")):
            with open(os.path.join(self.parent.resource_dir, 'journals/{0}'.format(company)), 'r') as config:
                labels_checkboxes += [line.split(" : ")[1] for line in config]

        labels_checkboxes.sort()

        self.box_select_all = QtGui.QCheckBox("Select all")
        self.box_select_all.setCheckState(0)
        self.vbox_check_journals.addWidget(self.box_select_all)

        # Build the checkboxes, and put them in a layout
        for index, label in enumerate(labels_checkboxes):
            check_box = QtGui.QCheckBox(label)
            check_box.setCheckState(2)
            self.check_journals.append(check_box)
            self.vbox_check_journals.addWidget(check_box)


        self.scroll_check_journals.setWidget(self.scrolling_check_journals)

        self.tabs.addTab(self.scroll_check_journals, "Journals")

# ------------------------ DATABASE TAB ------------------------------------------------

        self.widget_database = QtGui.QWidget()
        self.vbox_database = QtGui.QVBoxLayout()

        self.button_clean_db = QtGui.QPushButton("Clean database")

        self.vbox_database.addWidget(self.button_clean_db)
        self.widget_database.setLayout(self.vbox_database)
        self.tabs.addTab(self.widget_database, "Database")

# ------------------------ ASSEMBLING ------------------------------------------------

        self.vbox_global = QtGui.QVBoxLayout()
        self.vbox_global.addWidget(self.tabs)

        self.vbox_global.addWidget(self.ok_button)

        self.parent.fen_settings.setLayout(self.vbox_global)
        self.parent.fen_settings.show()


    def saveSettings(self):

        """Slot to save the settings"""

        journals_to_parse = []

        for box in self.check_journals:
            if box.text() != "Select all":
                if box.checkState() == 2:
                    journals_to_parse.append(box.text())

        if journals_to_parse:
            self.options.remove("journals_to_parse")
            self.options.setValue("journals_to_parse", journals_to_parse)
        else:
            self.options.remove("journals_to_parse")

        self.parent.model.submitAll()
        self.parent.displayTags()
        self.parent.resetView()

        # Close the settings window and free the memory
        self.parent.fen_settings.close()
        del self.parent.fen_settings


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    parent = QtGui.QWidget()
    obj = Settings(parent)
    sys.exit(app.exec_())
