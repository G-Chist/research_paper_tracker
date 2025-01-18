from flask import Blueprint, render_template, request, flash, jsonify, redirect
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
        # Check which button was clicked
        action = request.form.get('action')

        if action == "read":
            read = request.form.get('textfield-read')  # Gets the paper from the HTML
            try:
                if len(read) < 1:
                    flash('Link is too short!', category='error')
                else:
                    new_paper_read = PaperRead(link=read,
                                         authors="",
                                         title="",
                                         user_id=current_user.id)  # providing the schema for the paper
                    db.session.add(new_paper_read)  # adding the paper to the database
                    db.session.commit()
                    flash('Paper added!', category='success')
            except TypeError:
                flash('Server side error! TypeError', category='error')

        if action == "to-read":
            to_read = request.form.get('textfield-to-read')  # Gets the paper from the HTML
            try:
                if len(to_read) < 1:
                    flash('Link is too short!', category='error')
                else:
                    new_paper_read = PaperToRead(link=to_read,
                                               authors="",
                                               title="",
                                               user_id=current_user.id)  # providing the schema for the paper
                    db.session.add(new_paper_read)  # adding the paper to the database
                    db.session.commit()
                    flash('Paper added!', category='success')
            except TypeError:
                flash('Server side error! TypeError', category='error')

        # Check if the delete button was triggered
        deletion = request.form.get('deletion')
        if deletion:
            note = PaperRead.query.get(deletion)
            if note:
                if note.user_id == current_user.id:
                    db.session.delete(note)
                    db.session.commit()
                    print(f"Paper with ID {deletion} deleted.")
                else:
                    print("Unauthorized deletion attempt.")
            else:
                print(f"No paper found with ID {deletion}.")

    return render_template("home.html", user=current_user)


@views.route('/delete-paper-read', methods=['POST'])
def delete_paper_read():
    print("Delete paper function called!")
    paperReadId = request.form.get('paperReadId')  # Get the paperReadId from the form data

    print(f"Delete request received for paper ID: {paperReadId}")

    note = PaperRead.query.get(paperReadId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            print(f"Paper with ID {paperReadId} deleted.")
        else:
            print("Unauthorized deletion attempt.")
    else:
        print(f"No paper found with ID {paperReadId}.")

    return redirect('/')  # Redirect back to the homepage or any other page

