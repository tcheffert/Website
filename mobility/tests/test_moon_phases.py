import unittest
from mobility.moon_phases import *
from datetime import datetime


class MoonPhasesTestCase(unittest.TestCase):

    # Test each phase of the moon.
    def test_phase(self):


        # Set the date for each moon phase
        new = datetime(2023, 2, 20, 0, 0, 0)
        waxing_crescent = datetime(2023, 3, 25)
        first = datetime(2023, 3, 29)
        waxing_gibbous = datetime(2023, 4, 2)
        full = datetime(2023, 4, 6)
        waning_gibbous = datetime(2023, 4, 9)
        last = datetime(2023, 4, 13)
        waning_crescent = datetime(2023, 3, 17)

        # Set the result
        result_new = phase(age(new))
        result_waxing_crescent = phase(age(waxing_crescent))
        result_first = phase(age(first))
        result_waxing_gibbous = phase(age(waxing_gibbous))
        result_full = phase(age(full))
        result_waning_gibbous = phase(age(waning_gibbous))
        result_last = phase(age(last))
        result_waning_crescent = phase(age(waning_crescent))

        # Set the expected phase
        expected_new = MoonPhase.NEW_MOON
        expected_waxing_crescent = MoonPhase.WAXING_CRESCENT
        expected_first = MoonPhase.FIRST_QUARTER
        expected_waxing_gibbous = MoonPhase.WAXING_GIBBOUS
        expected_full = MoonPhase.FULL_MOON
        expected_waning_gibbous = MoonPhase.WANING_GIBBOUS
        expected_last = MoonPhase.LAST_QUARTER
        expected_waning_crescent = MoonPhase.WANING_CRESCENT

        # checks if the result obtained is expected
        # test phase with assert calls
        self.assertEqual(result_new, expected_new,
                         msg=f'Error: Expected {expected_new}, but got {result_new}')
        self.assertEqual(result_waxing_crescent, expected_waxing_crescent,
                         msg=f'Error: Expected {expected_waxing_crescent}, but got {result_waxing_crescent}')
        self.assertEqual(result_first, expected_first,
                         msg=f'Error: Expected {expected_first}, but got {result_first}')
        self.assertEqual(result_waxing_gibbous, expected_waxing_gibbous,
                         msg=f'Error: Expected {expected_waxing_gibbous}, but got {result_waxing_gibbous}')
        self.assertEqual(result_full, expected_full,
                         msg=f'Error: Expected {expected_full}, but got {result_full}')
        self.assertEqual(result_waning_gibbous, expected_waning_gibbous,
                         msg=f'Error: Expected {expected_waning_gibbous}, but got {result_waning_gibbous}')
        self.assertEqual(result_last, expected_last,
                         msg=f'Error: Expected {expected_last}, but got {result_last}')
        self.assertEqual(result_waning_crescent, expected_waning_crescent,
                         msg=f'Error: Expected {expected_waning_crescent}, but got {result_waning_crescent}')


if __name__ == '__main__':
    unittest.main(verbosity=2)
