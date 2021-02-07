from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User


@main.route("/", methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        _user = User.query.filter_by(username=form.name.data).first()
        if _user is None:
            _user = User(username=form.name.data)
            db.session.add(_user)
            db.session.commit()
            session['known'] = False
            # if main.config['FLASKY_ADMIN']:
            #     send_email(main.config['FLASKY_ADMIN'], "New User",
            #                "mail/new_user", user=_user)
        else:
            session['known'] = True

        session['name'] = form.name.data
        form.name.data = ""

        return redirect(url_for(".index"))

    return render_template("index.html",
                           form=form,
                           name=session.get("name"),
                           known=session.get("known", False),
                           current_time=datetime.utcnow()
                           )


@main.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name)
