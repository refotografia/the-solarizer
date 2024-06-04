import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QGroupBox, QGridLayout, \
    QMessageBox, QComboBox, QSlider
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import solar
import datetime


class MixerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.thresholds = [0, 255, 0, 255, 0, 255, 0, 255]
        self.input_button = QPushButton('Browse')
        self.input_lineedit = QLineEdit()
        self.input_label = QLabel('Source Image:')
        self.input_label.setAlignment(QtCore.Qt.AlignRight)
        self.finishGroup = QGroupBox('Output Location')
        self.startGroup = QGroupBox('File selection')

        self.apply_button = QPushButton('Solarize!')
        self.apply_button.setStyleSheet('QPushButton {background-color: grey; color: black;}')
        self.preset_lineedit = QLineEdit()
        self.preset_lineedit.setFixedWidth(275)
        self.preset_button = QPushButton('Create Preset')
        self.delete_preset_button = QPushButton('Delete Preset')
        self.presets = QComboBox()

        self.format_compression = QComboBox()
        self.output_name_lineedit = QLineEdit()
        self.output_name_label = QLabel('Output Name:')
        self.output_name_label.setAlignment(QtCore.Qt.AlignRight)
        self.output_button = QPushButton('Browse')
        self.output_label = QLabel('Output Path:')
        self.output_label.setAlignment(QtCore.Qt.AlignRight)
        self.output_lineedit = QLineEdit()
        self.buttonsGroup = QGroupBox('Save')

        self.sliders_group = QGroupBox('Thresholds')

        self.slider_shadows = QSlider(Qt.Horizontal)
        self.slider_shadows.setRange(0, 255)
        self.slider_shadows.setSingleStep(1)
        self.slider_shadows.setTickPosition(QSlider.TicksBothSides)
        self.slider_shadows.setTickInterval(5)
        self.slider_shadows.setValue(self.thresholds[0])
        self.slider_shadows.setStyleSheet("QSlider::handle:horizontal { background: #000000; border: 5px solid #000000; width: 40px; border-radius: 3px;}")
        self.slider_shadows.valueChanged.connect(self.update_thresholds)

        self.slider_high = QSlider(Qt.Horizontal)
        self.slider_high.setRange(0, 255)
        self.slider_high.setSingleStep(1)
        self.slider_high.setTickPosition(QSlider.TicksBothSides)
        self.slider_high.setTickInterval(5)
        self.slider_high.setValue(self.thresholds[1])
        self.slider_high.setStyleSheet("QSlider::handle:horizontal { background: #ffffff; border: 5px solid #ffffff; width: 40px; border-radius: 3px;}")
        self.slider_high.valueChanged.connect(self.update_thresholds)

        self.slider_r_shadows = QSlider(Qt.Horizontal)
        self.slider_r_shadows.setRange(0, 255)
        self.slider_r_shadows.setSingleStep(1)
        self.slider_r_shadows.setTickPosition(QSlider.TicksBothSides)
        self.slider_r_shadows.setTickInterval(5)
        self.slider_r_shadows.setValue(self.thresholds[2])
        self.slider_r_shadows.setStyleSheet("QSlider::handle:horizontal { background: #fe1200; border: 5px solid #000000; width: 40px; border-radius: 3px;}")
        self.slider_r_shadows.valueChanged.connect(self.update_thresholds)

        self.slider_r_high = QSlider(Qt.Horizontal)
        self.slider_r_high.setRange(0, 255)
        self.slider_r_high.setSingleStep(1)
        self.slider_r_high.setTickPosition(QSlider.TicksBothSides)
        self.slider_r_high.setTickInterval(5)
        self.slider_r_high.setValue(self.thresholds[3])
        self.slider_r_high.setStyleSheet("QSlider::handle:horizontal { background: #fe1200; border: 5px solid #ffffff; width: 40px; border-radius: 3px;}")
        self.slider_r_high.valueChanged.connect(self.update_thresholds)

        self.slider_g_shadows = QSlider(Qt.Horizontal)
        self.slider_g_shadows.setRange(0, 255)
        self.slider_g_shadows.setSingleStep(1)
        self.slider_g_shadows.setTickPosition(QSlider.TicksBothSides)
        self.slider_g_shadows.setTickInterval(5)
        self.slider_g_shadows.setValue(self.thresholds[4])
        self.slider_g_shadows.setStyleSheet("QSlider::handle:horizontal { background: #02ec10; border: 5px solid #000000; width: 40px; border-radius: 3px;}")
        self.slider_g_shadows.valueChanged.connect(self.update_thresholds)

        self.slider_g_high = QSlider(Qt.Horizontal)
        self.slider_g_high.setRange(0, 255)
        self.slider_g_high.setSingleStep(1)
        self.slider_g_high.setTickPosition(QSlider.TicksBothSides)
        self.slider_g_high.setTickInterval(5)
        self.slider_g_high.setValue(self.thresholds[5])
        self.slider_g_high.setStyleSheet("QSlider::handle:horizontal { background: #02ec10; border: 5px solid #ffffff; width: 40px; border-radius: 3px;}")
        self.slider_g_high.valueChanged.connect(self.update_thresholds)

        self.slider_b_shadows = QSlider(Qt.Horizontal)
        self.slider_b_shadows.setRange(0, 255)
        self.slider_b_shadows.setSingleStep(1)
        self.slider_b_shadows.setTickPosition(QSlider.TicksBothSides)
        self.slider_b_shadows.setTickInterval(5)
        self.slider_b_shadows.setValue(self.thresholds[6])
        self.slider_b_shadows.setStyleSheet("QSlider::handle:horizontal { background: #0b8ae9; border: 5px solid #000000; width: 40px; border-radius: 3px;}")
        self.slider_b_shadows.valueChanged.connect(self.update_thresholds)

        self.slider_b_high = QSlider(Qt.Horizontal)
        self.slider_b_high.setRange(0, 255)
        self.slider_b_high.setSingleStep(1)
        self.slider_b_high.setTickPosition(QSlider.TicksBothSides)
        self.slider_b_high.setTickInterval(5)
        self.slider_b_high.setValue(self.thresholds[7])
        self.slider_b_high.setStyleSheet("QSlider::handle:horizontal { background: #0b8ae9; border: 5px solid #ffffff; width: 40px; border-radius: 3px;}")
        self.slider_b_high.valueChanged.connect(self.update_thresholds)

        self.fc_format = ".jpg"
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('The Solarizer')
        self.setFixedSize(1200, 1400)

        # button to find source
        self.input_button.clicked.connect(self.browse_input)
        self.output_button.clicked.connect(self.browse_output)
        # combo to set jpeg or tiff
        self.format_compression.setFixedWidth(300)
        self.format_compression.addItem("Jpeg")
        self.format_compression.addItem("Tiff")
        self.format_compression.activated[str].connect(self.onselected)
        # combo to set different presets
        self.presets.setFixedWidth(300)
        with open("presets.json", "r") as read_file:
            data = json.load(read_file)
            for key in data:
                self.presets.addItem(key)
        self.presets.activated[str].connect(self.apply_preset)
        # Button to apply run app
        self.apply_button.setFixedWidth(300)
        self.apply_button.clicked.connect(self.solarize_image)
        # button to save presets
        self.preset_button.setFixedWidth(300)
        self.preset_button.clicked.connect(self.save_preset)
        # button to delete presets
        self.delete_preset_button.setFixedWidth(300)
        self.delete_preset_button.clicked.connect(self.delete_preset)

        # Start Layout setup
        start_layout = QGridLayout()
        start_layout.addWidget(self.input_label, 0, 0)
        start_layout.addWidget(self.input_lineedit, 0, 1)
        start_layout.addWidget(self.input_button, 0, 2)
        self.startGroup.setLayout(start_layout)

        sliders_layout = QGridLayout()
        sliders_layout.setVerticalSpacing(5)
        sliders_layout.addWidget(self.slider_shadows)
        sliders_layout.addWidget(self.slider_high)
        sliders_layout.addWidget(self.slider_r_shadows)
        sliders_layout.addWidget(self.slider_r_high)
        sliders_layout.addWidget(self.slider_g_shadows)
        sliders_layout.addWidget(self.slider_g_high)
        sliders_layout.addWidget(self.slider_b_shadows)
        sliders_layout.addWidget(self.slider_b_high)
        self.sliders_group.setLayout(sliders_layout)
        
        # finish layout setup
        finish_layout = QGridLayout()
        finish_layout.addWidget(self.output_label, 0, 0)
        finish_layout.addWidget(self.output_lineedit, 0, 1)
        finish_layout.addWidget(self.output_button, 0, 2)
        finish_layout.addWidget(self.output_name_label, 1, 0)
        finish_layout.addWidget(self.output_name_lineedit, 1, 1)
        finish_layout.addWidget(self.format_compression, 1, 2)
        self.finishGroup.setLayout(finish_layout)

        buttons_layout = QGridLayout()
        buttons_layout.addWidget(self.preset_lineedit, 0, 1)
        buttons_layout.addWidget(self.presets, 1, 1)
        buttons_layout.addWidget(self.preset_button, 0, 0)
        buttons_layout.addWidget(self.delete_preset_button, 1, 0)
        buttons_layout.addWidget(self.apply_button, 2, 2)
        self.buttonsGroup.setLayout(buttons_layout)

        # final layout
        grid = QGridLayout()
        grid.setVerticalSpacing(1)
        grid.addWidget(self.startGroup, 0, 0, 1, 1)
        grid.addWidget(self.sliders_group, 1, 0, 5, 1)
        grid.addWidget(self.finishGroup, 6, 0, 1, 1)
        grid.addWidget(self.buttonsGroup, 8, 0, 1, 1)
        self.setLayout(grid)
        self.show()

    def browse_input(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Image")
        if filename:
            self.input_lineedit.setText(filename)

    def browse_output(self):
        foldername = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if foldername:
            self.output_lineedit.setText(foldername)

    def onselected(self, textval):
        if textval == "Jpeg":
            self.fc_format = ".jpg"
        if textval == "Tiff":
            self.fc_format = ".tif"

    def show_success_message(self, output_path):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setFixedSize(400, 300)
        msg.setText("File saved successfully")
        msg.setInformativeText(f"The file was saved as {output_path}")
        msg.setWindowTitle("Success")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.move(self.geometry().center() - msg.rect().center())
        msg.exec_()

    def update_thresholds(self, value):
        if self.sender() == self.slider_shadows:
            self.thresholds[0] = value
        if self.sender() == self.slider_high:
            self.thresholds[1] = value
        if self.sender() == self.slider_r_shadows:
            self.thresholds[2] = value
        if self.sender() == self.slider_r_high:
            self.thresholds[3] = value
        if self.sender() == self.slider_g_shadows:
            self.thresholds[4] = value
        if self.sender() == self.slider_g_high:
            self.thresholds[5] = value
        if self.sender() == self.slider_b_shadows:
            self.thresholds[6] = value
        if self.sender() == self.slider_b_high:
            self.thresholds[7] = value

    def solarize_image(self):
        if self.thresholds == [0, 255, 0, 255, 0, 255, 0, 255]:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setFixedSize(400, 300)
            msg.setText("Solarize!")
            msg.setInformativeText("Move sliders from default position before applying changes to image.")
            msg.setWindowTitle("Defaults Still Set")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.move(self.geometry().center() - msg.rect().center())
            msg.exec_()
        else:
            image = self.input_lineedit.text()
            thresholds = self.thresholds
            output_path = self.output_lineedit.text() + "/" + self.output_name_lineedit.text() + self.fc_format
            out = solar.solarize(
                image=image,
                thresholds=thresholds,
            )
            out.save(output_path)  # Save as defined by ComboBox
            self.show_success_message(output_path)

    def apply_preset(self, textval):
        with open("presets.json", "r") as read_file:
            data = json.load(read_file)
        self.thresholds = data[textval]
        self.slider_shadows.setValue(self.thresholds[0])
        self.slider_high.setValue(self.thresholds[1])
        self.slider_r_shadows.setValue(self.thresholds[2])
        self.slider_r_high.setValue(self.thresholds[3])
        self.slider_g_shadows.setValue(self.thresholds[4])
        self.slider_g_high.setValue(self.thresholds[5])
        self.slider_b_shadows.setValue(self.thresholds[6])
        self.slider_b_high.setValue(self.thresholds[7])

    def save_preset(self):
        if not self.preset_lineedit.text():
            self.preset_lineedit.setText(f"User Preset {datetime.datetime.now()}")
        with open("presets.json", 'r+') as file:
            file_data = json.load(file)
            file_data.update({self.preset_lineedit.text(): self.thresholds})
            file.seek(0)
            json.dump(file_data, file, indent=4)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setFixedSize(400, 300)
        msg.setText("Preset created")
        msg.setInformativeText(f"The preset was saved as {self.preset_lineedit.text()}")
        msg.setWindowTitle("Success")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.move(self.geometry().center() - msg.rect().center())
        msg.exec_()
        self.presets.addItem(self.preset_lineedit.text())
        self.preset_lineedit.clear()

    def delete_preset(self):
        preset_to_delete = self.presets.currentText()
        if preset_to_delete == "Default":
            # the preset Default is no change to image, it is a way to reset the app
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setFixedSize(400, 300)
            msg.setText("Ooops")
            msg.setInformativeText("This preset can't be removed. It serves to reset all sliders.")
            msg.setWindowTitle("Sorry")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.move(self.geometry().center() - msg.rect().center())
            msg.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setFixedSize(400, 300)
            msg.setText("Delete preset?")
            msg.setInformativeText(f"Are you sure you want to delete: {preset_to_delete}?")
            msg.setWindowTitle("Please confirm")
            retval = msg.setStandardButtons(QMessageBox.Ok, QMessageBox.Cancel)
            msg.move(self.geometry().center() - msg.rect().center())
            msg.exec_()
            if retval == QMessageBox.Ok:
                with open("presets.json", 'r+') as file:
                    file_data = json.load(file)
                    del file_data[preset_to_delete]
                    file.seek(0)
                    json.dump(file_data, file, indent=4)
                # set presets combo back to Default, which is index 0
                self.presets.setCurrentIndex(0)
            else:
                pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MixerApp()
    sys.exit(app.exec_())
