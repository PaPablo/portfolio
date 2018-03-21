from flask import Flask,request,render_template,redirect
from flask_script import Manager

app = Flask(__name__)

app.config.from_object('app.local_settings')

manager = Manager(app)

@app.route('/')
def index():
    import yaml

    with open("app/projects.yml", 'r') as stream:
        try:
            projects = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return render_template('index.html',projects=projects)

