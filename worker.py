#!/usr/bin/python
# -*-coding:Utf-8 -*

from PyQt4 import QtGui, QtSql, QtCore
import parse


class Worker(QtCore.QThread):

    """Subclassing the class in order to provide a thread.
    The thread is used to parse the RSS flux, in background. The
    main UI remains functional"""

    #Explique comment faire une classe de thread pr ne pas bloquer la GUI principale
    #http://stackoverflow.com/questions/6783194/background-thread-with-qthread-in-pyqt


    def __init__(self, window):

        QtCore.QThread.__init__(self, window)

        self.exiting = False

        #Get the parent window
        self.window = window

        self.window.l.debug("Starting parsing of the new articles")


    def render(self):

        """Give the parameter to this function, if needed"""
        self.start()


    def __del__(self):
    
        self.exiting = True
        self.wait()


    def run(self):

        """Main function. Starts the real business"""

        parse.parse(self.window.l)
