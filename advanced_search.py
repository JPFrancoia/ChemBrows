#!/usr/bin/python
# -*-coding:Utf-8 -*

import sys
# import os
from PyQt4 import QtGui, QtCore
from log import MyLog

import functions


class AdvancedSearch(QtGui.QDialog):

    """Class to perform advanced searches"""

    def __init__(self, parent):

        super(AdvancedSearch, self).__init__(parent)

        self.parent = parent

        # Condition to use a specific logger if
        # module started in standalone
        if type(parent) is QtGui.QWidget:
            self.logger = MyLog()
            self.test = True
        else:
            self.logger = self.parent.l
            self.test = False

        self.options = QtCore.QSettings("searches.ini", QtCore.QSettings.IniFormat)

        # List to store the lineEdit, with the value of
        # the search fields
        self.fields_list = []

        self.initUI()
        self.defineSlots()
        self.restoreSettings()


    def restoreSettings(self):

        """Restore the right number of tabs"""

        for query in self.options.childGroups():
            self.tabs.addTab(self.createForm(), query)


    def defineSlots(self):

        """Establish the slots"""

        self.button_search.clicked.connect(self.search)

        self.button_search_and_save.clicked.connect(self.search)

        self.tabs.currentChanged.connect(self.tabChanged)

        self.button_delete_search.clicked.connect(self.deleteSearch)


    def deleteSearch(self):

        """Slot to delete a query"""

        # Get the title of the search, get the group with
        # the same name in searches.ini, and clear the group
        tab_title = self.tabs.tabText(self.tabs.currentIndex())
        self.options.beginGroup(tab_title)
        # Re-initialize the keys
        self.options.remove("")
        self.options.endGroup()

        self.tabs.removeTab(self.tabs.currentIndex())

        if not self.test:
            for index in range(self.parent.onglets.count()):
                if self.parent.onglets.tabText(index) == tab_title:
                    self.parent.onglets.removeTab(index)
                    self.parent.onglets.setCurrentIndex(0)
                    break


    def buildSearch(self):

        """Build the query"""

        # Get all the lineEdit from the current tab
        lines = self.tabs.currentWidget().findChildren(QtGui.QLineEdit)

        # name_search = lines[0].text()
        topic_entries = [line.text() for line in lines[1:4]]
        author_entries = [line.text() for line in lines[4:8]]

        if topic_entries == [''] * 3 and author_entries == [''] * 3:
            return False

        base = "SELECT * FROM papers WHERE "

        first = True

        # TOPIC, AND condition
        if topic_entries[0]:
            first = False

            words = [word.lstrip().rstrip() for word in topic_entries[0].split(",")]
            words = [functions.queryString(word) for word in words]

            for word in words:
                if word is words[0]:
                    base += "topic_simple LIKE '{0}'".format(word)
                else:
                    base += " AND topic_simple LIKE '{0}'".format(word)

        # TOPIC, OR condition
        if topic_entries[1]:
            words = [word.lstrip().rstrip() for word in topic_entries[1].split(",")]
            words = [functions.queryString(word) for word in words]

            if first:
                first = False
                base += "topic_simple LIKE '{0}'".format(words[0])

                for word in words[1:]:
                    base += " OR topic_simple LIKE '{0}'".format(word)
            else:
                for word in words:
                    base += " OR topic_simple LIKE '{0}'".format(word)

        # TOPIC, NOT condition
        if topic_entries[2]:
            words = [word.lstrip().rstrip() for word in topic_entries[2].split(",")]
            words = [functions.queryString(word) for word in words]

            if first:
                first = False
                base += "topic_simple NOT LIKE '{0}'".format(words[0])

                for word in words[1:]:
                    base += " AND topic_simple NOT LIKE '{0}'".format(word)
            else:
                for word in words:
                    base += " AND topic_simple NOT LIKE '{0}'".format(word)

        # AUTHOR, AND condition
        if author_entries[0]:
            words = [word.lstrip().rstrip() for word in author_entries[0].split(",")]
            words = [functions.queryString(word) for word in words]

            if first:
                first = False
                base += "' ' || replace(authors, ',', ' ') || ' ' LIKE '{0}'".format(words[0])

                for word in words[1:]:
                    base += " AND ' ' || replace(authors, ',', ' ') || ' ' LIKE '{0}'".format(word)
            else:
                for word in words:
                    base += " AND ' ' || replace(authors, ',', ' ') || ' ' LIKE '{0}'".format(word)

        # AUTHOR, OR condition
        if author_entries[1]:
            words = [word.lstrip().rstrip() for word in author_entries[1].split(",")]
            words = [functions.queryString(word) for word in words]

            if first:
                first = False
                base += "' ' || replace(authors, ',', ' ') || ' ' LIKE '{0}'".format(words[0])

                for word in words[1:]:
                    base += " OR ' ' || replace(authors, ',', ' ') || ' ' LIKE '{0}'".format(word)
            else:
                for word in words:
                    base += " OR ' ' || replace(authors, ',', ' ') || ' ' LIKE '{0}'".format(word)

        # AUTHOR, NOT condition
        if author_entries[2]:
            words = [word.lstrip().rstrip() for word in author_entries[2].split(",")]
            words = [functions.queryString(word) for word in words]

            if first:
                first = False
                base += "' ' || replace(authors, ',', ' ') || ' ' NOT LIKE '{0}'".format(words[0])

                for word in words[1:]:
                    base += " AND ' ' || replace(authors, ',', ' ') || ' ' NOT LIKE '{0}'".format(word)
            else:
                for word in words:
                    base += " AND ' ' || replace(authors, ',', ' ') || ' ' NOT LIKE '{0}'".format(word)

        return base


    def tabChanged(self):

        """Method called when tab is changed.
        Fill the fields with the good data"""

        # Get the current tab number
        index = self.tabs.currentIndex()
        tab_title = self.tabs.tabText(index)

        # Get the lineEdit objects of the current search tab displayed
        lines = self.tabs.currentWidget().findChildren(QtGui.QLineEdit)
        name_search = lines[0]
        topic_entries = [line for line in lines[1:4]]
        author_entries = [line for line in lines[4:8]]

        if index is not 0:

            name_search.setEnabled(False)

            # Change the buttons at the button if the tab is
            # a tab dedicated to search edition
            self.button_delete_search.show()
            self.button_search.hide()

            # Fill the lineEdit with the data
            name_search.setText(tab_title)

            topic_entries_options = self.options.value("{0}/topic_entries".format(tab_title), None)
            if topic_entries_options is not None:
                topic_entries = [line.setText(value) for line, value in zip(topic_entries, topic_entries_options)]
            author_entries_options = self.options.value("{0}/author_entries".format(tab_title), None)
            if author_entries_options is not None:
                author_entries = [line.setText(value) for line, value in zip(author_entries, author_entries_options)]

        else:
            self.button_delete_search.hide()
            self.button_search.show()


    def search(self):

        """Slot to save a query"""

        # TODO:
            # updater la vue du parent

        if self.sender() == self.button_search:
            save = False
        else:
            save = True

        lines = self.tabs.currentWidget().findChildren(QtGui.QLineEdit)

        # Get the name of the current tab. Used to determine if the current
        # tab is the "new query" tab
        tab_title = self.tabs.tabText(self.tabs.currentIndex())

        topic_entries = [line.text() for line in lines[1:4]]
        author_entries = [line.text() for line in lines[4:8]]

        # TODO: ajouter une boite de dialogue pour le nom
        # si user pushed saved
        # Get the name of the search
        name_search = lines[0].text()

        # Build the query string
        base = self.buildSearch()

        if not base:
            return

        if tab_title == "New query":

            # The search is about to be saved
            if save:
                if name_search in self.options.childGroups():
                    # TODO:
                        # afficher une dialog box d'erreur pr le nom
                    self.logger.debug("This search name is already used")
                    return
                else:
                    group_name = name_search
                    self.tabs.addTab(self.createForm(), name_search)

                    if not self.test:
                        self.parent.createSearchTab(name_search, base)

                    # Clear the fields when perform search
                    for line in lines:
                        line.clear()
            else:
                # Perform a simple search, in the first tab
                self.parent.simpleQuery(base)

        else:
            group_name = tab_title

            if not self.test:
                self.parent.createSearchTab(name_search, base, update=True)

        if save:
            self.logger.debug("Saving the search")

            self.options.beginGroup(group_name)

            # Re-initialize the keys
            self.options.remove("")
            # self.options.setValue("name_search", name_search)
            if topic_entries != [''] * 3:
                self.options.setValue("topic_entries", topic_entries)
            if author_entries != [''] * 3:
                self.options.setValue("author_entries", author_entries)
            if base:
                self.options.setValue("sql_query", base)
            self.options.endGroup()


    def createForm(self):

# ------------------------ NEW SEARCH TAB -------------------------------------

        # Main widget of the tab, with a grid layout
        widget_query = QtGui.QWidget()

        vbox_query = QtGui.QVBoxLayout()
        widget_query.setLayout(vbox_query)


        # Line for the search name, to save
        # Create a hbox to put the label and the line
        hbox_name = QtGui.QHBoxLayout()
        label_name = QtGui.QLabel("Search name : ")
        line_name = QtGui.QLineEdit()
        hbox_name.addWidget(label_name)
        hbox_name.addWidget(line_name)

        # add the label and the line to the
        # local vbox
        vbox_query.addLayout(hbox_name)

        vbox_query.addStretch(1)

        # ------------- TOPIC ----------------------------------
        # Create a groupbox for the topic
        group_topic = QtGui.QGroupBox("Topic")
        grid_topic = QtGui.QGridLayout()
        group_topic.setLayout(grid_topic)


        # Add the topic groupbox to the global vbox
        vbox_query.addWidget(group_topic)


        # Create 3 lines, with their label: AND, OR, NOT
        label_topic_and = QtGui.QLabel("AND:")
        line_topic_and = QtGui.QLineEdit()

        label_topic_or = QtGui.QLabel("OR:")
        line_topic_or = QtGui.QLineEdit()

        label_topic_not = QtGui.QLabel("NOT:")
        line_topic_not = QtGui.QLineEdit()

        # Organize the lines and the lab within the grid
        grid_topic.addWidget(label_topic_and, 0, 0)
        grid_topic.addWidget(line_topic_and, 0, 1, 1, 3)
        grid_topic.addWidget(label_topic_or, 1, 0)
        grid_topic.addWidget(line_topic_or, 1, 1, 1, 3)
        grid_topic.addWidget(label_topic_not, 2, 0)
        grid_topic.addWidget(line_topic_not, 2, 1, 1, 3)

        vbox_query.addStretch(1)


        # ------------- AUTHORS ----------------------------------
        # Create a groupbox for the authors
        group_author = QtGui.QGroupBox("Author(s)")
        grid_author = QtGui.QGridLayout()
        group_author.setLayout(grid_author)


        # Add the author groupbox to the global vbox
        vbox_query.addWidget(group_author)


        label_author_and = QtGui.QLabel("AND:")
        line_author_and = QtGui.QLineEdit()

        label_author_or = QtGui.QLabel("OR:")
        line_author_or = QtGui.QLineEdit()

        label_author_not = QtGui.QLabel("NOT:")
        line_author_not = QtGui.QLineEdit()

        grid_author.addWidget(label_author_and, 0, 0)
        grid_author.addWidget(line_author_and, 0, 1, 1, 3)
        grid_author.addWidget(label_author_or, 1, 0)
        grid_author.addWidget(line_author_or, 1, 1, 1, 3)
        grid_author.addWidget(label_author_not, 2, 0)
        grid_author.addWidget(line_author_not, 2, 1, 1, 3)

        vbox_query.addStretch(1)

        return widget_query


    def initUI(self):

        """Handles the display"""

        self.parent.window_search = QtGui.QWidget()
        self.parent.window_search.setWindowTitle('Advanced Search')


        self.tabs = QtGui.QTabWidget()

        query = self.createForm()

        self.tabs.addTab(query, "New query")


# ------------------------ BUTTONS -----------------------------------------

        self.button_search = QtGui.QPushButton("Search !", self)
        self.button_delete_search = QtGui.QPushButton("Delete search", self)
        self.button_search_and_save = QtGui.QPushButton("Save", self)

# ------------------------ ASSEMBLING -----------------------------------------

        # Create a global vbox, and stack the main widget + the search button
        self.vbox_global = QtGui.QVBoxLayout()
        self.vbox_global.addWidget(self.tabs)

        self.vbox_global.addWidget(self.button_search)
        self.vbox_global.addWidget(self.button_delete_search)
        self.button_delete_search.hide()
        self.vbox_global.addWidget(self.button_search_and_save)

        self.parent.window_search.setLayout(self.vbox_global)
        self.parent.window_search.show()


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    parent = QtGui.QWidget()
    obj = AdvancedSearch(parent)
    sys.exit(app.exec_())
