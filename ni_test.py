from freezegun import freeze_time
from clock import Time
import unittest


class TestStringMethods(unittest.TestCase):
    def test_day_change(self):
        with freeze_time("2012-01-14 14:59:59"):
            timer = Time()
            self.assertFalse(timer.isDayChange())

        with freeze_time("2012-01-14 15:00:00"):
            self.assertTrue(timer.isDayChange())

        with freeze_time("2012-01-14 15:00:01"):
            self.assertFalse(timer.isDayChange())

    def test_nowTime(self):
        with freeze_time("2012-01-14 15:00:00"):
            timer = Time()
            self.assertEqual(timer.getTime(), '00:00:00')

    def test_nowTime1(self):
        with freeze_time("2012-01-14 16:00:00"):
            timer = Time()
            self.assertEqual(timer.getTime(), '01:00:00')

    def test_nowTime2(self):
        with freeze_time("2012-01-15 00:00:00"):
            timer = Time()
            self.assertEqual(timer.getTime(), '09:00:00')


if __name__ == '__main__':
    unittest.main()
