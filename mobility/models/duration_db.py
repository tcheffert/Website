from mobility.db import get_db

def min_day():
    db = get_db()
    return db.execute("SELECT date(MIN(date)) AS min_day FROM trafic").fetchone()[0]

def max_day():
    db = get_db()
    return db.execute("SELECT date(MAX(date)) AS min_day FROM trafic").fetchone()[0]

def duration(min_date,max_date,rue_id):
    db = get_db()
    return db.execute(
        "SELECT date(trafic.date) as jour, COALESCE(SUM(trafic.lourd),0) as lourd,"
        " COALESCE(SUM(trafic.voiture),0) as voiture, COALESCE(SUM(trafic.velo),0) as velo,"
        " COALESCE(SUM(trafic.pieton),0) as pieton FROM trafic"
        " JOIN rue ON rue.rue_id = trafic.rue_id"
        " WHERE jour BETWEEN ? AND ? AND rue.rue_id = ?"
        ,(min_date,max_date,rue_id)).fetchall()
    