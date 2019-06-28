from flask import g, session
import os

from alignment.db import *

def test_get_db(app, client):
    """Ensure proper database connection behavior. Connections should persist across Requests, and be closed automatically upon the completion of a request
    """
    with app.test_request_context():
        db = get_db()
        assert db is get_db(), "Database connection shouldn't change within a Request Context"

        client.get('/')
        assert 'db' in g, "g object should store database connection during a Request"
    
    # Same request, but in a new request context without opening a new connection.
    with app.app_context():
        assert 'db' not in g, "Connection should automatically close and remove itself from g after a Request" 



def test_db_behavior(app, client):
    """Ensure proper database insertion behavior. Genes are pulled from the g object and identified by the UID from the session object and persisted to SQLite DB.

    Also ensure querying and wiping behavior. The query_genes function should return all gene data associated with a user across requests.
    """
    with client:
        client.get('/')
        session['user_id'] = 'test'
        g.gene_dict['gene1'] = 'ATT'

        insert_genes(session, g)
        
        query = get_db().execute('SELECT * FROM SEQUENCE WHERE user_id = ?', ("test",)).fetchone()
        assert all(x in [1, 'test', 'gene1', 'ATT'] for x in query), "insert_genes function doesn't correctly insert genes into DB."

        one_query = query_genes(session)
        assert len(one_query) is 1, "Should only be one row queried."
        assert len(one_query[0]) is 4, "Should only be four items in a row."
        assert all(x in [1, 'test', 'gene1', 'ATT'] for x in one_query[0]), "query_genes doesn't retrieve correct genes."

        client.get('/')
        session['user_id'] = 'test'
        g.gene_dict = {'gene2': 'AAA',
                       'gene3': 'TTT'}
        insert_genes(session, g)

        multi_query = query_genes(session)
        assert len(multi_query) is 3, "Should be three rows in this query"
        assert all(x in [1, 'test', 'gene1', 'ATT'] for x in multi_query[0]), "query_genes doesn't retrieve correct genes."
        assert all(x in [2, 'test', 'gene2', 'AAA'] for x in multi_query[1]), "query_genes doesn't retrieve correct genes."
        assert all(x in [3, 'test', 'gene3', 'TTT'] for x in multi_query[2]), "query_genes doesn't retrieve correct genes."

        wipe_genes(session)
        assert len(query_genes(session)) is 0, "wipe_genes function does not work correctly."

        session['user_id'] = 'dont_delete'
        g.gene_dict = {'please_dont_delete_this_gene': 'ATT'}
        insert_genes(session, g)

        session['user_id'] = 'delete'
        g.gene_dict = {'please_delete_this_gene' : 'TTT'}
        insert_genes(session, g)

        wipe_genes(session)
        assert len(get_db().execute('SELECT * FROM sequence;').fetchall()) is 1, "wipe_genes function doesn't discriminate between unique IDs." 

        wipe_all_genes() 
        assert len(get_db().execute('SELECT * FROM sequence;').fetchall()) is 0, "wipe_all_genes function doesn't wipe the database." 

    
def test_get_gene_dict(app, client):
    """This function should generate a dictionary of all the genes associated with a user within the database
    """
    with client:
        client.get('/')
        g.gene_dict['gene1'] = 'ATT'
        insert_genes(session, g)

        gene_dict = get_gene_dict(session)
        assert(len(gene_dict)) is 1, "gene_dict function returns a dictionary with incorrect content."
        
        g.gene_dict = {'gene2': 'AAA',
                       'gene3': 'TTT'}
        insert_genes(session, g)

        gene_dict = get_gene_dict(session)
        assert(len(gene_dict)) is 3, "gene_dict function returns a dictionary with incorrect content."


def test_init_db(app):
    """Ensure the init_db function works as intended when used as a command line argument.
    """
    with app.test_request_context():
        init_db()
        assert os.path.exists(app.config['DATABASE']), "Database file hasn't been created."

