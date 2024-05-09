from flask import Blueprint, url_for, render_template, request, session
from werkzeug.utils import redirect
from datetime import datetime

from masterpiece import db
from masterpiece.models import Song, User
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
    song_list = Song.query.order_by(Song.write_date.desc())
    song_list = song_list.paginate(page=page, per_page=5)
    search = sp.search(q="아우성", limit=3, type="track", market='KR')
    return render_template("song_list.html", song_list=song_list, search=search)

@bp.route('/detail/<int:song_id>/')
def detail(song_id):
    song = Song.query.get(song_id)
    return render_template("song_detail.html", song=song)

@bp.route('/add/', methods=('GET', 'POST'))
@login_required
def add():
    form = SongForm()
    if request.method == 'POST' and form.validate_on_submit():
        user_name = User.query.get(session['user_id']).user_name
        song = Song(name=form.name.data, singer=form.singer.data, user_name=user_name, write_date = datetime.now())
        db.session.add(song)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template("song_add.html", form=form) 