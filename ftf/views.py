from flask import abort, Blueprint, flash, jsonify, Markup, redirect, render_template, request, url_for
from flask.ext.login import current_user, login_required, login_user, logout_user

from .forms import LoginForm, RegistrationForm, AddEntryForm
from .models import User, Entries, MenuItems
from .data import query_to_list, db


POSTS_PER_PAGE = 5
TITLE = 'The Random Ramblings'

ftf = Blueprint("ftf", __name__)

#main page route
@ftf.route('/')
@ftf.route('/<int:page>')
@ftf.route('/<postlink>')
def show_entries(page=1, postlink=''):
    title = TITLE
    pages = Entries.query.paginate(page, POSTS_PER_PAGE, False)

    if postlink == '':
        entries = Entries.query.filter_by(status = 1).order_by(Entries.publishedtime.desc()).paginate(page, POSTS_PER_PAGE, False).items
    else:
        entries = Entries.query.filter_by(postlink = postlink)
        #raise Exception(postlink)
    menuitems = MenuItems.query.all()

    return render_template('show_entries.html', entries=entries, pages=pages, menuitems=menuitems, title=title)

@ftf.route('/admin')
@login_required
def adminpage():
    notyetpublished = Entries.query.filter_by(status = 0).order_by(Entries.publishedtime.desc())
    publishedentries = Entries.query.filter_by(status = 1).order_by(Entries.publishedtime.desc())
    menuitems = MenuItems.query.all()

    return render_template('admin.html', publishedentries=publishedentries, notyetpublished=notyetpublished, menuitems=menuitems)

@ftf.route('/admin/add-section')
@login_required
def addsection():
    if request.method == 'GET':
        return render_template('add_author.html')
    if request.method =='POST':
        author = Authors(request.form['name'])
        db.session.add(author)
        db.session.commit()
        flash('New author aded to the list')
        return redirect(url_for('show_entries'))

#add a post
@ftf.route('/admin/add/', methods=['GET', 'POST'])
@login_required
def addentry():
    form = AddEntryForm()
    if form.validate_on_submit():
        entry = Entries.create(**form.data)
        form.populate_obj(entry)
        flash('New entry was sucessfully posted')
        return redirect(url_for('.adminpage'))
    return render_template('addpost.html', form=form)

#login and out methods
#@lm.user_loader
#def load_user(userid):
#   return User.get(userid)

@ftf.route('/login/', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Let Flask-Login know that this user
        # has been authenticated and should be
        # associated with the current session.
        login_user(form.user)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for(".show_entries"))
    return render_template('login.html', form=form)

@ftf.route('/logout/')
@login_required
def logout():
    # Tell Flask-Login to destroy the
    # session->User connection for this session.
    logout_user()
    return redirect(url_for('.show_entries'))

@ftf.route('/register/', methods=('GET', 'POST'))
@login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.create(**form.data)
        form.populate_obj(user)
        login_user(user)
        return redirect(url_for('.show_entries'))
    return render_template('register.html', form=form)
