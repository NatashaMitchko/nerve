from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """Game user - basic info"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, 
                    nullable=False, 
                    autoincrement=True, 
                    primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(30))

    def __repr__(self):
        return '<User username:{username} id:{id}>'.format(username=self.username,
                                                            id=self.id)
