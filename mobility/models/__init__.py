# --- Imports ---#
from mobility.models.city_db import insert_city
from mobility.models.speed_db import insert_speed
from mobility.models.street_db import insert_street
from mobility.models.trafic_db import insert_trafic

# --- Extract all the data from the CSV ---#


def parse_csv_file(file):
    '''
        @pre: a CSV file with mobility data
        @post: insert everything in the file into the database
    '''
    # Open the CSV file
    with open(file, 'r') as f:
        lines = f.readlines()

        # Population data for postal codes
        population_list = {
            '1000': 1046816, '2280': 11015,
            '4000': 187577, '5000': 107178,
            '5100': 20193, '6000': 418000,
            '8500': 75893, '9120': 46410,
            '9550': 16973
        }

        # All the variables
        cities = []
        streets = []
        trafics = []
        speeds = []

        # Loop through each line in the CSV file
        for idx, line in enumerate(lines):
            if idx != 0:
                line = line.strip().split(",")

                # Extract data from the CSV line (cf ugly_csv.csv)
                city_name = line[0]
                postal_code = line[1]
                street_name = line[2]
                street_id = line[3]
                date = line[4]
                lourd = line[5]
                voiture = line[6]
                velo = line[7]
                pieton = line[8]

                # Extracting proportion data
                prop_str = line[-26:-1]
                prop_float = []
                # Handle issues with the subarray v120
                for s in prop_str:
                    s = s.replace('\"', '').replace('[', '').replace(']', '')
                    prop_float.append(float(s))

                v85 = line[-1]

                # Now, we have extract and stored all the data from the csv
                # We need to put them into the database.

                # Insert data into respective tables if not already present
                if city_name not in cities:
                    insert_city(
                        population_list[postal_code], city_name, postal_code)
                    cities.append(city_name)

                if street_id not in streets:
                    insert_street(street_id, street_name, postal_code)
                    streets.append(street_id)

                if (street_id, date) not in trafics:
                    insert_trafic(street_id, date, lourd,
                                  voiture, velo, pieton, v85)
                    trafics.append((street_id, date))

                if (street_id, date, 0, prop_float[0]) not in speeds:
                    # Insert speed data for each time interval (120 => range of 25 : 5*25 = 120)
                    for i in range(25):
                        insert_speed(street_id, date, i, prop_float[i])
                        speeds.append((street_id, date, i, prop_float[i]))
