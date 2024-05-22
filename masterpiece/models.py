from masterpiece import db
from datetime import datetime

#Song 모델 속성 추가하거나 삭제시 song_views의 _list뷰함수의 query의 SELECT대상 수정해야함.
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(200), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    singer = db.Column(db.String(200), nullable=False)
    average_rate = db.Column(db.Float, nullable=True, server_default='0')
    masterpiece_score = db.Column(db.Float)
    image_url = db.Column(db.String(300), nullable=True, server_default='https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg')
    # review_set 연동돼있음.

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
    # Review_set 연동돼있음.