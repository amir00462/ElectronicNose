import matplotlib.patches as mpatches

MQTT_ADDRESS = 'localhost'
MQTT_USER = 'pl_arduino'
MQTT_PASSWORD = 'pla_1400'
CNTRL_TOPIC = 'esp/control'
DATA_TOPIC = 'esp/data'
MQTT_PORT = 1883

data_path = r"C:\Users\Amir  Mohammadi\Desktop\ahmadi roshan/Plot sensors"  # Directory of .csv dataset files

pumps = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6']
header = ['Time', *pumps, 'Temperature', 'Humidity', 'REF']

colors = ['r','b','g','k','m','y']
S1_patch = mpatches.Patch(color='r', label='S1')
S2_patch = mpatches.Patch(color='b', label='S2')
S3_patch = mpatches.Patch(color='g', label='S3')
S4_patch = mpatches.Patch(color='k', label='S4')
S5_patch = mpatches.Patch(color='m', label='S5')
S6_patch = mpatches.Patch(color='y', label='S6')
patches = [S1_patch, S2_patch, S3_patch, S4_patch, S5_patch, S6_patch]


X_UNITS = 5

FILE_TYPES = 'Comma Separated Values (*.csv)'
