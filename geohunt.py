from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Welcome to Geo Hunt!'

@app.route('/<name>')
def greet(name):
    return f'Hello {name}'

@app.route('/another')
def anotherPage():
    return 'Welcome to another Geo Hunt page!'

## this code calls the app.run function and executes the code in this file
## now you can call python geohunt.py in the venv and it will run flask
if __name__ == '__main__':
    app.run(debug=True)
