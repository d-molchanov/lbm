# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'beam_profiler_widget_2.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QComboBox,
    QDoubleSpinBox, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QSplitter, QTableWidgetItem, QVBoxLayout,
    QWidget)

from ..utils.custom_graphics_view import CustomGraphicsView
from laser_beam_measurements.widgets.utils.parameters_table_widget import ParametersTableWidget
from pyqtgraph import PlotWidget

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(983, 739)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.splitter_4 = QSplitter(Form)
        self.splitter_4.setObjectName(u"splitter_4")
        self.splitter_4.setOrientation(Qt.Orientation.Horizontal)
        self.widget = QWidget(self.splitter_4)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_4 = QVBoxLayout(self.widget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.groupBoxCursors = QGroupBox(self.widget)
        self.groupBoxCursors.setObjectName(u"groupBoxCursors")
        self.verticalLayout_7 = QVBoxLayout(self.groupBoxCursors)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.groupBoxMode = QGroupBox(self.groupBoxCursors)
        self.groupBoxMode.setObjectName(u"groupBoxMode")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxMode.sizePolicy().hasHeightForWidth())
        self.groupBoxMode.setSizePolicy(sizePolicy)
        self.groupBoxMode.setMinimumSize(QSize(120, 48))
        self.comboBoxMode = QComboBox(self.groupBoxMode)
        self.comboBoxMode.setObjectName(u"comboBoxMode")
        self.comboBoxMode.setGeometry(QRect(11, 20, 111, 22))

        self.verticalLayout_7.addWidget(self.groupBoxMode)

        self.groupBoxTop = QGroupBox(self.groupBoxCursors)
        self.groupBoxTop.setObjectName(u"groupBoxTop")
        sizePolicy.setHeightForWidth(self.groupBoxTop.sizePolicy().hasHeightForWidth())
        self.groupBoxTop.setSizePolicy(sizePolicy)
        self.groupBoxTop.setMinimumSize(QSize(120, 48))
        self.doubleSpinBoxTop = QDoubleSpinBox(self.groupBoxTop)
        self.doubleSpinBoxTop.setObjectName(u"doubleSpinBoxTop")
        self.doubleSpinBoxTop.setGeometry(QRect(10, 20, 88, 24))
        self.doubleSpinBoxTop.setMinimum(-10000.000000000000000)
        self.doubleSpinBoxTop.setMaximum(10000.000000000000000)
        self.doubleSpinBoxTop.setStepType(QAbstractSpinBox.StepType.AdaptiveDecimalStepType)

        self.verticalLayout_7.addWidget(self.groupBoxTop)

        self.groupBoxBottom = QGroupBox(self.groupBoxCursors)
        self.groupBoxBottom.setObjectName(u"groupBoxBottom")
        sizePolicy.setHeightForWidth(self.groupBoxBottom.sizePolicy().hasHeightForWidth())
        self.groupBoxBottom.setSizePolicy(sizePolicy)
        self.groupBoxBottom.setMinimumSize(QSize(120, 48))
        self.doubleSpinBoxBottom = QDoubleSpinBox(self.groupBoxBottom)
        self.doubleSpinBoxBottom.setObjectName(u"doubleSpinBoxBottom")
        self.doubleSpinBoxBottom.setGeometry(QRect(10, 20, 88, 24))
        self.doubleSpinBoxBottom.setMinimum(-10000.000000000000000)
        self.doubleSpinBoxBottom.setMaximum(10000.000000000000000)
        self.doubleSpinBoxBottom.setStepType(QAbstractSpinBox.StepType.AdaptiveDecimalStepType)

        self.verticalLayout_7.addWidget(self.groupBoxBottom)

        self.groupBoxContrast = QGroupBox(self.groupBoxCursors)
        self.groupBoxContrast.setObjectName(u"groupBoxContrast")
        sizePolicy.setHeightForWidth(self.groupBoxContrast.sizePolicy().hasHeightForWidth())
        self.groupBoxContrast.setSizePolicy(sizePolicy)
        self.groupBoxContrast.setMinimumSize(QSize(120, 48))
        self.lineEditContrast = QLineEdit(self.groupBoxContrast)
        self.lineEditContrast.setObjectName(u"lineEditContrast")
        self.lineEditContrast.setGeometry(QRect(10, 20, 113, 22))
        self.lineEditContrast.setReadOnly(True)

        self.verticalLayout_7.addWidget(self.groupBoxContrast)


        self.verticalLayout_4.addWidget(self.groupBoxCursors)

        self.groupBox = QGroupBox(self.widget)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy1)
        self.groupBox.setFlat(False)
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.enable_check_box = QCheckBox(self.groupBox)
        self.enable_check_box.setObjectName(u"enable_check_box")

        self.verticalLayout.addWidget(self.enable_check_box)

        self.colormap_groub_box = QGroupBox(self.groupBox)
        self.colormap_groub_box.setObjectName(u"colormap_groub_box")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.colormap_groub_box.sizePolicy().hasHeightForWidth())
        self.colormap_groub_box.setSizePolicy(sizePolicy2)
        self.colormap_groub_box.setMinimumSize(QSize(120, 48))
        self.colormap_groub_box.setMaximumSize(QSize(120, 48))
        self.colormap_combo_box = QComboBox(self.colormap_groub_box)
        self.colormap_combo_box.setObjectName(u"colormap_combo_box")
        self.colormap_combo_box.setGeometry(QRect(10, 18, 100, 20))

        self.verticalLayout.addWidget(self.colormap_groub_box)

        self.show_cross_check_box = QCheckBox(self.groupBox)
        self.show_cross_check_box.setObjectName(u"show_cross_check_box")

        self.verticalLayout.addWidget(self.show_cross_check_box)

        self.auto_cross_check_box = QCheckBox(self.groupBox)
        self.auto_cross_check_box.setObjectName(u"auto_cross_check_box")

        self.verticalLayout.addWidget(self.auto_cross_check_box)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.verticalLayout_4.addWidget(self.groupBox)

        self.splitter_4.addWidget(self.widget)
        self.splitter_3 = QSplitter(self.splitter_4)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setOrientation(Qt.Orientation.Vertical)
        self.verticalLayoutWidget_3 = QWidget(self.splitter_3)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayout_6 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.splitter_2 = QSplitter(self.verticalLayoutWidget_3)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Orientation.Horizontal)
        self.output_beam_view = CustomGraphicsView(self.splitter_2)
        self.output_beam_view.setObjectName(u"output_beam_view")
        self.splitter_2.addWidget(self.output_beam_view)
        self.verticalLayoutWidget = QWidget(self.splitter_2)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(self.verticalLayoutWidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.cs_plot_y = PlotWidget(self.splitter)
        self.cs_plot_y.setObjectName(u"cs_plot_y")
        self.splitter.addWidget(self.cs_plot_y)
        self.cs_plot_x = PlotWidget(self.splitter)
        self.cs_plot_x.setObjectName(u"cs_plot_x")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.cs_plot_x.sizePolicy().hasHeightForWidth())
        self.cs_plot_x.setSizePolicy(sizePolicy3)
        self.splitter.addWidget(self.cs_plot_x)

        self.verticalLayout_3.addWidget(self.splitter)

        self.splitter_2.addWidget(self.verticalLayoutWidget)

        self.verticalLayout_6.addWidget(self.splitter_2)

        self.splitter_3.addWidget(self.verticalLayoutWidget_3)
        self.verticalLayoutWidget_2 = QWidget(self.splitter_3)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayout_5 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.parametersGroupBox = QGroupBox(self.verticalLayoutWidget_2)
        self.parametersGroupBox.setObjectName(u"parametersGroupBox")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.parametersGroupBox.sizePolicy().hasHeightForWidth())
        self.parametersGroupBox.setSizePolicy(sizePolicy4)
        self.gridLayout = QGridLayout(self.parametersGroupBox)
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(2, 2, 2, 1)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.selectParametersPushButton = QPushButton(self.parametersGroupBox)
        self.selectParametersPushButton.setObjectName(u"selectParametersPushButton")

        self.gridLayout.addWidget(self.selectParametersPushButton, 0, 0, 1, 1)

        self.tableWidget = ParametersTableWidget(self.parametersGroupBox)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setShowGrid(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(40)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setMinimumSectionSize(20)
        self.tableWidget.verticalHeader().setDefaultSectionSize(20)

        self.gridLayout.addWidget(self.tableWidget, 2, 0, 1, 2)


        self.verticalLayout_5.addWidget(self.parametersGroupBox)

        self.splitter_3.addWidget(self.verticalLayoutWidget_2)
        self.splitter_4.addWidget(self.splitter_3)

        self.horizontalLayout.addWidget(self.splitter_4)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBoxCursors.setTitle(QCoreApplication.translate("Form", u"Cursors", None))
        self.groupBoxMode.setTitle(QCoreApplication.translate("Form", u"Mode", None))
        self.groupBoxTop.setTitle(QCoreApplication.translate("Form", u"Top", None))
        self.groupBoxBottom.setTitle(QCoreApplication.translate("Form", u"Bottom", None))
        self.groupBoxContrast.setTitle(QCoreApplication.translate("Form", u"Contrast", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Controls", None))
        self.enable_check_box.setText(QCoreApplication.translate("Form", u"Enable", None))
        self.colormap_groub_box.setTitle(QCoreApplication.translate("Form", u"Colormap", None))
        self.show_cross_check_box.setText(QCoreApplication.translate("Form", u"Show cross", None))
        self.auto_cross_check_box.setText(QCoreApplication.translate("Form", u"Auto cross", None))
        self.parametersGroupBox.setTitle(QCoreApplication.translate("Form", u"Beam Parameters", None))
        self.selectParametersPushButton.setText(QCoreApplication.translate("Form", u"Select", None))
    # retranslateUi

