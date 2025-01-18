from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user
from .models import PaperRead, PaperToRead, User
from . import db
import json
import sqlalchemy as sa
import scraper

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
                    scraped_dict = scraper.scrapeMain(read)
                    if scraped_dict.get('error'):
                        flash('Invalid URL!', category='error')
                    else:
                        new_paper_read = PaperRead(link=read,
                                             authors=', '.join(scraped_dict.get('authors')),
                                             title=scraped_dict.get('title'),
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
                    scraped_dict = scraper.scrapeMain(to_read)
                    if scraped_dict.get('error'):
                        flash('Invalid URL!', category='error')
                    else:
                        new_paper_to_read = PaperToRead(link=to_read,
                                                   authors=', '.join(scraped_dict.get('authors')),
                                                   title=scraped_dict.get('title'),
                                                   user_id=current_user.id)  # providing the schema for the paper
                    db.session.add(new_paper_to_read)  # adding the paper to the database
                    db.session.commit()
                    flash('Paper added!', category='success')
            except TypeError:
                flash('Server side error! TypeError', category='error')

        # Check if the delete buttons were triggered
        deletionRead = request.form.get('deletionRead')
        if deletionRead:
            note = PaperRead.query.get(deletionRead)
            if note:
                if note.user_id == current_user.id:
                    db.session.delete(note)
                    db.session.commit()
                    print(f"Paper with ID {deletionRead} deleted.")
                else:
                    print("Unauthorized deletionRead attempt.")
            else:
                print(f"No paper found with ID {deletionRead}.")

        deletionToRead = request.form.get('deletionToRead')
        if deletionToRead:
            note = PaperToRead.query.get(deletionToRead)
            if note:
                if note.user_id == current_user.id:
                    db.session.delete(note)
                    db.session.commit()
                    print(f"Paper with ID {deletionToRead} deleted.")
                else:
                    print("Unauthorized deletionRead attempt.")
            else:
                print(f"No paper found with ID {deletionToRead}.")

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
            print(f"Read paper with ID {paperReadId} deleted.")
        else:
            print("Unauthorized deletion attempt.")
    else:
        print(f"No read paper found with ID {paperReadId}.")

    return redirect('/')  # Redirect back to the homepage or any other page


@views.route('/delete-paper-to-read', methods=['POST'])
def delete_paper_to_read():
    print("Delete paper function called!")
    paperToReadId = request.form.get('paperToReadId')  # Get the paperReadId from the form data

    print(f"Delete request received for paper ID: {paperToReadId}")

    note = PaperToRead.query.get(paperToReadId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            print(f"To-read paper with ID {paperToReadId} deleted.")
        else:
            print("Unauthorized deletion attempt.")
    else:
        print(f"No to-read paper found with ID {paperToReadId}.")

    return redirect('/')  # Redirect back to the homepage or any other page
