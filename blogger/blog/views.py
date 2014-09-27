from flask import abort, Blueprint, flash, jsonify, Markup, redirect, render_template, request, url_for

from flask.ext.login import current_user, login_required

from blogger.data import query_to_list, db
from blogger.admin.models import Entries, MenuItems

POSTS_PER_PAGE = 5
blogger = Blueprint("blogger", __name__, static_folder='static')
TITLE = 'The Random Ramblings'


#main page route
@blogger.route('/')
@blogger.route('/<int:page>')
def show_entries(page=1):
    title = TITLE
    pages = Entries.query.paginate(page, POSTS_PER_PAGE, False)
    entries = Entries.query.filter_by(status = 1).order_by(Entries.publishedtime.desc()).paginate(page, POSTS_PER_PAGE, False).items
    menuitems = MenuItems.query.all()

    return render_template('show_entries.html', entries=entries, pages=pages, menuitems=menuitems, title=title)

@blogger.route('/<posttitle>')
def showpost(posttitle):
    title = TITLE
    entries = Entries.query.filter_by(title = posttitle)
    menuitems = MenuItems.query.all()

    return render_template('show_entries.html', entries=entries, title=title, pages=1, menuitems=menuitems )
