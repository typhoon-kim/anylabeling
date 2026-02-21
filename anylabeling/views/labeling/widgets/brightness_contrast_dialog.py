"""This module defines brightness/contrast dialog"""

import PIL.Image
import PIL.ImageEnhance
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt

from .. import utils


class BrightnessContrastDialog(QtWidgets.QDialog):
    """Dialog for adjusting brightness and contrast of current image"""

    def __init__(self, img, callback, parent=None):
        super(BrightnessContrastDialog, self).__init__(parent)
        self.setModal(True)
        self.setWindowTitle(self.tr("Display Options"))

        self.slider_brightness = self._create_slider()
        self.slider_contrast = self._create_slider()
        self.slider_darkness = self._create_slider(0, 255, 0)

        self.reset_button = QtWidgets.QPushButton(self.tr("Reset"))
        self.reset_button.clicked.connect(self.reset_values)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(self.tr("Brightness"), self.slider_brightness)
        form_layout.addRow(self.tr("Contrast"), self.slider_contrast)
        form_layout.addRow(self.tr("Background Darkness"), self.slider_darkness)
        
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.reset_button)
        self.setLayout(main_layout)

        assert isinstance(img, PIL.Image.Image)
        self.img = img
        self.callback = callback

    def reset_values(self):
        """Reset all values to default"""
        self.slider_brightness.setValue(50)
        self.slider_contrast.setValue(50)
        self.slider_darkness.setValue(0)
        self.on_new_value(None)

    def on_new_value(self, value):
        """On new value event"""
        brightness = self.slider_brightness.value() / 50.0
        contrast = self.slider_contrast.value() / 50.0
        darkness = self.slider_darkness.value()

        img = self.img
        img = PIL.ImageEnhance.Brightness(img).enhance(brightness)
        img = PIL.ImageEnhance.Contrast(img).enhance(contrast)

        img_data = utils.img_pil_to_data(img)
        qimage = QtGui.QImage.fromData(img_data)
        self.callback(qimage, darkness)

    def _create_slider(self, min_val=0, max_val=150, default_val=50):
        """Create a slider"""
        slider = QtWidgets.QSlider(Qt.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(default_val)
        slider.valueChanged.connect(self.on_new_value)
        return slider
