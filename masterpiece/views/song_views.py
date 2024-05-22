from flask import Blueprint, url_for, render_template, request, session
from werkzeug.utils import redirect
from sqlalchemy import func, desc
from datetime import datetime

from masterpiece import db
from masterpiece.models import Song, Review, User
from masterpiece.forms import SongForm, ReviewForm
from .auth_views import login_required

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
 
cid = '1c2246a49faf498eb364c3867ddf912f'
secret = 'fbe55a0277f04533a9fa88012a9d5a9f'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

bp = Blueprint('song', __name__, url_prefix='/song')

@bp.route('/')
def _list():
    page = request.args.get('page', type=int, default=1)  # 페이지
    kw = request.args.get('kw', type=str, default='') # 검색어

    # 최근 리뷰가 등록된 순서로 정렬하여 song_list에 가장 최근의 리뷰날짜와 함께 저장
    query = (db.session.query(Song.id, Song.spotify_id, Song.name, Song.singer, Song.average_rate, Song.masterpiece_score, Song.image_url, func.count(Review.id), Review.write_date).join(Review).group_by(Song.id).having(Review.write_date == func.max(Review.write_date)).order_by(desc(Review.write_date)))
    song_list = query.paginate(page=page, per_page=5)

    # 자체 음악 랭킹 기준으로 정렬하여 song_ranking에 저장
    song_ranking = (db.session.query(Song).filter(Song.average_rate != None).order_by(desc(Song.masterpiece_score)))

    if kw:
        search = sp.search(q=kw, limit=50, type="track", market='KR')
        return render_template("song_list.html", song_list=song_list, song_ranking=song_ranking, search=search)
    else:
        return render_template("song_list.html", song_list=song_list, song_ranking=song_ranking)

@bp.route('/ranking/')
def ranking():
    page = request.args.get('page', type=int, default=1)  # 페이지

    # 자체 음악 랭킹 기준으로 정렬하여 song_ranking에 저장
    song_ranking = (db.session.query(Song).filter(Song.average_rate != None).order_by(desc(Song.masterpiece_score)))
    song_ranking = song_ranking.paginate(page=page, per_page=10)

    return render_template("song_ranking.html", song_ranking=song_ranking, page=page)


@bp.route('/detail/<int:song_id>/')
def detail(song_id):
    song = Song.query.get(song_id)
    return render_template("song_detail.html", song=song)

@bp.route('/add/')
@login_required
def add():
    spotify_id = request.args.get('spotify_id', type=str)
    name = request.args.get('name', type=str)
    singer = request.args.get('singer', type=str)
    image_url = request.args.get('image_url', type=str)
    if spotify_id and name and singer and image_url:
        song = Song(spotify_id=spotify_id, name=name, singer=singer, image_url=image_url, average_rate=None)
        db.session.add(song)
        db.session.commit()
        added_song = Song.query.order_by(Song.id.desc()).first()
        return redirect(url_for('song.detail', song_id=added_song.id))
    return render_template("base.html") #오류나면 베이스템플릿만 출력