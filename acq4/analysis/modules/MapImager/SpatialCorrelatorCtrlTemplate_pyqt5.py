# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'acq4/analysis/modules/MapImager/SpatialCorrelatorCtrlTemplate.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(273, 234)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spontSpin = SpinBox(Form)
        self.spontSpin.setSuffix("")
        self.spontSpin.setObjectName("spontSpin")
        self.horizontalLayout.addWidget(self.spontSpin)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.deltaTSpin = SpinBox(Form)
        self.deltaTSpin.setObjectName("deltaTSpin")
        self.horizontalLayout_2.addWidget(self.deltaTSpin)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.radiusSpin = SpinBox(Form)
        self.radiusSpin.setObjectName("radiusSpin")
        self.horizontalLayout_3.addWidget(self.radiusSpin)
        self.gridLayout.addLayout(self.horizontalLayout_3, 3, 0, 1, 2)
        self.disableChk = QtWidgets.QCheckBox(Form)
        self.disableChk.setObjectName("disableChk")
        self.gridLayout.addWidget(self.disableChk, 6, 0, 1, 1)
        self.processBtn = QtWidgets.QPushButton(Form)
        self.processBtn.setObjectName("processBtn")
        self.gridLayout.addWidget(self.processBtn, 6, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setContentsMargins(3, 3, 3, 3)
        self.gridLayout_2.setSpacing(3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.probabilityRadio = QtWidgets.QRadioButton(self.groupBox)
        self.probabilityRadio.setChecked(True)
        self.probabilityRadio.setObjectName("probabilityRadio")
        self.gridLayout_2.addWidget(self.probabilityRadio, 0, 0, 1, 2)
        self.thresholdSpin = SpinBox(self.groupBox)
        self.thresholdSpin.setEnabled(True)
        self.thresholdSpin.setObjectName("thresholdSpin")
        self.gridLayout_2.addWidget(self.thresholdSpin, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setAlignment(Qt.Qt.AlignRight|Qt.Qt.AlignTrailing|Qt.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)
        self.thresholdRadio = QtWidgets.QRadioButton(self.groupBox)
        self.thresholdRadio.setObjectName("thresholdRadio")
        self.gridLayout_2.addWidget(self.thresholdRadio, 1, 0, 1, 2)
        self.gridLayout.addWidget(self.groupBox, 5, 0, 1, 2)
        self.eventCombo = ComboBox(Form)
        self.eventCombo.setObjectName("eventCombo")
        self.gridLayout.addWidget(self.eventCombo, 0, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)

        self.retranslateUi(Form)
        Qt.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = Qt.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Spontaneous Event Rate:"))
        self.label_2.setText(_translate("Form", "Post-stimulus time window:"))
        self.label_3.setText(_translate("Form", "Correlation Radius:"))
        self.disableChk.setText(_translate("Form", "Disable"))
        self.processBtn.setText(_translate("Form", "re-Process"))
        self.groupBox.setTitle(_translate("Form", "Output data:"))
        self.probabilityRadio.setText(_translate("Form", "Probability values (float)"))
        self.label_4.setText(_translate("Form", "Threshold:"))
        self.thresholdRadio.setText(_translate("Form", "Spots that cross threshold (boolean)"))
        self.label_5.setText(_translate("Form", "Event Parameter to use:"))

from acq4.pyqtgraph.widgets.ComboBox import ComboBox
from acq4.pyqtgraph.widgets.SpinBox import SpinBox
