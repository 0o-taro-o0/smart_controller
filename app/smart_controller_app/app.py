from flask import Flask

from views import tasks_module, devices_module

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


app.register_blueprint(devices_module)
app.register_blueprint(tasks_module)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
