from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import PaperRead, PaperToRead, User
from . import db
import json
import sqlalchemy as sa

views = Blueprint('views', __name__)

@views.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    return render_template('user.html', user=user)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        pass  # Placeholder

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  

    # Placeholder

    return jsonify({})
