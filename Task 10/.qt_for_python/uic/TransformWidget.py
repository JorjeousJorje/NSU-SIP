# Form implementation generated from reading ui file 'c:\Users\georg\Desktop\Education\current semester\image-processing\Task 9\ui\TransformWidget.ui'
#
# Created by: PyQt6 UI code generator 6.1.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_TransformWidget(object):
    def setupUi(self, TransformWidget):
        TransformWidget.setObjectName("TransformWidget")
        TransformWidget.resize(392, 184)
        self.verticalLayout = QtWidgets.QVBoxLayout(TransformWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.height_label = QtWidgets.QLabel(TransformWidget)
        self.height_label.setObjectName("height_label")
        self.horizontalLayout_2.addWidget(self.height_label)
        self.height_spin = QtWidgets.QSpinBox(TransformWidget)
        self.height_spin.setMaximum(5000)
        self.height_spin.setObjectName("height_spin")
        self.horizontalLayout_2.addWidget(self.height_spin)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.width_label = QtWidgets.QLabel(TransformWidget)
        self.width_label.setObjectName("width_label")
        self.horizontalLayout.addWidget(self.width_label)
        self.width_spin = QtWidgets.QSpinBox(TransformWidget)
        self.width_spin.setMaximum(5000)
        self.width_spin.setObjectName("width_spin")
        self.horizontalLayout.addWidget(self.width_spin)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.default_shape = QtWidgets.QCheckBox(TransformWidget)
        self.default_shape.setChecked(True)
        self.default_shape.setObjectName("default_shape")
        self.verticalLayout.addWidget(self.default_shape)
        self.refresh_button = QtWidgets.QPushButton(TransformWidget)
        self.refresh_button.setObjectName("refresh_button")
        self.verticalLayout.addWidget(self.refresh_button)
        self.transform_button = QtWidgets.QPushButton(TransformWidget)
        self.transform_button.setObjectName("transform_button")
        self.verticalLayout.addWidget(self.transform_button)
        self.reset_transform_button = QtWidgets.QPushButton(TransformWidget)
        self.reset_transform_button.setObjectName("reset_transform_button")
        self.verticalLayout.addWidget(self.reset_transform_button)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem2)

        self.retranslateUi(TransformWidget)
        self.refresh_button.clicked.connect(TransformWidget.refresh_points)
        self.transform_button.clicked.connect(TransformWidget.transform_image)
        self.reset_transform_button.clicked.connect(TransformWidget.reset_transform)
        QtCore.QMetaObject.connectSlotsByName(TransformWidget)

    def retranslateUi(self, TransformWidget):
        _translate = QtCore.QCoreApplication.translate
        TransformWidget.setWindowTitle(_translate("TransformWidget", "Form"))
        self.height_label.setText(_translate("TransformWidget", "Height"))
        self.width_label.setText(_translate("TransformWidget", "Width"))
        self.default_shape.setText(_translate("TransformWidget", "Use Image Shape"))
        self.refresh_button.setText(_translate("TransformWidget", "Refresh points"))
        self.transform_button.setText(_translate("TransformWidget", "Transform"))
        self.reset_transform_button.setText(_translate("TransformWidget", "Reset Transform"))
