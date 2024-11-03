from mobility.db import get_db


def get_city_list():
    '''
       @pre: /
       @post: return a list of every cities (city name, population and postal code)
          in the ville table of the database
    '''
    db = get_db()
    return db.execute('SELECT * FROM ville')


def get_cities_number():
    '''
       @pre: /
       @post: return the number of records in the ville table
    '''
    db = get_db()
    result = db.execute('SELECT COUNT(*) FROM ville').fetchone()[0]
    return result


def insert_city(population, nom, code_postal):
    '''
       @pre: a city name, population and postal code
       @post: insert a given city with it's population 
          and postal code into the ville table of the database
    '''
    db = get_db()
    db.execute('INSERT INTO ville (population, nom, code_postal) VALUES (?, ?, ?)',
               (population, nom, code_postal)
               )
    db.commit()


def get_nom_de_ville():
    '''
       @pre: /
       @post: return the name of every cities in the ville table of the database
    '''
    db = get_db()
    return db.execute('SELECT DISTINCT nom FROM ville').fetchall()


def get_streets_for_city(city):
    '''
       @pre: a city name
       @post: get every streets name and id in the rue table of the database for a given city
    '''
    db = get_db()
    return db.execute(
        "SELECT rue.nom, rue.rue_id FROM rue"
        " JOIN ville ON (ville.nom = ? AND ville.code_postal = rue.code_postal)",
        (city,)
    ).fetchall()



def get_code_postal_ville(name):
    db = get_db()
    return db.execute('SELECT ville.code_postal FROM ville WHERE nom=?', (name,)).fetchone()[0]
