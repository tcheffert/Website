# --- Imports ---#
from flask import Blueprint, render_template, request
from mobility.models.city_db import get_nom_de_ville, get_streets_for_city
from mobility.models.trafic_db import get_trafic_for_city, get_trafic_for_street_by_day
from mobility.models.street_db import get_street_name
from mobility.models.duration_db import min_day, max_day, duration

# Creating a blueprint named "requests"
bp = Blueprint("requests", __name__,)

# --- Handle the requests from the page requests.html ---#

# Route for handling requests at "/requests"


@bp.route("/requests", methods=("GET", "POST"))
def indexxx():
    '''
      @pre: /
      @post: return every piece of information needed to the requests html
    '''
    # Getting list of the cities from the database with the row into a dictonnary
    cities = [dict(row) for row in get_nom_de_ville()]

    # POST requests
    if request.method == "POST":

        selected_city = request.form["city"]  # Get the city from the form
        # Get the trafic data for the city chosen (converting each row into a dictionary)
        trafic_req = [dict(row) for row in get_trafic_for_city(selected_city)][0]

        # Calculating the percentage of each type of vehicle in the city and store it in trafic
        trafic = {
            "lourd": round(trafic_req["lourd"] / trafic_req["sum"] * 100),
            "voiture": round(trafic_req["voiture"] / trafic_req["sum"] * 100),
            "velo": round(trafic_req["velo"] / trafic_req["sum"] * 100),
            "pieton": round(trafic_req["pieton"] / trafic_req["sum"] * 100)
        }

        # Getting street.s for the selected city
        city_streets = [dict(row) for row in get_streets_for_city(selected_city)]

        # If the request form contains "street", then:
        if "street" in request.form:
        
            # Get the desired street from the form
            selected_street = request.form["street"]
            name_rue = get_street_name(selected_street)  #get the name of the sreet chosen

            # Get the trafic for the desired street by day from the db
            street_trafic_req = [
                dict(row) for row in get_trafic_for_street_by_day(selected_street)
                ]
            street_trafic = {}  # Where we'll store the percentage
            # Calculating percentages of types of vehicule for each day
            for i in street_trafic_req:
                if i["sum"] != 0:
                    street_trafic[i["jour"]] = {
                        "lourd": round(i["lourd"] / i["sum"] * 100),
                        "voiture": round(i["voiture"] / i["sum"] * 100),
                        "velo": round(i["velo"] / i["sum"] * 100),
                        "pieton": round(i["pieton"] / i["sum"] * 100)
                    }
                else:
                    street_trafic[i["jour"]] = {
                        "lourd": 0, "voiture": 0, "velo": 0, "pieton": 0}

            if "day" in request.form:  
                selected_day = request.form["day"]
            else:
                selected_day = "7"

            minimum_day = min_day()
            maximum_day = max_day()

            if "max_date" in request.form:
                min_date = request.form["min_date"]
                max_date = request.form["max_date"]
                street_trafic_for_duration = duration(min_date, max_date, selected_street)
                
        # Finally, render the template with all the datas that we have calculated
        return render_template("requests.html", **locals())

    else:
        # GET requests (initial page without having choose nothing)
        return render_template("requests.html", cities=cities)
