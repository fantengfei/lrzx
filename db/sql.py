# -*- coding: utf-8 -*-
"""
    sql
    ~~~~~~
    :copyright: (c) 2018 by Taffy.
"""

import os
from sqlite3 import dbapi2 as sqlite3
from flask import g, Flask

app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE = os.path.join(app.root_path, 'database.db')
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db


@app.teardown_appcontext
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()
        # print 'db close'


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), one=False):
    with app.app_context():
        db = get_db()
        cur = g.db.execute(query, args)
        rv = [dict((cur.description[idx][0], value)
            for idx, value in enumerate(row)) for row in cur.fetchall()]
        g.db.commit()
        return (rv[0] if rv else None) if one else rv

