from flask import Blueprint

tasks_module = Blueprint('tasks', __name__)


@tasks_module.route('/smart-controller/tasks/')
def task_list():
    return 'task list'


@tasks_module.route('/smart-controller/tasks/<string:task_name>')
def task_detail(task_name: str):
    return 'task detail'
