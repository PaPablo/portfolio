from flask import Flask,request,render_template,redirect
from flask_script import Manager

app = Flask(__name__)

app.config.from_object('app.local_settings')

manager = Manager(app)


def add_static_prefix(projects):

    f = lambda x: 'static/images/'+x if x is not None else None

    for project in projects['projects']:

        if project["project"]["images"] is None:
            continue

        project["project"]["images"] = list(map(f,project["project"]["images"]))

    print(projects)
    return projects

@app.route('/')
def index():
    import yaml

    with open("app/projects.yml", 'r') as stream:
        try:
            projects = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    add_static_prefix(projects)

    return render_template('index.html',projects=projects)

