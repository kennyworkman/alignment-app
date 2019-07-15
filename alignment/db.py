"""
    db
    ~~
    A collection of methods to interact with an SQLite database.
"""

import sqlite3
import click
from flask import g, current_app
from flask.cli import with_appcontext


def get_db():
    """Creates a connection with the SQLite database.

    If a connection already exists in the current request (accessed through the
    Flask g object), the existing connection will be returned.

    :return: an sqlite3 Connection object that can represent the database.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE']
        )
        # Row object mimics tuple and makes querying much easier.
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """Closes a connection with the SQLite database.

    Note
    ----
    This function is called implicitly by app.teardown_appcontext when a
    request has finished. There is therefore no need to explicitly call it.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def insert_genes(session, g):
    """Inserts gene data from the current app context into the SQLite database.

    Gene data is extracted from the gene_dict attribute of the g object
    A UUID is extracted from the Flask session object, that persists across all
    requests.

    :param session: Flask session object
    :param g: Flask g object
    """
    input_data = []
    for gene_name, gene_content in g.gene_dict.items():
        input_data.append((session['user_id'], gene_name, gene_content))

    cur = get_db().executemany('INSERT INTO sequence (user_id, name, bases)'
                               ' VALUES (?,?,?)', input_data)
    get_db().commit()
    cur.close()


def query_genes(session):
    """Querys all genes associated with a unique user.

    The UUID is stored and extracted from the Flask Session object.

    :param session: Flask session object
    :returns: A list of of sqlite3 Row objects, which have intuitive
    tuple-esque behavior. `Docs for sqlite3 Rows'
    <https://docs.python.org/2/library/sqlite3.html#row-object/>`_
    """
    cur = get_db().execute('SELECT * FROM sequence WHERE user_id = ?',
                           (session['user_id'],))
    genes = cur.fetchall()
    cur.close()
    return genes


def wipe_genes(session):
    """Deletes all genes associated with a unique UUID from the session.

    :param session: Flask session object
    """
    cur = get_db().execute('DELETE FROM sequence WHERE user_id = ?',
                            (session['user_id'],))
    get_db().commit()
    cur.close()


def wipe_all_genes():
    """Deletes all gene data from the database (ignores UUID identifier).
    """
    cur = get_db().execute('DELETE FROM sequence;')
    get_db().commit()
    cur.close()


def get_gene_dict(session):
    """Returns a dictionary of queried genes based on the session's unique UUID.

    :param session: Flask session object
    :returns: dict
    """
    gene_objects = query_genes(session)

    gene_dict = {}
    for gene_object in gene_objects:
        gene_dict[gene_object['name']] = gene_object['bases']
    return gene_dict


def init_db():
    """Initializes database as defined in the schema.sql file.

    The schema.sql file is located in the alignment package's root
    directory.

    Note
    ----
    This command is wrapped with the click package. It should be used from the
    command line when configuring a new app.
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        contents = f.read().decode('utf8')
        db.executescript(contents)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Wraps the init_db() function as a click command command."""
    init_db()
    click.echo('Initialized the SQLite Database.')


def init_app(app):
    """Registers Flask app instance with 'init-db' command and adds close_db()
    to the app.teardown_appcontext() stack.

    :param app: a Flask instance

    Note
    ____
    This should never be referenced directly by the user. The app is registered
    in the __init__ module.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
