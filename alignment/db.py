import sqlite3
import click
from flask import g, current_app
from flask.cli import with_appcontext

def get_db():
# Save database connection in Request Context
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'] 
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
# Close connection with db if in Request Context
    db = g.pop('db', None)

    if db is not None:
        db.close()

def insert_genes(session, g):
    """ Insert gene data into database. Pass session object as argument.     
    """
    input_data = (session['user_id'], g.gene_name, g.gene_content)
    cur = get_db().execute('INSERT INTO sequence (user_id, name, bases) VALUES (?,?,?)', input_data)
    get_db().commit()
    cur.close()

def query_genes(session):
    """ Pulls all sqlite3 Row Objects from database associated with user. Pass session object as argument. 
    """
    cur = get_db().execute('SELECT * FROM sequence WHERE user_id = ?', (session['user_id'],))
    genes = cur.fetchall()
    cur.close()
    return genes

def get_gene_dict(session, quantity=2):
    """
    """
    gene_objects = query_genes(session)
    if quantity > len(gene_objects):
        return "Insufficient genes stored in database. You requested {} genes and there are {} genes in the database.".format(quantity, len(gene_objects))

    gene_dict = {}
    for i in range(quantity):
        row_object = gene_objects[i]
        gene_dict[row_object['name']] = row_object['bases']
    return gene_dict

def wipe_genes():
    """ Deletes gene data from the database.
    """
    cur = get_db().execute('DELETE FROM sequence')
    get_db().commit()
    cur.close()

def init_db():
# Initialize database based on schema
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        contents = f.read().decode('utf8')  
        db.executescript(contents)
 
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the SQLite Database.')

def init_app(app):
    """Registers init command line with app;
    Automatically closes database connection when request has finished
    """
    app.teardown_appcontext(close_db)
    # Adds new command to command line 
    app.cli.add_command(init_db_command)


