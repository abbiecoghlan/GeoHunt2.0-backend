from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Welcome to Geo Hunt!'

@app.route('/another')
def anotherPage():
    return 'Welcome to another Geo Hunt page!'