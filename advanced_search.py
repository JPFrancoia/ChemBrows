#!/usr/bin/python
# -*-coding:Utf-8 -*

import sys
import os
from PyQt4 import QtGui, QtCore


class AdvancedSearch(QtGui.QDialog):

    """Classe pour effectuer les réglages du programme
    par l'utilisateur. On crée une fenêtre secondaire."""

    def __init__(self, parent):

        super(AdvancedSearch, self).__init__(parent)

        print("prout")

    #def connexion(self):

        #"""Get the settings and restore them"""

        #journals_to_parse = self.parent.options.value("journals_to_parse", [])

        ##Check the boxes
        #if not journals_to_parse:
            #return
        #else:
            #for box in self.check_journals:
                #if box.text() in journals_to_parse:
                    #box.setCheckState(2)
                #else:
                    #box.setCheckState(0)


    #def defineSlots(self):

        #"""Establish the slots"""

        ##To close the window and save the settings
        #self.ok_button.clicked.connect(self.saveSettings)

        ##Button "clean database" (erase the unintersting journals from the db)
        ##connected to the method of the main window class
        #self.button_clean_db.clicked.connect(self.parent.cleanDb)


    #def selectBrowser(self):

        #"""Méthode pour retourner le chemin du player"""

        ##path = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home')
        ##self.line_path.setText(path)
        #pass


    #def initUI(self):

        #"""Handles the display"""

        #self.parent.fen_settings = QtGui.QWidget()
        #self.parent.fen_settings.setWindowTitle('Settings')

        #self.ok_button = QtGui.QPushButton("OK", self)

        #self.tabs = QtGui.QTabWidget()

##------------------------ GENERAL TAB ------------------------------------------------

        ##Scroll area for the journals to check
        #self.scroll_check_journals = QtGui.QScrollArea()
        #self.scrolling_check_journals = QtGui.QWidget()
        #self.vbox_check_journals = QtGui.QVBoxLayout()
        #self.scrolling_check_journals.setLayout(self.vbox_check_journals)

        #labels_checkboxes = []

        ##Get labels of the future check boxes of the journals to be parsed
        #for company in os.listdir("./journals"):
            #with open('journals/{0}'.format(company), 'r') as config:
                #labels_checkboxes += [ line.split(" : ")[1] for line in config ]

        #labels_checkboxes.sort()

        ##Build the checkboxes, and put them in a layout
        #for index, label in enumerate(labels_checkboxes):
            #check_box = QtGui.QCheckBox(label)
            #check_box.setCheckState(2)
            #self.check_journals.append(check_box)
            #self.vbox_check_journals.addWidget(check_box)


        #self.scroll_check_journals.setWidget(self.scrolling_check_journals)

        #self.tabs.addTab(self.scroll_check_journals, "Journals")

##------------------------ DATABASE TAB ------------------------------------------------

        #self.widget_database = QtGui.QWidget()
        #self.vbox_database = QtGui.QVBoxLayout()

        #self.button_clean_db = QtGui.QPushButton("Clean database")

        #self.vbox_database.addWidget(self.button_clean_db)
        #self.widget_database.setLayout(self.vbox_database)
        #self.tabs.addTab(self.widget_database, "Database")

##------------------------ ASSEMBLING ------------------------------------------------

        #self.vbox_global = QtGui.QVBoxLayout()
        #self.vbox_global.addWidget(self.tabs)

        #self.vbox_global.addWidget(self.ok_button)

        #self.parent.fen_settings.setLayout(self.vbox_global)
        #self.parent.fen_settings.show()


    #def saveSettings(self):

        #"""Slot to save the settings"""

        #journals_to_parse = []

        #for box in self.check_journals:
            #if box.checkState() == 2:
                #journals_to_parse.append(box.text())

        #if journals_to_parse:
            #self.parent.options.remove("journals_to_parse")
            #self.parent.options.setValue("journals_to_parse", journals_to_parse)
        #else:
            #self.parent.options.remove("journals_to_parse")

        #self.parent.displayTags()
        #self.parent.resetView()

        ##Close the settings window and free the memory
        #self.parent.fen_settings.close()
        #del self.parent.fen_settings
