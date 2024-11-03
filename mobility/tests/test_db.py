import os
import tempfile
import unittest

from mobility import create_app
from mobility.db import get_db, close_db
from mobility.models import city_db, speed_db, street_db, trafic_db , duration_db


class TestUser(unittest.TestCase):
    ''' test the sql requests and the data base '''

    def setUp(self):
        # generate a temporary file for the test db
        self.db_fd, self.db_path = tempfile.mkstemp()
        # create the testapp with the temp file for the test db
        self.app = create_app({'TESTING': True, 'DATABASE': self.db_path})
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db = get_db()

        # read in SQL for populating test data
        with open(os.path.join(os.path.dirname(__file__), "schema_test.sql"), "rb") as f:
            self.db.executescript(f.read().decode("utf8"))

    def tearDown(self):
        # closing the db and cleaning the temp file
        close_db()
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_insert_city(self):
        # Insert a new city
        city_db.insert_city(population=13296, nom='Dinant', code_postal='5500')

        # Get the list of cities after insertion
        cities = city_db.get_city_list()

        # Extracting city data from sqlite3.Row objects
        city_data = [(row['population'], row['nom'], row['code_postal']) for row in cities]

        # Check if the inserted city is in the list
        self.assertIn((13296, 'Dinant', 5500), city_data)

    def test_get_city_list(self):
        # Insert some cities
        self.db.execute("""INSERT INTO ville (population, nom, code_postal)
                            VALUES
                            (250000, 'Liège', 4000),
                            (100000, 'Namur', 5000);""")
        # Check if the number of the cities are returned correctly
        number_of_cities = city_db.get_cities_number()

        # Define the expected number of cities
        expected_number_of_cities = 2
        # Check if the returned number of cities matches the expected value
        self.assertEqual(number_of_cities, expected_number_of_cities, "Number of cities does not match")

    def test_get_nom_de_ville(self):
        # Insert some cities
        self.db.execute("""INSERT INTO ville (population, nom, code_postal)
                            VALUES
                            (250000, 'Liège', 4000),
                            (100000, 'Namur', 5000);""")
        # Check if the names of the cities are returned correctly
        city_names = [row[0] for row in city_db.get_nom_de_ville()]

        # Define the expected names of cities
        expected_names = ['Liège', 'Namur']
        # Check if the returned names of cities matches the expected value
        self.assertCountEqual(city_names, expected_names)

    def test_get_streets_for_city(self):
        # Insert streets and a city into the database
        self.db.execute("""INSERT INTO rue (rue_id, nom, code_postal)
                              VALUES
                              (1, 'Rue Saint-Jacques', '5500'),
                              (2, 'Rue Coster', '5500');""")
        self.db.execute("""INSERT INTO ville (population, nom, code_postal)
                               VALUES
                               (13296, 'Dinant', '5500');""")
        # Call the get_streets_for_city function for the city 'Dinant'
        streets = city_db.get_streets_for_city('Dinant')

        # Extracting street names and IDs from sqlite3.Row objects
        street_data = [(row[0], row[1]) for row in streets]

        # Check if the extracted street data matches the expected streets
        expected_streets = [('Rue Saint-Jacques', 1), ('Rue Coster', 2)]
        self.assertEqual(street_data, expected_streets)

    def get_streets_for_city(self):
        # Insert streets and a city into the database
        self.db.execute("""INSERT INTO ville (population, nom, code_postal)
                                    VALUES
                                    (250000, 'Liège', 4000),
                                    (100000, 'Namur', 5000);""")
        # Call the get_code_postal_ville function for the city 'Namur'
        code_postal = city_db.get_code_postal_ville('Namur')
        expected_code_postal= 5000
        # Check if the extracted code_postal data matches the expected code_postal
        self.assertEqual(expected_code_postal, code_postal)


    def test_insert_speed(self):
        # insertion speed
        speed_db.insert_speed(1, date='2024-03-26', tranche_vitesse='4', proportion=0)
        speed_db.insert_speed(2, date='2024-03-26', tranche_vitesse='2', proportion=100)
        speed_db.insert_speed(3, date='2024-03-26', tranche_vitesse='9', proportion=0)

        # Get the number of speed records after insertion
        speed_number = speed_db.get_speed_number()
        # Define the expected number of speed
        expected_number = 3
        # Check if the returned speed number is as expected
        self.assertEqual(speed_number, expected_number)

    def test_insert_street(self):
        # insertion speed
        street_db.insert_street(id=1, nom='Rue Saint-Jacques', code_postal=5500)
        street_db.insert_street(id=2, nom='Rue Coster', code_postal=5500)

        # Get the number of speed records after insertion
        street_number = street_db.get_streets_number()

        # Define the expected number of street
        expected_number = 2

        # Check if the returned street number is as expected
        self.assertEqual(street_number, expected_number)

    def test_streets_per_city(self):
        # insert streets and city
        street_db.insert_street(id=1, nom='Rue Saint-Jacques', code_postal=5500)
        street_db.insert_street(id=2, nom='Rue Coster', code_postal=5500)
        city_db.insert_city(population=13296, nom='Dinant', code_postal='5500')

        # Call the function under test to get streets per city
        street_per_city = street_db.streets_per_city()

        # Transform the data obtained from the function
        transformed_data = [(row[0], row[1]) for row in street_per_city]

        expected_result = [('Dinant', 2)]

        # Check if the transformed data matches the expected result
        self.assertEqual(transformed_data, expected_result)
    def test_get_street_name(self):
        # insert streets
        street_db.insert_street(id=1, nom='Rue Saint-Jacques', code_postal=5500)
        street_db.insert_street(id=2, nom='Rue Coster', code_postal=5500)
        # Call the function to get street name
        street_name = street_db.get_street_name(1)
        expected_name= 'Rue Saint-Jacques'
        # Check if the returned street name is as expected
        self.assertEqual(street_name, expected_name)


    def test_insert_trafic(self):
        # insertion trafic
        trafic_db.insert_trafic(rue_id=1, date='2024-03-26', lourd=round(2.32323), voiture=round(8.1233123),
                                velo=round(4.1233123), pieton=round(2.232323), v85=41.5)
        trafic_db.insert_trafic(rue_id=2, date='2024-03-26', lourd=round(12.32323), voiture=round(12.1233123),
                                velo=round(3.1233123), pieton=round(2.232323), v85=72.5)

        # Get the number of trafic records after insertion
        trafic_number = trafic_db.get_trafic_number()

        # Check if the returned speed number is as expected
        self.assertEqual(trafic_number, 2)

    def test_most_cyclable_cities(self):
        trafic_db.insert_trafic(rue_id=1, date='2024-03-26', lourd=round(2.32323), voiture=round(8.1233123),
                                velo=round(4.1233123), pieton=round(2.232323), v85=41.5)
        trafic_db.insert_trafic(rue_id=2, date='2024-03-26', lourd=round(12.32323), voiture=round(12.1233123),
                                velo=round(3.1233123), pieton=round(2.232323), v85=72.5)
        street_db.insert_street(id=1, nom='Rue Saint-Jacques', code_postal=5500)
        street_db.insert_street(id=2, nom='Rue Coster', code_postal=5500)
        city_db.insert_city(population=13296, nom='Dinant', code_postal='5500')

        most_cyclable_cities = trafic_db.most_cyclable_cities()
        transformed_data = [(row[0], row[1]) for row in most_cyclable_cities]
        expected_result = [('Dinant', 0.0)]
        self.assertEqual(transformed_data, expected_result)

    def test_get_trafic_for_city(self):
        # Insert streets, city, and traffic into the database
        self.db.execute("""INSERT INTO rue (rue_id, nom, code_postal)
                                      VALUES
                                      (1, 'Rue Saint-Jacques', '5500'),
                                      (2, 'Rue Coster', '5500');""")
        self.db.execute("""INSERT INTO ville (population, nom, code_postal)
                                       VALUES
                                       (13296, 'Dinant', '5500');""")
        self.db.execute("""INSERT INTO trafic (rue_id, date, lourd, voiture, velo, pieton, v85)
                                       VALUES
                                       (1, '2024-03-26', round(2.32323), round(8.1233123), round(4.1233123), round(2.232323), 41.5),
                                       (2, '2024-03-26', round(12.32323), round(12.1233123), round(3.1233123), round(2.232323), 72.5);""")

        # Call the get_trafic_for_city function for the city 'Dinant'
        trafics = trafic_db.get_trafic_for_city('Dinant')

        # Extracting traffic from sqlite3.Row objects
        trafic_data = [(row[0], row[1], row[2], row[3]) for row in trafics]

        # Check if the extracted traffic data matches the expected traffic sum
        expected_trafic = [(14, 20, 7, 4)]  # Adjust the expected sum as per your data
        self.assertEqual(trafic_data, expected_trafic)

    def test_get_trafic_for_street_by_day(self):
        # Insert streets and traffic into the database
        self.db.execute("""INSERT INTO rue (rue_id, nom, code_postal)
                                              VALUES
                                              (1, 'Rue Saint-Jacques', '5500'),
                                              (2, 'Rue Coster', '5500');""")
        self.db.execute("""INSERT INTO trafic (rue_id, date, lourd, voiture, velo, pieton, v85)
                                               VALUES
                                               (1, '2024-03-26', round(2.32323), round(8.1233123), round(4.1233123), round(2.732323), 41.5),
                                               (1, '2024-03-15', round(3.32323), round(2.1233123), round(3.1233123), round(2.232323), 41.5),
                                               (2, '2024-03-26', round(12.32323), round(12.1233123), round(3.1233123), round(2.232323), 72.5);""")
        # Call the get_trafic_for_street_by_day function for the street_id '1'
        trafics = trafic_db.get_trafic_for_street_by_day(1)
        trafic_data = [(row[0], row[1], row[2], row[3], row[4]) for row in trafics]
        expected_trafic = [('2', 2, 8, 4, 3), ('5', 3, 2, 3, 2)]
        # Check if the extracted traffic data matches the expected traffic sum
        self.assertEqual(trafic_data, expected_trafic)

    def test_get_cyclists_by_day(self):
        # Insert traffic into the database
        self.db.execute("""INSERT INTO trafic (rue_id, date, lourd, voiture, velo, pieton, v85)
                                                       VALUES
                                                       (1, '2024-03-26', round(2.32323), round(8.1233123), round(4.1233123), round(2.732323), 41.5),
                                                       (1, '2024-03-15', round(3.32323), round(2.1233123), round(3.1233123), round(2.232323), 41.5),
                                                       (2, '2024-03-26', round(12.32323), round(12.1233123), round(3.1233123), round(2.232323), 72.5);""")
        # Call the get_cyclists_by_day function
        velo = trafic_db.get_cyclists_by_day()
        velo_data = [(row[0], row[1]) for row in velo]
        expected_trafic = [('2024/03/15', 3), ('2024/03/26', 7)]
        # Check if the extracted velo data matches the expected velo sum
        self.assertEqual(velo_data, expected_trafic)

    def test_min_day(self):
        # Insert traffic into the database
        self.db.execute("""INSERT INTO trafic (rue_id, date, lourd, voiture, velo, pieton, v85)
                                                               VALUES
                                                               (1, '2024-03-26', round(2.32323), round(8.1233123), round(4.1233123), round(2.732323), 41.5),
                                                               (1, '2024-03-15', round(3.32323), round(2.1233123), round(3.1233123), round(2.232323), 41.5),
                                                               (2, '2024-03-26', round(12.32323), round(12.1233123), round(3.1233123), round(2.232323), 72.5);""")
        min_date= '2024-03-15'
        # Call the min_day function
        expected_date= duration_db.min_day()
        # Check if the extracted date data matches the expected date
        self.assertEqual(min_date, expected_date)

    def test_max_day(self):
        # Insert traffic into the database
        self.db.execute("""INSERT INTO trafic (rue_id, date, lourd, voiture, velo, pieton, v85)
                                                               VALUES
                                                               (1, '2024-03-26', round(2.32323), round(8.1233123), round(4.1233123), round(2.732323), 41.5),
                                                               (1, '2024-03-15', round(3.32323), round(2.1233123), round(3.1233123), round(2.232323), 41.5),
                                                               (2, '2024-03-26', round(12.32323), round(12.1233123), round(3.1233123), round(2.232323), 72.5);""")
        max_date= '2024-03-26'
        # Call the max_day function
        expected_date= duration_db.max_day()
        # Check if the extracted date data matches the expected date
        self.assertEqual(max_date, expected_date)

    def test_duration(self):
        # Insert traffic into the database
        self.db.execute("""INSERT INTO trafic (rue_id, date, lourd, voiture, velo, pieton, v85)
                                                                       VALUES
                                                                       (1, '2024-03-26', round(2.32323), round(8.1233123), round(4.1233123), round(2.732323), 41.5),
                                                                       (1, '2024-03-29', round(2.32323), round(8.1233123), round(4.1233123), round(2.732323), 41.5),
                                                                       (1, '2024-03-15', round(3.32323), round(2.1233123), round(3.1233123), round(2.232323), 41.5),
                                                                       (2, '2024-03-26', round(12.32323), round(12.1233123), round(3.1233123), round(2.232323), 72.5);""")
        min_date = '2024-03-15'
        max_date = '2024-03-26'
        rue_id = 1
        # Call the duration function
        result = duration_db.duration(min_date, max_date, rue_id)
        expected_result = [(1, '2024-03-15', round(3.32323), round(2.1233123), round(3.1233123), round(2.232323), 41.5),
                           (1, '2024-03-26', round(2.32323), round(8.1233123), round(4.1233123), round(2.732323), 41.5)]
        # Check if the extracted  data matches the expected data
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main(verbosity=2)
