from flask import (Blueprint, render_template)

bp = Blueprint('city', __name__)


@bp.route('/')
def getbasestats():
    return render_template("index.html")
