# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'acq4/devices/MockClamp/devTemplate.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MockClampDevGui(object):
    def setupUi(self, MockClampDevGui):
        MockClampDevGui.setObjectName("MockClampDevGui")
        MockClampDevGui.resize(459, 243)
        self.gridLayout = QtWidgets.QGridLayout(MockClampDevGui)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(MockClampDevGui)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.vcModeRadio = QtWidgets.QRadioButton(self.groupBox_2)
        self.vcModeRadio.setObjectName("vcModeRadio")
        self.horizontalLayout.addWidget(self.vcModeRadio)
        self.i0ModeRadio = QtWidgets.QRadioButton(self.groupBox_2)
        self.i0ModeRadio.setObjectName("i0ModeRadio")
        self.horizontalLayout.addWidget(self.i0ModeRadio)
        self.icModeRadio = QtWidgets.QRadioButton(self.groupBox_2)
        self.icModeRadio.setObjectName("icModeRadio")
        self.horizontalLayout.addWidget(self.icModeRadio)
        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 1, 0, 1, 1)
        self.vcHoldingSpin = SpinBox(self.groupBox_2)
        self.vcHoldingSpin.setObjectName("vcHoldingSpin")
        self.gridLayout_3.addWidget(self.vcHoldingSpin, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 2, 0, 1, 1)
        self.icHoldingSpin = SpinBox(self.groupBox_2)
        self.icHoldingSpin.setObjectName("icHoldingSpin")
        self.gridLayout_3.addWidget(self.icHoldingSpin, 2, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 4, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 3, 0, 1, 1)
        self.pipOffsetSpin = SpinBox(self.groupBox_2)
        self.pipOffsetSpin.setObjectName("pipOffsetSpin")
        self.gridLayout_3.addWidget(self.pipOffsetSpin, 3, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 0, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(MockClampDevGui)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.pipCapSpin = SpinBox(self.groupBox)
        self.pipCapSpin.setObjectName("pipCapSpin")
        self.gridLayout_2.addWidget(self.pipCapSpin, 0, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.pipResSpin = SpinBox(self.groupBox)
        self.pipResSpin.setObjectName("pipResSpin")
        self.gridLayout_2.addWidget(self.pipResSpin, 1, 1, 1, 2)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 2, 0, 1, 1)
        self.pipJunctPotSpin = SpinBox(self.groupBox)
        self.pipJunctPotSpin.setObjectName("pipJunctPotSpin")
        self.gridLayout_2.addWidget(self.pipJunctPotSpin, 2, 1, 1, 2)
        self.pipBathRadio = QtWidgets.QRadioButton(self.groupBox)
        self.pipBathRadio.setObjectName("pipBathRadio")
        self.gridLayout_2.addWidget(self.pipBathRadio, 3, 0, 1, 3)
        self.pipAttachRadio = QtWidgets.QRadioButton(self.groupBox)
        self.pipAttachRadio.setObjectName("pipAttachRadio")
        self.gridLayout_2.addWidget(self.pipAttachRadio, 5, 0, 1, 2)
        self.pipWholeRadio = QtWidgets.QRadioButton(self.groupBox)
        self.pipWholeRadio.setObjectName("pipWholeRadio")
        self.gridLayout_2.addWidget(self.pipWholeRadio, 5, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 6, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout_2.addWidget(self.comboBox, 4, 1, 1, 2)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 4, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 1, 1, 1)

        self.retranslateUi(MockClampDevGui)
        Qt.QMetaObject.connectSlotsByName(MockClampDevGui)

    def retranslateUi(self, MockClampDevGui):
        _translate = Qt.QCoreApplication.translate
        MockClampDevGui.setWindowTitle(_translate("MockClampDevGui", "Form"))
        self.groupBox_2.setTitle(_translate("MockClampDevGui", "Clamp"))
        self.vcModeRadio.setText(_translate("MockClampDevGui", "VC"))
        self.i0ModeRadio.setText(_translate("MockClampDevGui", "I=0"))
        self.icModeRadio.setText(_translate("MockClampDevGui", "IC"))
        self.label_3.setText(_translate("MockClampDevGui", "VC Holding"))
        self.label_4.setText(_translate("MockClampDevGui", "IC Holding"))
        self.label_6.setText(_translate("MockClampDevGui", "Pipette Offset"))
        self.groupBox.setTitle(_translate("MockClampDevGui", "Pipette"))
        self.label.setText(_translate("MockClampDevGui", "Capacitance"))
        self.label_2.setText(_translate("MockClampDevGui", "Resistance"))
        self.label_5.setText(_translate("MockClampDevGui", "Junct. Pot."))
        self.pipBathRadio.setText(_translate("MockClampDevGui", "Bath"))
        self.pipAttachRadio.setText(_translate("MockClampDevGui", "On Cell"))
        self.pipWholeRadio.setText(_translate("MockClampDevGui", "Whole Cell"))
        self.comboBox.setItemText(0, _translate("MockClampDevGui", "HH"))
        self.comboBox.setItemText(1, _translate("MockClampDevGui", "Type II"))
        self.comboBox.setItemText(2, _translate("MockClampDevGui", "Type I"))
        self.label_7.setText(_translate("MockClampDevGui", "Cell"))

from acq4.pyqtgraph import SpinBox
