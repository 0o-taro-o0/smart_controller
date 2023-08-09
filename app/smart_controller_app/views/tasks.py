from flask import Blueprint, render_template

import config

tasks_module = Blueprint('tasks', __name__)


@tasks_module.route('/smart-controller/tasks/')
def task_list():
    print(config.tasks)
    return render_template('tasks.html', tasks=config.tasks)


@tasks_module.route('/smart-controller/tasks/<string:task_name>')
def task_detail(task_name: str):
    return 'task detail'
