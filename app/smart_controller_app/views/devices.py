from flask import Blueprint, render_template, request, jsonify, redirect, url_for, abort
from markupsafe import escape

import config

devices_module = Blueprint('devices', __name__)


@devices_module.route('/smart-controller/devices/', methods=['GET', 'POST', 'DELETE'])
def devices():
    if request.method == 'GET':
        return render_template('devices.html', devices=config.devices)
    if request.method == 'POST':
        if config.add_device(request.form.get('device_name')):
            return redirect(url_for('devices.devices'))
        return jsonify({'message': 'the device name already exists'}), 400
    if request.method == 'DELETE':
        config.delete_all_devices()
        return redirect(url_for('devices.devices'))


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
            signal = 'start learning signal'
            return jsonify({'message': 'starting to learn new signal'}), 200
        return jsonify({'message': f'the signal name of {device_name} already exists'}), 400
    if request.method == 'DELETE':
        config.delete_device(device_name)
        return redirect(url_for('devices.devices'))


@devices_module.route('/smart-controller/devices/<string:device_name>/<string:signal_name>/')
def signal(device_name: str, signal_name: str):
    device_name, signal_name = map(escape, (device_name, signal_name))
    print((device_name, signal_name))
    # return device_name+signal_name
