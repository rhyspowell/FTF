from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask.ext.login import login_required, login_user, logout_user

from .forms import LoginForm, RegistrationForm
from .models import User

admin = Blueprint("admin", __name__, static_folder='static', static_url_path='/static/')

@admin.route('/admin/add-section')
@login_required
def add_section():
    if request.method == 'GET':
        return render_template('admin/add_author.html')
    if request.method =='POST':
        author = Authors(request.form['name'])
        db.session.add(author)
        db.session.commit()
        flash('New author aded to the list')
        return redirect(url_for('show_entries'))

#add a post
@admin.route('/add', methods=['GET', 'POST'])
@login_required
def add_entry():
    if request.method == 'GET':
        if not session.get('logged_in'):
            flash('You need to be logged in to do that')
            return redirect(url_for('show_entries'))
        return render_template('add_post.html')
    if request.method == 'POST':
        g.db.execute('insert into entries (title, text) values (?,?)', [request.form['title'], request.form['text']])
        g.db.commit()
        flash('New entry was sucessfully posted')
        return redirect(url_for('show_entries'))

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
        user = User()
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('tracking.index'))
    return render_template('register.html', form=form)
