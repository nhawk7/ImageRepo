from imagerepo import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# many to many table
uploads = db.Table('uploads',
                   db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                   db.Column('image_hash', db.String(32), db.ForeignKey('image.hash'), primary_key=True))


# user table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    images = db.relationship('Image', secondary=uploads, lazy='subquery',
                             backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f"User('id={self.id}', 'username={self.username}')"


# image table
class Image(db.Model):
    hash = db.Column(db.String(8), primary_key=True)

    def __repr__(self):
        return f"{self.hash}.png"
