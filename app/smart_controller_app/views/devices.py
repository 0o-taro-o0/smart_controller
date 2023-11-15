from flask import Blueprint, render_template, request, jsonify, abort
from markupsafe import escape

import config

devices_module = Blueprint('devices', __name__)


@devices_module.route('/smart-controller/devices/', methods=['GET', 'POST', 'DELETE'])
def devices():
    if request.method == 'GET':
        return render_template('devices.html', devices=config.devices)
    if request.method == 'POST':
        device_name = request.form.get('device_name')
        if not device_name:
            abort(400)
        if config.valid_device_name(device_name):
            config.add_device(device_name)
            return jsonify({'message': 'added new device'}), 200
        return jsonify({'message': 'the device name already exists'}), 400
    if request.method == 'DELETE':
        config.delete_all_devices()
        return jsonify({'message': 'deleted successfully'}), 200


@devices_module.route('/smart-controller/devices/<string:device_name>/', methods=['GET', 'POST', 'DELETE'])
def signals(device_name: str):
    device_name = escape(device_name)
    if request.method == 'GET':
        if device_name in config.device_names:
            matching_signals = [s for s in config.signals if s['device_name'] == device_name]
            return render_template('signals.html', device_name=device_name, signals=matching_signals)
        abort(404)
    if request.method == 'POST':
        signal_name = request.form.get('signal_name')
        if not signal_name:
            abort(400)
        if config.valid_signal_name(device_name, signal_name):
            # 信号読み取り開始 並列
            # 指定秒後にクライアント側からAjaxで信号登録の成否確認(signalにhttpリクエスト)し、結果に応じて表示を変更
            # config.jsonへの書き込みは別処理
            signal_data = 'start learning signal'    # 仮
            config.add_signal(device_name, signal_name, signal_data)  # 仮
            return jsonify({'message': 'starting to learn new signal'}), 200
        return jsonify({'message': f'the signal name of {device_name} already exists'}), 400
    if request.method == 'DELETE':
        config.delete_device(device_name)
        return jsonify({'message': 'deleted successfully'}), 200


@devices_module.route('/smart-controller/devices/<string:device_name>/<string:signal_name>/', methods=['GET', 'DELETE'])
def signal(device_name: str, signal_name: str):
    device_name, signal_name = map(escape, (device_name, signal_name))
    if request.method == 'GET':
        # 信号送信
        return jsonify({'message': f'{signal_name} signal of {device_name} sent successfully'}), 200
    if request.method == 'DELETE':
        print(('delete', device_name, signal_name))
        config.delete_signal(device_name, signal_name)
        return jsonify({'message': 'deleted successfully'}), 200
