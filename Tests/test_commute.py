from unittest import TestCase
import unittest
from commute import Commute

commute = Commute('commute2_test', 'time_home2downtown', 'time_downtown2home')

class TestCommute(TestCase):
    def test_get_commute_data(self):
        commute.get_commute_data(5000)
        self.assertEqual(round(sum(commute.drive_time_from_home_list), 1), 85639.1)
        self.assertEqual(round(sum(commute.drive_time_to_home_list), 1), 81878.9)

    def test_get_commute_data_by_day(self):
        commute.get_commute_data_by_day(5000, 6)
        self.assertEqual(round(sum(commute.drive_time_from_home_list), 1), 5126.0)
        commute.get_commute_data_by_day(5000, 3)
        self.assertEqual(round(sum(commute.drive_time_to_home_list), 1), 6074.0)

    def test_get_commute_average(self):
        commute.get_commute_average(5000, 0)
        self.assertEqual(round(sum(commute.drive_time_avg_from_home_list), 1), 1588.8)
        commute.get_commute_average(5000, 8)
        self.assertEqual(round(sum(commute.drive_time_avg_to_home_list), 1), 1464.0)
        commute.get_commute_average(5000, 2)
        self.assertEqual(round(sum(commute.drive_time_stdev_from_home_list), 1), 57.9)
        commute.get_commute_average(5000, 9)
        self.assertEqual(round(sum(commute.drive_time_stdev_to_home_list), 1), 50.5)

if __name__ == '__main__':
    unittest.main()
