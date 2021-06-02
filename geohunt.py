from flask import Flask, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12))

    def __str__(self):
        return f'{self.username}, {self.id}'

def user_serializer(user):
    return {
        'id': user.id,
        'username': user.username 
    }

# attempt = Table(db.model):
#     id = db.Column(db.Integer, primary_key=True)
#     status = db.Column(db.String(15))

# attempt = Table(db.model):
    # puzzle key
    # user key
    # status
    # time_taken
    

@app.route('/users', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return jsonify([*map(user_serializer, User.query.all())])
    if request.method == 'POST':
        request_data = json.loads(request.data)
        user = User(username=request_data['username'])
        db.session.add(user)
        db.session.commit()
        return {
            'name' : user.username
        }

@app.route('/users/<int:id>', methods=['GET', 'DELETE'])
def profile(id):
    if request.method == 'GET':
    # return jsonify([*map(user_serializer, User.query.filter_by(id=id))])
        username = User.query.filter_by(id=id).first().username
        return {
            "username": f'{username}'
        }
    if request.method == 'DELETE':
        User.query.filter_by(id=id).delete()
        db.session.commit()
        return {
            '204': 'Deleted successfully'
        }


@app.route('/geohunt', methods=['GET'])
def example():
    return {
        'message': 'Welcome to Geo Hunt, abbie!',
        "name": "Abbie"
    }


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
