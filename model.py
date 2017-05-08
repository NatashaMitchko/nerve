"""Database model for nerve
V1: three tables will be created: User, UserChallenge and Challenge

User will store id, username, password, email and phone (for verification)

UserChallenge will store id, challenge_id, user_id, is_completed, 
accepted_timestamp, completed_timestamp, lat, long, image_path, points_earned.
Relationships to the other two tables are defined by .user and .challenge

Challenge will store id, title, description, difficulty, image_path 

Class names are singular - table names are plural
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """Game user"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(25), nullable=False) #not encrypted
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(30)) #not stored as phone number type

    def __repr__(self):
        return '<User username:{username} id:{id}>'.format(username=self.username,
                                                            id=self.id)

class UserChallenge(db.Model):
    """This table maps users to tasks they've accepted"""

    __tablename__ = 'user_challenges'

    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'))
    is_completed = db.Column(db.Boolean, nullable=False, default=False)
    accepted_timestamp = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    completed_timestamp = db.Column(db.TIMESTAMP(timezone=True), nullable=True)
    lat = db.Column(db.String(12)) #+/-###.#######
    long = db.Column(db.String(12)) #+/-###.#######
    image_path = db.Column(db.String(50))
    points_earned = db.Column(db.Integer, default=0, nullable=False)

    user = db.relationship('User', backref=db.backref('users'))
    challenge = db.relationship('Challenge', backref=db.backref('challenges'))

    def __repr__(self):
        return '<UserChallenge challenge_id:{challenge_id} id:{id}>'.format(challenge_id=self.challenge_id, 
                                                                            id=self.id)

class Challenge(db.Model):
    """Stores information about individual user generated challenges"""

    __tablename__ = 'challenges'

    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    title = db.Column(db.String(35), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(50))

    def __repr__(self):
        return '<Challenge title:{title} id:{id}>'.format(title=self.title, id=self.id)


################################################################################

def init_app():
    """Creating Flask app in order to run SQLAlchemy"""

    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app):
    """Connect the database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///nerves'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == '__main__':

# in terminal: createdb nerves
# run this file in interactive mode and run db.create_all()

        init_app()

