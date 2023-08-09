import json

CONFIG_FILE_PATH = './config.json'

config_data = json.load(open(CONFIG_FILE_PATH, 'r'))

devices = config_data['devices']

device_names = [device['device_name'] for device in devices]

signals = config_data['signals']

signal_names = [signal['signal_name'] for signal in signals]

tasks = config_data['tasks']


def add_device(device_name: str):
    print(device_name)
    print(device_names)
    if device_name in device_names:
        return False
    devices.append({
        'device_name': device_name
    })
    __save_config_data()
    return True


def valid_signal_name(device_name: str, signal_name: str) -> bool:
    if device_name not in device_names:
        return False
    if signal_name in signal_names:
        same_signal_name_devices = [signal['device_name'] for signal in signals if signal['signal_name'] == signal_name]
        if device_name in same_signal_name_devices:
            return False
    return True

def add_signal(device_name: str, signal_name: str, signal: str) -> bool:
    if not valid_signal_name(device_name, signal_name):
        return False
    signals.append({
        'signal_name': signal_name,
        'device_name': device_name,
        'signal': signal
    })
    __save_config_data()
    return True


def delete_all_devices():
    config_data['devices'] = []
    config_data['signals'] = []
    # config_data['tasks'] = []
    __save_config_data()
    return True


def delete_device(device_name: str):
    config_data['devices'] = [device for device in devices if device['device_name'] != device_name]
    config_data['signals'] = [signal for signal in signals if signal['device_name'] != device_name]
    # config_data['tasks'] = [task for task in tasks if task['device_name'] != device_name]
    __save_config_data()
    return True


def __save_config_data():
    global config_data
    with open(CONFIG_FILE_PATH, 'w') as f:
        json.dump(config_data, f, ensure_ascii=False)
    __load_config_data(CONFIG_FILE_PATH)


def __load_config_data(path: str):
    global config_data, devices, device_names, signals, signal_names, tasks
    config_data = json.load(open(path, 'r'))
    devices = config_data['devices']
    device_names = [device['device_name'] for device in devices]
    signals = config_data['signals']
    signal_names = [signal['signal_name'] for signal in signals]
    tasks = config_data['tasks']
