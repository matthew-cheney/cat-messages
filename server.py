import sqlite3
import uuid

from flask import Flask, render_template, request, redirect, url_for
import DBHandler
import Emailer
from json.decoder import JSONDecodeError
import re

from CustomErrors import EmailNotFoundError

app = Flask(__name__)

db_filename = 'db/cat_emails.db'

@app.route('/')
def home():
    all_emails = DBHandler.get_all_emails(db_filename)
    return render_template('index.html', all_emails=all_emails)

@app.route('/subscribe', methods=['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        # GET request
        return render_template('subscribe.html')
    else:
        # POST request
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        if '' in (first_name, last_name, email):
            return 'invalid credentials'
        if re.findall(r'[^@]+@[^@]+\.[^@]+', email) == []:
            return "invalid email"
        verify_key = uuid.uuid4().hex
        DBHandler.add_unverified_email(db_filename, first_name, last_name, email, verify_key)
        Emailer.send_verification_email(db_filename, email)
        return redirect(url_for('home'))

@app.route('/verify/<email>/<verify_key>')
def verify_email(email, verify_key):
    try:
        person = DBHandler.get_person_by_email_unverified(db_filename, email)
        if person[4] == verify_key:
            # Key is correct
            try:
                DBHandler.verify_email(db_filename, email)
                return f'verified'
            except EmailNotFoundError:
                return 'already verified'
        else:
            # Key is incorrect
            return 'incorrect key'
    except EmailNotFoundError:
        return 'already verified'

@app.route('/unsubscribe', methods=['GET', 'POST'])
def unsubscribe():
    if request.method == 'POST':
        email = request.form.get('email')
        DBHandler.remove_email(db_filename, email)
        return f'unsubscribed {email}'
    else:
        return render_template('unsubscribe.html')

@app.route('/send-cat')
def send_cat():
    pass

"""
@app.route('/book/<book_id>/<chapter_number>')
def get_chapter(book_id, chapter_number):
    try:
        chapter_number = int(chapter_number)
    except ValueError:
        return 'invalid chapter number'
    book = _get_book_from_db(book_id)
    try:
        chapter = book.chapters[chapter_number]
    except IndexError:
        return 'invalid chapter number'
    return render_template('chapter.html', title=book.title, book=book, chapter=chapter)

@app.route('/book/<book_id>')
def get_book(book_id):
    book = _get_book_from_db(book_id)
    return render_template('book.html', book=book)

def _get_book_from_db(book_id):
    book_json = DBHandler.get_book_json(db_filename, book_id)
    if isinstance(book_json, int):
        return f'no book found with id {book_id}'
    try:
        book = json_to_book(book_json)
        book.id = book_id
        return book
    except (TypeError, JSONDecodeError):
        return 'something went wrong'
"""