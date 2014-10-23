from flask import Flask

from .auth import login_manager
from .data import db
#from .blog.views import blogger
from .admin.views import admin

app = Flask(__name__)
app.config.from_object('config')


# Add the `constants` variable to all Jinja templates.
@app.context_processor
def provide_constants():
    return {"constants": {"TUTORIAL_PART": 1}}

db.init_app(app)

login_manager.init_app(app)

#app.register_blueprint(blogger)
app.register_blueprint(admin)
