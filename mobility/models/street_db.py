from mobility.db import get_db


def get_streets_number():
    '''
        @pre: /
        @post: return the number of records in the rue table of the database
    '''
    db = get_db()
    return db.execute('SELECT COUNT(*) FROM rue').fetchone()[0]


def insert_street(id, nom, code_postal):
    '''
        @pre: a street id, name and postal code
        @post: insert a records in the rue table of the database with the given arguments
    '''
    db = get_db()
    db.execute(
        'INSERT INTO rue (rue_id, nom, code_postal) VALUES (?, ?, ?)',
        (id, nom, code_postal)
    )
    db.commit()


def streets_per_city():
    '''
        @pre: /
        @post: return the number of streets for every cities
    '''
    db = get_db()
    return db.execute(
        'SELECT ville.nom, COUNT(rue.nom) as nombre FROM rue'
        ' JOIN ville ON ville.code_postal = rue.code_postal'
        ' GROUP BY ville.nom'
    ).fetchall()

def get_street_name(rue_id):
    db = get_db()
    return db.execute('SELECT rue.nom FROM rue WHERE rue_id=?', (rue_id,)).fetchone()[0]
