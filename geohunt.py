from flask import Flask, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/database.db'
db = SQLAlchemy(app)




#attempts written as table 
# attempts = db.Table('user_puzzle',
#     db.Column('id', db.Integer, primary_key=True),
#     db.Column('puzzle_id', db.Integer, db.ForeignKey('puzzle.id')),
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('status', (db.String(15)))
#     )

    # time_taken
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12))
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    puzzles = db.relationship('Puzzle', secondary="attempt")
    attempts = db.relationship('Attempt', backref='user', lazy='dynamic')


##for printing
    def __str__(self):
        return f'{self.username}, {self.id}, {self.first_name}, {self.last_name}'

def user_serializer(user):
    return {
        'id': user.id,
        'username': user.username 
    }

class Puzzle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    location_name = db.Column(db.String(30))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    radius_limit = db.Column(db.Float)
    users = db.relationship('User', secondary="attempt")

##for printing
    def __str__(self):
        return f'{self.id}, {self.title}, {self.location_name}, {self.latitude}, {self.longitude}, {self.radius_limit}'

def puzzle_serializer(puzzle):
    return {
        'id': puzzle.id,
        'title': puzzle.title,
        'location_name': puzzle.location_name,
        'latitude': puzzle.latitude,
        'longitude': puzzle.longitude,
        'radius_limit': puzzle.radius_limit 
    }


class Attempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    puzzle_id = db.Column(db.Integer, db.ForeignKey('puzzle.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column((db.String(15)))
    # puzzle = db.relationship("Puzzle")
 
    def __str__(self):
        return f'{self.id}, {self.puzzle_id}, {self.user_id}, {self.status}'

def attempt_serializer(attempt):
    return {
        'id': attempt.id,
        'puzzle_id': attempt.puzzle_id,
        'user_id': attempt.user_id,
        'status': attempt.status
    }


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
