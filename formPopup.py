#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""PyQt4 port of the layouts/basiclayout example from Qt v4.x"""

from PySide import QtCore, QtGui


class Dialog(QtGui.QDialog):

    def __init__(self):
        super(Dialog, self).__init__()

        self.createFormGroupBox()

        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Basic Layouts")

    def createFormGroupBox(self):
        self.formGroupBox = QtGui.QGroupBox("INSERIR CHAMADO:")
        layout = QtGui.QFormLayout()
        layout.addRow(QtGui.QLabel("Numero chamado:"), QtGui.QLineEdit())
        layout.addRow(QtGui.QLabel("Empresa:"), QtGui.QLineEdit())
        layout.addRow(QtGui.QLabel("Tempo desenvolvimento:"), QtGui.QSpinBox())
        layout.addRow(QtGui.QLabel("Tipo do chamado:"), QtGui.QLineEdit())
        self.formGroupBox.setLayout(layout)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    dialog = Dialog()
    sys.exit(dialog.exec_())
