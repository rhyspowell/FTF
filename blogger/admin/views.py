from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask.ext.login import login_required, login_user, logout_user

from .forms import LoginForm, RegistrationForm, AddEntryForm
from .models import User, Entries, MenuItems

admin = Blueprint("admin", __name__, static_folder='static', static_url_path='/static/')

@admin.route('/admin')
@login_required
def adminpage():
    notyetpublished = Entries.query.filter_by(status = 0).order_by(Entries.publishedtime.desc()).items()
    publishedentries = Entries.query.filter_by(status = 1).order_by(Entries.publishedtime.desc()).items()
    menuitems = MenuItems.query.all()

    return render_template('admin/admin.html', publishedentries=publishedentries, notyetpublished=notyetpublished, menuitems=menuitems)

@admin.route('/admin/add-section')
@login_required
def addsection():
    if request.method == 'GET':
        return render_template('admin/add_author.html')
    if request.method =='POST':
        author = Authors(request.form['name'])
        db.session.add(author)
        db.session.commit()
        flash('New author aded to the list')
        return redirect(url_for('show_entries'))

#add a post
@admin.route('/admin/add/', methods=['GET', 'POST'])
@login_required
def addentry():
    form = AddEntryForm()
    if form.validate_on_submit():
        entry = Entries.create(**form.data)
        form.populate_obj(entry)
        flash('New entry was sucessfully posted')
        return redirect(url_for('admin.adminpage'))
    return render_template('admin/addpost.html', form=form)

#login and out methods
#@lm.user_loader
#def load_user(userid):
#   return User.get(userid)

@admin.route('/login/', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Let Flask-Login know that this user
        # has been authenticated and should be
        # associated with the current session.
        login_user(form.user)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("blogger.show_entries"))
    return render_template('login.html', form=form)

@admin.route('/logout/')
@login_required
def logout():
    # Tell Flask-Login to destroy the
    # session->User connection for this session.
    logout_user()
    return redirect(url_for('blogger.show_entries'))

@admin.route('/register/', methods=('GET', 'POST'))
#@login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.create(**form.data)
        form.populate_obj(user)
        login_user(user)
        return redirect(url_for('blogger.show_entries'))
    return render_template('register.html', form=form)
