from flask import abort, Blueprint, flash, jsonify, Markup, redirect, render_template, request, url_for
from flask.ext.login import current_user, login_required

from blogger.data import query_to_list, db
from blogger.admin.models import Entries

POSTS_PER_PAGE = 2
blogger = Blueprint("blogger", __name__, static_folder='static')


#main page route
@blogger.route('/')
@blogger.route('/<int:page>')
def show_entries(page = 1):
    #cur = g.db.execute('select title, text from entries order by id desc')
    #entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    #cur = g.db.execute('select name, url from menu')
    #menu_items = [dict(name=row[0], url=row[1]) for row in cur.fetchall()]
    #entries = Entries.query.paginate(page, POSTS_PER_PAGE, False)
    entries = Entries.query.all()
    #posts = entries.posts.paginate(page, POSTS_PER_PAGE, False)
    #entries = Entries.query.paginate(page, posts_per_page, False).items
    #menu_items = Menu_Items.query.all()
    #data = query_to_list(entries)
    #results = []

    #try:
        # The header row should not be linked
    #    results = [next(data)]
    #    for row in data:
    #        row = [_make_link(cell) if i == 0 else cell
    #               for i, cell in enumerate(row)]
    #        results.append(row)
    #except StopIteration:
        # This happens when a user has no sites registered yet
        # Since it is expected, we ignore it and carry on.
    #    pass

    #return render_template("tracking/sites.html", sites=results, form=form)
    #return render_template('show_entries.html', entries=entries, menu_items=menu_items)
    return render_template('show_entries.html', entries=entries)
