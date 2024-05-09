from flask import Blueprint, url_for, render_template
from werkzeug.utils import redirect

from masterpiece.models import Song

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return redirect(url_for('song._list'))