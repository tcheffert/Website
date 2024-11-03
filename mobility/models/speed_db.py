from mobility.db import get_db


def get_speed_number():
    '''
      @pre: /
      @post: return the number of records in the vitesse table
    '''
    db = get_db()
    result = db.execute('SELECT COUNT(*) FROM vitesse').fetchone()[0]
    return result


def insert_speed(rue_id, date, tranche_vitesse, proportion):
    '''
      @pre: a street id, a date, a speed array and a proportion
      @post: insert a record in the vitesse table of the database
    '''
    db = get_db()
    db.execute('INSERT INTO vitesse (rue_id, date, tranche_de_vitesse, proportion) VALUES (?, ?, ?, ?)',
               (rue_id, date, tranche_vitesse, proportion))
    db.commit()
