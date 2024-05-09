from masterpiece import db
from datetime import datetime

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    singer = db.Column(db.String(200), nullable=False)
    average_rate = db.Column(db.Float, nullable=True, server_default='0')
    write_date = db.Column(db.DateTime(), nullable=False)
    user_name = db.Column(db.String(200), db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('Song_set'))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id', ondelete='CASCADE'))
    song = db.relationship('Song', backref=db.backref('review_set'))
    rate = db.Column(db.Float, nullable=False)
    content = db.Column(db.Text(), nullable=False)
    user_name = db.Column(db.String(200), db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('Review_set'))
    write_date = db.Column(db.DateTime(), nullable=False)
    #좋아요수 추가해야함
    #댓글 추가해아함

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email_id = db.Column(db.String(200), unique=True, nullable=False)
    user_name = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)