import glob
import os
import sys
import pandas as pd
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout, QLabel, QLineEdit, \
    QDialogButtonBox, QWidget


class ExportDialog(QDialog):
    def __init__(self, parent=None, folder=''):
        super(ExportDialog, self).__init__(parent)
        self.resize(360, 100)
        self.setWindowTitle('Add Extra Column?')
        self.dataFolder = folder

        icon = QIcon("icon.ico")
        self.setWindowIcon(icon)

        self.label1 = QLabel('Set If Statement:\nby using \'Class\' data ', self)
        self.text_input = QLineEdit(self)
        self.text_input.setText("if x < 0.01 non else sample")

        # self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

        self.button_box = QDialogButtonBox(self)
        self.button_box.addButton(QPushButton(" Append "), QDialogButtonBox.AcceptRole)
        self.button_box.addButton(QPushButton(" Don't Need "), QDialogButtonBox.RejectRole)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label1)
        layout.addWidget(self.text_input)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

        self.button_box.accepted.connect(self.addCategorical)
        self.button_box.rejected.connect(self.doNotAddCategorical)

    def addCategorical(self):

        strMe = str(self.text_input.text())

        # Extract threshold value 0.01
        threshold_str = strMe.split('<')[1].split()[0].strip()
        threshold = float(threshold_str)

        # Extract 'non' value
        non = strMe.split(threshold_str)[1].split()[0].strip()

        # Extract 'sample' value
        sample = strMe.split('else')[1].strip()

        DATA_FOLDER = self.dataFolder

        time1 = 100
        config_file = os.path.join(DATA_FOLDER, "config.txt")
        if not os.path.exists(config_file):
            with open(config_file, "x") as f:
                for line in f:
                    if line.__contains__('Index'):
                        time1 = int(line.split('=')[1])
        else:
            with open(DATA_FOLDER + "/config.txt") as f:
                for line in f:
                    if line.__contains__('Index'):
                        time1 = int(line.split('=')[1])

        SAMPLE_START_INDEX = int(time1 - (time1 / 10))
        SKIP_ROW_INDEX = 70

        # creating csv file  ->
        sensors = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6']
        header = [*sensors, 'Temperature', 'Humidity', 'Class']
        df = pd.DataFrame(columns=header)

        data_paths = glob.glob(DATA_FOLDER + '/*/*/*.csv', recursive=True)

        for file_path in data_paths:
            raw_data = pd.read_csv(file_path)
            xmax = raw_data[SKIP_ROW_INDEX:].max(0)  # Max values of each column
            process_dict = {}

            for sensor in sensors:
                sample_start = raw_data[sensor][SAMPLE_START_INDEX]
                if sample_start == 0:
                    process_dict.setdefault(sensor, 0)
                else:
                    # Normalizing sensors data
                    process_dict.setdefault(sensor, ((xmax[sensor] - sample_start) / sample_start).round(4))

            process_dict.setdefault('Temperature', xmax['Temperature'])
            process_dict.setdefault('Humidity', xmax['Humidity'])
            process_dict.setdefault('Class', file_path.split('\\')[-3])
            df = pd.concat([df, pd.DataFrame(process_dict, index=[0])], ignore_index=True)

        df['class_q'] = df['Class'].apply(lambda x: non if float(x) < threshold else sample)
        df.to_excel(DATA_FOLDER + '\processed_data.xlsx', index=False)

        self.accept()

    def doNotAddCategorical(self):
        DATA_FOLDER = self.dataFolder

        time1 = 100
        config_file = os.path.join(DATA_FOLDER, "config.txt")
        if not os.path.exists(config_file):
            with open(config_file, "x") as f:
                for line in f:
                    if line.__contains__('Index'):
                        time1 = int(line.split('=')[1])
        else:
            with open(DATA_FOLDER + "/config.txt") as f:
                for line in f:
                    if line.__contains__('Index'):
                        time1 = int(line.split('=')[1])

        SAMPLE_START_INDEX = int(time1 - (time1 / 10))
        SKIP_ROW_INDEX = 70

        # creating csv file  ->
        sensors = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6']
        header = [*sensors, 'Temperature', 'Humidity', 'Class']
        df = pd.DataFrame(columns=header)

        data_paths = glob.glob(DATA_FOLDER + '/*/*/*.csv', recursive=True)

        for file_path in data_paths:
            raw_data = pd.read_csv(file_path)
            xmax = raw_data[SKIP_ROW_INDEX:].max(0)  # Max values of each column
            process_dict = {}

            for sensor in sensors:
                sample_start = raw_data[sensor][SAMPLE_START_INDEX]
                if sample_start == 0:
                    process_dict.setdefault(sensor, 0)
                else:
                    # Normalizing sensors data
                    process_dict.setdefault(sensor, ((xmax[sensor] - sample_start) / sample_start).round(4))

            process_dict.setdefault('Temperature', xmax['Temperature'])
            process_dict.setdefault('Humidity', xmax['Humidity'])
            process_dict.setdefault('Class', file_path.split('\\')[-3])
            df = pd.concat([df, pd.DataFrame(process_dict, index=[0])], ignore_index=True)


        df.to_excel(DATA_FOLDER + '\processed_data.xlsx', index=False)

        self.accept()
