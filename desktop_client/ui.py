# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(408, 563)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(12, 12, 12, 12)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.FrameRokmaskin = QtWidgets.QFrame(self.centralwidget)
        self.FrameRokmaskin.setFrameShape(QtWidgets.QFrame.Box)
        self.FrameRokmaskin.setFrameShadow(QtWidgets.QFrame.Plain)
        self.FrameRokmaskin.setLineWidth(1)
        self.FrameRokmaskin.setObjectName("FrameRokmaskin")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.FrameRokmaskin)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.b = QtWidgets.QLabel(self.FrameRokmaskin)
        self.b.setObjectName("b")
        self.verticalLayout_4.addWidget(self.b, 0, QtCore.Qt.AlignHCenter)
        self.power = QtWidgets.QCheckBox(self.FrameRokmaskin)
        self.power.setEnabled(False)
        self.power.setObjectName("power")
        self.verticalLayout_4.addWidget(self.power, 0, QtCore.Qt.AlignHCenter)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 2, 1, 1, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.btn = QtWidgets.QPushButton(self.FrameRokmaskin)
        self.btn.setCheckable(True)
        self.btn.setAutoExclusive(False)
        self.btn.setFlat(True)
        self.btn.setObjectName("btn")
        self.horizontalLayout_7.addWidget(self.btn)
        self.btn2 = QtWidgets.QPushButton(self.FrameRokmaskin)
        self.btn2.setCheckable(True)
        self.btn2.setAutoExclusive(False)
        self.btn2.setFlat(True)
        self.btn2.setObjectName("btn2")
        self.horizontalLayout_7.addWidget(self.btn2)
        self.gridLayout.addLayout(self.horizontalLayout_7, 1, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 1, 2, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem4)
        self.colorbtn = QtWidgets.QPushButton(self.FrameRokmaskin)
        self.colorbtn.setObjectName("colorbtn")
        self.horizontalLayout_8.addWidget(self.colorbtn)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem5)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem6)
        self.label = QtWidgets.QLabel(self.FrameRokmaskin)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.strobeOffBtn = QtWidgets.QPushButton(self.FrameRokmaskin)
        self.strobeOffBtn.setCheckable(True)
        self.strobeOffBtn.setChecked(True)
        self.strobeOffBtn.setAutoExclusive(True)
        self.strobeOffBtn.setObjectName("strobeOffBtn")
        self.horizontalLayout.addWidget(self.strobeOffBtn)
        self.strobeOnBtn = QtWidgets.QPushButton(self.FrameRokmaskin)
        self.strobeOnBtn.setCheckable(True)
        self.strobeOnBtn.setAutoExclusive(True)
        self.strobeOnBtn.setObjectName("strobeOnBtn")
        self.horizontalLayout.addWidget(self.strobeOnBtn)
        self.strobePulseBtn = QtWidgets.QPushButton(self.FrameRokmaskin)
        self.strobePulseBtn.setCheckable(True)
        self.strobePulseBtn.setAutoExclusive(True)
        self.strobePulseBtn.setObjectName("strobePulseBtn")
        self.horizontalLayout.addWidget(self.strobePulseBtn)
        self.strobeRandomBtn = QtWidgets.QPushButton(self.FrameRokmaskin)
        self.strobeRandomBtn.setCheckable(True)
        self.strobeRandomBtn.setAutoExclusive(True)
        self.strobeRandomBtn.setObjectName("strobeRandomBtn")
        self.horizontalLayout.addWidget(self.strobeRandomBtn)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.FrameRokmaskin)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.strobeslider = QtWidgets.QSlider(self.FrameRokmaskin)
        self.strobeslider.setOrientation(QtCore.Qt.Horizontal)
        self.strobeslider.setObjectName("strobeslider")
        self.horizontalLayout_3.addWidget(self.strobeslider)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.gridLayout_2.addWidget(self.FrameRokmaskin, 1, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 3, 0, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem7, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.FrameLampa = QtWidgets.QFrame(self.centralwidget)
        self.FrameLampa.setFrameShape(QtWidgets.QFrame.Box)
        self.FrameLampa.setObjectName("FrameLampa")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.FrameLampa)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.floodlightOff = QtWidgets.QPushButton(self.FrameLampa)
        self.floodlightOff.setCheckable(True)
        self.floodlightOff.setAutoExclusive(True)
        self.floodlightOff.setObjectName("floodlightOff")
        self.horizontalLayout_2.addWidget(self.floodlightOff)
        self.floodlightOn = QtWidgets.QPushButton(self.FrameLampa)
        self.floodlightOn.setCheckable(True)
        self.floodlightOn.setAutoExclusive(True)
        self.floodlightOn.setObjectName("floodlightOn")
        self.horizontalLayout_2.addWidget(self.floodlightOn)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.floodlightSlow = QtWidgets.QPushButton(self.FrameLampa)
        self.floodlightSlow.setCheckable(True)
        self.floodlightSlow.setAutoExclusive(True)
        self.floodlightSlow.setObjectName("floodlightSlow")
        self.horizontalLayout_5.addWidget(self.floodlightSlow)
        self.floodlightFast = QtWidgets.QPushButton(self.FrameLampa)
        self.floodlightFast.setCheckable(True)
        self.floodlightFast.setAutoExclusive(True)
        self.floodlightFast.setObjectName("floodlightFast")
        self.horizontalLayout_5.addWidget(self.floodlightFast)
        self.floodlightUltra = QtWidgets.QPushButton(self.FrameLampa)
        self.floodlightUltra.setCheckable(True)
        self.floodlightUltra.setAutoExclusive(True)
        self.floodlightUltra.setObjectName("floodlightUltra")
        self.horizontalLayout_5.addWidget(self.floodlightUltra)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.gridLayout_2.addWidget(self.FrameLampa, 5, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ADJ Fog Fury Jett"))
        self.b.setText(_translate("MainWindow", "Ansluter..."))
        self.power.setText(_translate("MainWindow", "Ström på"))
        self.btn.setText(_translate("MainWindow", "KÖR FÄRG"))
        self.btn2.setText(_translate("MainWindow", "KÖR ELD"))
        self.colorbtn.setText(_translate("MainWindow", "Välj färg"))
        self.label.setText(_translate("MainWindow", "Stroboskopkontroll"))
        self.strobeOffBtn.setText(_translate("MainWindow", "Av"))
        self.strobeOnBtn.setText(_translate("MainWindow", "Strobo"))
        self.strobePulseBtn.setText(_translate("MainWindow", "Puls"))
        self.strobeRandomBtn.setText(_translate("MainWindow", "Slumpmässig"))
        self.label_2.setText(_translate("MainWindow", "Hastighet"))
        self.label_5.setText(_translate("MainWindow", "Lampa"))
        self.label_4.setText(_translate("MainWindow", "Rökmaskin"))
        self.floodlightOff.setText(_translate("MainWindow", "Släck"))
        self.floodlightOn.setText(_translate("MainWindow", "Tänd"))
        self.floodlightSlow.setText(_translate("MainWindow", "Strobo Slow"))
        self.floodlightFast.setText(_translate("MainWindow", "Strobo Fast"))
        self.floodlightUltra.setText(_translate("MainWindow", "Strobo Ultra"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
