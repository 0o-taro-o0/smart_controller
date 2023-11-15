from flask import Blueprint, render_template, request, abort

import config

tasks_module = Blueprint('tasks', __name__)


@tasks_module.route('/smart-controller/tasks/', methods=['GET', 'POST', 'DELETE'])
def tasks():
    """
    GET: タスク一覧を表示
    POST: タスクを追加
    DELETE: タスクを全て削除
    """
    if request.method == 'GET':
        return render_template('tasks.html', tasks=config.tasks)
    if request.method == 'POST':
        return 200
    if request.method == 'DELETE':
        return 200


@tasks_module.route('/smart-controller/tasks/<string:task_name>', methods=['GET', 'PATCH', 'DELETE'])
def task_detail(task_name: str):
    """
    GET: タスク詳細を表示
    PATCH: タスクを更新
    DELETE: タスクを削除
    """
    if request.method == 'GET':
        matching_tasks = [task for task in config.tasks if task['task_name'] == task_name]
        if not matching_tasks:
            abort(404)
        return render_template('task_detail.html', device_names=config.device_names, signal_names_of=config.signal_names_of, task=matching_tasks[0])
    if request.method == 'PATCH':
        return 200
    if request.method == 'DELETE':
        return 200