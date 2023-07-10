from matplotlib.backends.qt_compat import QtWidgets
from queue import Queue
import datetime
import dialog_export
import matplotlib.pyplot as plt
import glob
import paho.mqtt.client as mqtt
import pandas as pd
import time
import json
import sys
import random
import os
import threading
import meta
import layout
from layout_chart import ChartWindow
from matplotlib.backends.qt_compat import QtWidgets
from PyQt5.QtWidgets import QDialog

import analyze_screen
import subprocess

START_FLAG = False
global df


class Sensor:
    __slots__ = ['name', 't_prev', 'v_prev']

    def __init__(self, name):
        self.name = name
        self.t_prev = receive_time()
        self.v_prev = 0

    def update(self, t, value):
        self.t_prev = t
        self.v_prev = value


def receive_time(limit=7):
    return "-".join(str(t) for t in time.localtime()[:limit])


def row_sorter(message):
    """ Sort received message based on the sort of csv files headers """

    sorted_list = [message[title] for title in meta.header[1:]]
    sorted_list.insert(0, receive_time())
    return sorted_list


def times_to_json(time1, time2, time3, samples=5):
    command_dict = {
        'command': 'start',
        'num_samples': samples,
        'period1_length': time1,
        'period2_length': time2,
        'period3_length': time3
    }

    return json.dumps(command_dict)


def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server """

    print(f"Connected with result code {rc}")
    # add_log(logs_queue, f"Connected with result code {rc}")
    client.subscribe(meta.DATA_TOPIC)


def on_message(client, userdata, msg):
    """ The callback for when a PUBLISH message is received from the server """
    global df, START_FLAG
    if START_FLAG:
        print(msg.payload)
        loaded_msg = json.loads(msg.payload)
        sorted_sensors = row_sorter(loaded_msg)
        df = df.append({col: val for col, val in zip(meta.header, sorted_sensors)}, ignore_index=True)

        for pump in pumps.values():
            idx = meta.header.index(pump.name)
            X = [pump.t_prev, sorted_sensors[0]]
            Y = [pump.v_prev, sorted_sensors[idx]]
            t1 = threading.Thread(target=plotter, args=(X, Y, meta.colors[meta.pumps.index(pump.name)]))
            t1.start()
            t1.join()
            # ax.plot([pump.t_prev, sorted_sensors[0]], [pump.v_prev, sorted_sensors[idx]])
            pump.update(sorted_sensors[0], sorted_sensors[idx])

        # add_log(logs_queue, 'Updating pumps finished')

        # # for pump in pumps.values():
        # #     idx = meta.header.index(pump.name)
        # #     pump.update(sorted_sensors[0], sorted_sensors[idx])

        plt.pause(0.001)
        app.canvas.draw()
        # ax.legend(meta.pumps, loc='upper left')
        ax.legend(handles=meta.patches, loc='upper left')


def start_time1_handler():
    time1 = app.spinBox.value()
    add_log(logs_queue, f'Time 1 started with {time1}')

    try:
        mqtt_client.publish(meta.CNTRL_TOPIC, times_to_json(time1, 0, 0))
    except Exception:
        add_log(logs_queue, 'Publishing time1 failed!')


def start_time2_handler():
    time2 = app.spinBox_2.value()
    add_log(logs_queue, f'Time 2 started with {time2}')

    try:
        mqtt_client.publish(meta.CNTRL_TOPIC, times_to_json(0, time2, 0))
    except Exception:
        add_log(logs_queue, 'Publishing time2 failed!')


def start_time3_handler():
    time3 = app.spinBox_3.value()
    add_log(logs_queue, f'Time 3 started with {time3}')

    try:
        mqtt_client.publish(meta.CNTRL_TOPIC, times_to_json(0, 0, time3))
    except Exception:
        add_log(logs_queue, 'Publishing time3 failed!')


def browse_handler():
    folder_path = QtWidgets.QFileDialog.getExistingDirectory(app, 'Select Folder', os.path.dirname(__file__))

    if folder_path:
        add_log(logs_queue, f'Path <{folder_path}> browsed,\nnow select Level and Repetition and Start\n')
        folder_path = os.path.normpath(folder_path)
        app.textEditFolder.setText(folder_path)
    else:
        add_log(logs_queue, f'Folder selection cancelled')


def enqueue(queue, clause):
    if queue.full():
        queue.get()

    queue.put(clause)


def add_log(queue, clause):
    enqueue(queue, clause)
    app.logSection.setText('\n'.join(list(logs_queue.queue)))


def show_diagram(x):
    fig.clear()
    ax.plot(x)
    canvas.draw()
    print('Showing diagram!')


def stop_handler():
    global mqtt_client, START_FLAG
    add_log(logs_queue, 'The program finished')

    # mqtt_client.loop_stop()
    START_FLAG = False
    # app.spinBox.setValue(0)
    # app.spinBox_2.setValue(0)
    # app.spinBox_3.setValue(0)

    additivePath = app.textEditFolder.toPlainText()
    level = app.textEditLevel.toPlainText()
    repetition = app.textEditRepeat.toPlainText()

    finalAddress = additivePath + '/' + level + '/' + repetition + '/' + repetition + '.csv'
    finalAddress = os.path.normpath(finalAddress)

    base_dir = os.path.dirname(finalAddress)
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    df.to_csv(finalAddress, index=False)

    mqtt_client.publish(meta.CNTRL_TOPIC, "{'command':'stop'}")


def start_handler(_):
    createConfigFile()

    global mqtt_client, START_FLAG
    time1 = app.spinBox.value()
    time2 = app.spinBox_2.value()
    time3 = app.spinBox_3.value()
    add_log(logs_queue, f'Time 1,2,3 started with {time1}, {time2}, {time3}')
    add_log(logs_queue, f'Config file created')
    START_FLAG = True
    try:
        # mqtt_client.loop_start()
        mqtt_client.publish(meta.CNTRL_TOPIC, times_to_json(time1, time2, time3))
        # mqtt_client.start_loop()
        # add_log(logs_queue, times_to_json(time1, time2, time3))
    except Exception:
        add_log(logs_queue, 'Publishing times failed!')


def plotter(x, y, color):
    global ax, fig, app
    ax.plot(x, y, color)
    # app.canvas.draw()
    # fig.show()


def createConfigFile():
    time1 = app.spinBox.value()
    DATA_FOLDER = app.textEditFolder.toPlainText()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # creating config.txt  ->
    with open(DATA_FOLDER + "/config.txt", "w") as f:
        f.write(f"Export Time={now}\n")
        f.write(f"Data Folder={DATA_FOLDER}\n")
        f.write(f"Sample Start Index={int(time1)}\n\n")
        f.write(f"-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  \n\n")


def exportData():
    dialog = dialog_export.ExportDialog(folder=app.textEditFolder.toPlainText())
    if dialog.exec_() == QDialog.Accepted:
        add_log(logs_queue, f'all data exported in processed_data.xlsx')


def generate_json_data(num_records):
    data = []
    for i in range(num_records):
        record = {
            "S1": round(random.uniform(0.008, 0.983), 3),
            "S2": round(random.uniform(0.008, 0.983), 3),
            "S3": round(random.uniform(0.008, 0.983), 3),
            "S4": round(random.uniform(0.008, 0.983), 3),
            "S5": round(random.uniform(0.008, 0.983), 3),
            "S6": round(random.uniform(0.008, 0.983), 3)
        }
        data.append(record)

    json_data = json.dumps(data)
    return json_data


def testingDataframe():
    json_data = generate_json_data(16)
    df = create_dataframe(json_data)
    visualize_dataframe(df)


def create_dataframe(json_data):
    df = pd.read_json(json_data)
    return df


def visualize_dataframe(df):
    df.plot(ax=ax)
    ax.legend(handles=meta.patches, loc='upper left')

    canvas.draw()


def clearDataFrameAndCanvas():
    global ax, fig
    ax.clear()
    ax.legend(handles=meta.patches, loc='upper left')
    canvas.draw()


if __name__ == '__main__':

    print('MQTT to InfluxDB bridge')
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(meta.MQTT_USER, meta.MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    resultCode = mqtt_client.connect(meta.MQTT_ADDRESS, meta.MQTT_PORT)
    mqtt_client.loop_start()

    pumps = {}
    for pump in meta.pumps:
        pumps[pump] = Sensor(pump)

    df = pd.DataFrame(columns=meta.header)
    logs_queue = Queue(maxsize=6)

    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    app = layout.ApplicationWindow()
    app.show()
    app.activateWindow()
    app.raise_()

    app.startButton.clicked.connect(start_handler)
    app.stopButton.clicked.connect(stop_handler)
    app.exportButton.clicked.connect(exportData)
    # app.clearButton.clicked.connect(clearDataFrameAndCanvas)
    app.time1Button.clicked.connect(start_time1_handler)
    app.time2Button.clicked.connect(start_time2_handler)
    app.time3Button.clicked.connect(start_time3_handler)
    app.browseButton.clicked.connect(browse_handler)

    canvas = app.canvas
    fig = canvas.figure
    ax = fig.subplots()
    ax.xaxis.set_major_locator(plt.MaxNLocator(meta.X_UNITS))

    if resultCode == 0:
        add_log(logs_queue, f'Mqtt broker is ready to use')

    outputHostedNetwork = subprocess.run(["netsh", "wlan", "show", "hostednetwork"], capture_output=True, text=True)
    if str(outputHostedNetwork).__contains__("mhshse") and str(outputHostedNetwork).__contains__(
            "Mode                   : Allowed"):
        add_log(logs_queue, f'hotspot \'mhshse\' created. enable it using MyPublicWifi.exe')
    else:
        add_log(logs_queue, f'hotspot \'mhshse\' not found. See hotspot.txt for help')

    add_log(logs_queue, "Important = when browse address in this app, your path should not contains whiteSpace\n")

    qapp.exec()
