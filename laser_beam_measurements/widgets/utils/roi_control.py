#
# Project: laser_beam_measurements
#
# File: roi_control.py
#
# Author: Dmitry Molchanov
#
# Copyright 2025 Dmitry Molchanov <d.a.molchanoff@gmail.com>
#


from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QDoubleSpinBox
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot

__all__ = ["ROIControl"]


class ROIControl(QWidget):

    def __init__(self, parent=None, *args, **kwargs):
        super(ROIControl, self).__init__(parent=parent, *args, **kwargs)

        self._outerLayout = QHBoxLayout(self)
        self._outerLayout.setSpacing(0)
        self._outerLayout.setContentsMargins(0, 0, 0, 0)

        self._label = QLabel(self)
        self._spinBox = QDoubleSpinBox(self)
        self._spinBox.setKeyboardTracking(False)
        self._spinBox.setMinimum(0)
        self._spinBox.setMaximum(10000)

        self._outerLayout.addWidget(self._label)
        self._outerLayout.addWidget(self._spinBox)
        # self._spinBox.setSingleStep(self._slider.get_range()/100.0)
        # self._connect()

    def set_label_text(self, text: str) -> None:
    	self._label.setText(text)

    @property
    def label(self) -> QLabel:
    	return self._label

    @property
    def spin_box(self) -> QDoubleSpinBox:
    	return self._spinBox
    
