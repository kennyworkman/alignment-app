import sqlite3
import click
from flask import g, current_app
from flask.cli import with_appcontext

def get_db():
    """Returns a connection with the SQlite DB (a sqlite3 connection object). The connection is ensured to be the same throughout the lifetime of a request
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'] 
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """Removes database connection object from the request context and closes the connection.

    (Note this function is called implicitly by app.teardown_appcontext, thus there is no need to manually call it)
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()

def insert_genes(session, g):
    """Insert gene data into database. Gene data is extracted from the g object that is refreshed after the request has completed.

    The session object provides a unqiue UserID that persists across multiple requests, allowing all user data to be uniquely queried.
    """
    input_data = []
    for gene_name, gene_content in g.gene_dict.items():
        input_data.append((session['user_id'], gene_name, gene_content))

    cur = get_db().executemany('INSERT INTO sequence (user_id, name, bases) VALUES (?,?,?)', input_data)
    get_db().commit()
    cur.close()

def query_genes(session):
    """Pulls all sqlite3 Row Objects from database associated with user. Pass session object as argument. 
    """
    cur = get_db().execute('SELECT * FROM sequence WHERE user_id = ?', (session['user_id'],))
    genes = cur.fetchall()
    cur.close()
    return genes

def wipe_genes(session):
    """Deletes gene data from the database associated with a user. ID extracted from the session object.
    """
    cur = get_db().execute('DELETE FROM sequence WHERE user_id = ?', (session['user_id'],))
    get_db().commit()
    cur.close()

def wipe_all_genes():
    """Deletes all gene data from the database irrespective of any user ID.
    """
    cur = get_db().execute('DELETE FROM sequence;')
    get_db().commit()
    cur.close()

def get_gene_dict(session):
    """Uses the query_genes function to generate a dictionary of all genes stored in the database that are associated with a particular user.
    """
    gene_objects = query_genes(session)

    gene_dict = {}
    for gene_object in gene_objects:
        gene_dict[gene_object['name']] = gene_object['bases']
    return gene_dict


def init_db():
    """Creates a file schema.sql in the instance folder within project root directory. Generates a table defined in the schema.sql file.

    Note: This command is wrapped with the click package. It should be used from the command line.
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        contents = f.read().decode('utf8')  
        db.executescript(contents)
 
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Wrap the init_db as a click command that is callable from the command line.
    """
    init_db()
    click.echo('Initialized the SQLite Database.')

def init_app(app):
    """Registers init_db with the app as a command line command.
    Automatically closes database connection when request has finished, thus no need to manually call close_db
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command) # Adds new command to command line 


