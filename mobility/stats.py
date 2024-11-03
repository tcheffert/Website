from flask import Blueprint, render_template
from datetime import datetime
from mobility.models.street_db import streets_per_city, get_streets_number
from mobility.models.city_db import get_cities_number, get_code_postal_ville
from mobility.models.speed_db import get_speed_number
from mobility.models.trafic_db import get_trafic_number, get_cyclists_by_day, most_cyclable_cities
from mobility.moon_phases import *
from mobility.models.trafic_db import get_trafic_number, most_cyclable_cities

bp = Blueprint("stats", __name__)

def get_province(code_postal):
    if code_postal >= 1000 and code_postal <= 1299:
        return "Bruxelles-Capitale"
    elif code_postal >= 2000 and code_postal <= 2999:
        return "Anvers"
    elif code_postal >= 4000 and code_postal <= 4999:
        return "Liège"
    elif code_postal >= 5000 and code_postal <= 5680:
        return "Namur"
    elif code_postal >= 6000 and code_postal <= 6599:
        return "Hainaut"
    elif code_postal >= 8000 and code_postal <= 8999:
        return "Flandre-Occidentale"
    elif code_postal >= 9000 and code_postal <= 9999:
        return "Flandre-Orientale"
    else:
        return "Not found"

@bp.route("/stats")
def get_stats():
    '''
      @pre: /
      @post: return the statistics needed by the stats html
    '''

    # create a list of dictionnaries with the sum of trafic in every cities by days
    cbd = [dict(row) for row in get_cyclists_by_day()]
    cyclists_per_moon_phase = {
        "full": 0,
        "not_full": 0,
        "ratio": 0
    }
    # take the year, month and day out of the date in every dictionnaries of the list cbd
    # then
    for row in cbd:
        year = row["date"].split("/")[0]
        month = row["date"].split("/")[1]
        day = row["date"].split("/")[2]
        # calcul the moon phase
        moon_phase = phase(age(datetime(int(year), int(month), int(day))))

        # sort the trafic between the trafic with a full moon and the trafic without it
        if moon_phase == MoonPhase.FULL_MOON:
            cyclists_per_moon_phase["full"] += row["velo"]
        else:
            cyclists_per_moon_phase["not_full"] += row["velo"]

    # calcul the ratio between the trafic with a full moon and the trafic without it
    cyclists_per_moon_phase["ratio"] = round(
        cyclists_per_moon_phase["full"] /
        cyclists_per_moon_phase["not_full"] * 100,
        2
    )
    city_streets = streets_per_city()
    streetsNumber = get_streets_number()
    citiesNumber = get_cities_number()
    speedNumber = get_speed_number()
    traficNumber = get_trafic_number()
    most_cyclables = most_cyclable_cities()
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #---Get the variable in the correct format for ChartJS---#
    #First graph (stats.html)
    lst_cities = []
    lst_percent = []
    for city, percent in most_cyclables:
        lst_cities.append(city)
        lst_percent.append(percent)
    #Second graph (stats.html)
    lst_villes_graph2 = []
    nbr_rues_ville = []
    for row in city_streets:
        lst_villes_graph2.append(row[0])
        nbr_rues_ville.append(row[1])

     #---Complete the province dictionnary---#
    villes_provinces = {
        "Namur": 0, "Flandre-Orientale": 0,"Flandre-Occidentale": 0,
         "Anvers": 0, "Liège": 0, "Bruxelles-Capitale": 0, "Hainaut": 0
        }
    for ville in lst_cities:
        code = get_code_postal_ville(ville)
        villes_provinces[get_province(code)] += 1

    #Get all variables for the provinces graph
    lst_provinces = []
    nbr_villes_provinces = []
    for key in villes_provinces:
        lst_provinces.append(key)
        nbr_villes_provinces.append(villes_provinces[key])


    #---Render template with all the variables---#
    return render_template("stats.html", **locals())
