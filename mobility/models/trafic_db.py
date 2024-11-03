from mobility.db import get_db


def get_trafic_number():
    '''
        @pre: /
        @post: return the number of records in trafic table of the database
    '''
    db = get_db()
    return db.execute('SELECT COUNT(*) FROM trafic').fetchone()[0]


def insert_trafic(rue_id, date, lourd, voiture, velo, pieton, v85):
    '''
        @pre: a street id with a date and all the trafic 
          for every vehicule in this street with the v85
        @post: insert a record in the trafic table of the database
    '''
    db = get_db()
    db.execute(
        'INSERT INTO trafic (rue_id, date, lourd, voiture, velo, pieton, v85) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (rue_id, date, round(float(lourd)), round(float(voiture)),
         round(float(velo)), round(float(pieton)), v85)
    )
    db.commit()


def most_cyclable_cities():
    '''
        @pre: /
        @post: return the cycling proportion of every cities in the ville table of the database
    '''
    db = get_db()
    return db.execute(
        'SELECT ville.nom, round(((SUM(trafic.velo * 1.0)) / (ville.population * 1000)) * 100, 2) as nombre FROM trafic'
        ' JOIN rue ON rue.rue_id = trafic.rue_id'
        ' JOIN ville ON ville.code_postal = rue.code_postal'
        ' GROUP BY ville.nom'
        ' ORDER BY nombre DESC'
    ).fetchall()


def get_trafic_for_city(city):
    '''
        @pre: a city name
        @post: return the sum of every trafic by vehicule in a given city
    '''
    db = get_db()
    return db.execute(
        'SELECT SUM(trafic.lourd) as lourd, SUM(trafic.voiture) as voiture,'
        ' SUM(trafic.velo) as velo, SUM(trafic.pieton) as pieton,'
        ' SUM(trafic.lourd+trafic.voiture+trafic.velo+trafic.pieton) as sum FROM trafic'
        ' JOIN rue ON rue.rue_id = trafic.rue_id'
        ' JOIN ville ON ville.code_postal = rue.code_postal'
        ' WHERE ville.nom = ?'
        ' ORDER BY trafic.date ASC',
        (city,)
    ).fetchall()


def get_trafic_for_street_by_day(street):
    '''
        @pre: a street id
        @post: return the sum of trafic for each vehicule type by weekdays
    '''
    db = get_db()
    return db.execute(
        "SELECT strftime('%w', trafic.date) as jour, SUM(trafic.lourd) as lourd,"
        " SUM(trafic.voiture) as voiture, SUM(trafic.velo) as velo,"
        " SUM(trafic.pieton) as pieton,"
        " SUM(trafic.lourd + trafic.voiture + trafic.velo + trafic.pieton) as sum FROM trafic"
        " JOIN rue ON rue.rue_id = trafic.rue_id"
        " WHERE rue.rue_id = ?"
        " GROUP BY strftime('%w', trafic.date)",
        (street,)
    ).fetchall()

def get_cyclists_by_day():
    '''
        @pre: /
        @post: return the sum of trafic in every cities by days
    '''
    db = get_db()
    return db.execute(
        "SELECT strftime('%Y/%m/%d', trafic.date) as date, SUM(trafic.velo) as velo"
        " FROM trafic GROUP BY strftime('%Y/%m/%d', trafic.date)"
    ).fetchall()
