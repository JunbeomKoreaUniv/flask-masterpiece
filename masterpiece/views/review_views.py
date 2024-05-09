from masterpiece.forms import ReviewForm
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, g
from datetime import datetime

from masterpiece import db

from masterpiece.models import Song, Review, User

from .auth_views import login_required

bp = Blueprint('review', __name__, url_prefix='/review')

@bp.route('/add/<int:song_id>', methods=('GET', 'POST'))
@login_required
def add(song_id):
    form = ReviewForm()
    song = Song.query.get(song_id)
    if g.user.user_name in [review.user_name for review in song.review_set]:
        flash('이미 후기를 작성하였습니다.')
        return render_template('errors.html', song_id=song_id)
    elif request.method=="POST":
        if form.validate_on_submit():
            user_name = User.query.get(session['user_id']).user_name
            review = Review(song_id=song_id, rate=form.rate.data, content=form.content.data, user_name=user_name, write_date=datetime.now())
            db.session.add(review)
            db.session.commit()
            #노래 평균평점 자동계산
            if not song.average_rate: #노래 평균평점이 None일 경우 0으로 세팅
                song.average_rate = 0
            review_count = len(song.review_set)
            song.average_rate = ((review_count-1) * song.average_rate + form.rate.data) / review_count
            db.session.commit()
            return redirect(url_for('song.detail', song_id=song_id))
    else:
        return render_template("review_add.html", form=form,song=song)

@bp.route('/delete/<int:review_id>')
@login_required
def delete(review_id):
    review = Review.query.get_or_404(review_id)
    song_id = review.song.id
    song = Song.query.get(song_id)
    if g.user.user_name != review.user_name:
        flash('삭제권한이 없습니다.')
    else:
        #노래 평균평점 자동계산
        review_count = len(song.review_set)
        song.average_rate = ((review_count) * song.average_rate - review.rate) / (review_count-1)
        db.session.delete(review)
        db.session.commit()
    return redirect(url_for('song.detail', song_id=song_id))

@bp.route('/edit/<int:review_id>', methods=('GET', 'POST'))
@login_required
def edit(review_id):
    review = Review.query.get_or_404(review_id)
    if g.user.user_name != review.user_name:
        flash('수정권한이 없습니다')
    elif request.method=="POST":
        form = ReviewForm()
        if form.validate_on_submit():
            form.populate_obj(review)
            #노래 평균평점 자동계산
            song = Song.query.get(review.song.id)
            review_count = len(song.review_set)
            song.average_rate = ((review_count) * song.average_rate -session['previous_rate'] + review.rate) / (review_count)
            db.session.commit()
            return redirect(url_for('song.detail', song_id=review.song.id))
    else:
        form = ReviewForm(obj=review)
        session['previous_rate']=review.rate
        return render_template('review_add.html', form=form)