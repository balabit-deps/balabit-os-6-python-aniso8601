# -*- coding: utf-8 -*-

#Copyright 2013 Brandon Nielsen
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import datetime

from aniso8601.interval import parse_interval, parse_repeating_interval

class TestIntervalFunctions(unittest.TestCase):
    def test_parse_interval(self):
        resultinterval = parse_interval('P1M/1981-04-05T01:01:00')
        self.assertEqual(resultinterval[0], datetime.datetime(year=1981, month=4, day=5, hour=1, minute=1))
        self.assertEqual(resultinterval[1], datetime.datetime(year=1981, month=3, day=6, hour=1, minute=1))

        resultinterval = parse_interval('P1M/1981-04-05')
        self.assertEqual(resultinterval[0], datetime.date(year=1981, month=4, day=5))
        self.assertEqual(resultinterval[1], datetime.date(year=1981, month=3, day=6))

        resultinterval = parse_interval('1981-04-05T01:01:00/P1M1DT1M')
        self.assertEqual(resultinterval[0], datetime.datetime(year=1981, month=4, day=5, hour=1, minute=1))
        self.assertEqual(resultinterval[1], datetime.datetime(year=1981, month=5, day=6, hour=1, minute=2))

        resultinterval = parse_interval('1981-04-05/P1M1D')
        self.assertEqual(resultinterval[0], datetime.date(year=1981, month=4, day=5))
        self.assertEqual(resultinterval[1], datetime.date(year=1981, month=5, day=6))

        resultinterval = parse_interval('1980-03-05T01:01:00/1981-04-05T01:01:00')
        self.assertEqual(resultinterval[0], datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1))
        self.assertEqual(resultinterval[1], datetime.datetime(year=1981, month=4, day=5, hour=1, minute=1))

        resultinterval = parse_interval('1980-03-05T01:01:00/1981-04-05')
        self.assertEqual(resultinterval[0], datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1))
        self.assertEqual(resultinterval[1], datetime.date(year=1981, month=4, day=5))

        resultinterval = parse_interval('1980-03-05/1981-04-05T01:01:00')
        self.assertEqual(resultinterval[0], datetime.date(year=1980, month=3, day=5))
        self.assertEqual(resultinterval[1], datetime.datetime(year=1981, month=4, day=5, hour=1, minute=1))

        resultinterval = parse_interval('1980-03-05/1981-04-05')
        self.assertEqual(resultinterval[0], datetime.date(year=1980, month=3, day=5))
        self.assertEqual(resultinterval[1], datetime.date(year=1981, month=4, day=5))

        resultinterval = parse_interval('1981-04-05/1980-03-05')
        self.assertEqual(resultinterval[0], datetime.date(year=1981, month=4, day=5))
        self.assertEqual(resultinterval[1], datetime.date(year=1980, month=3, day=5))

        resultinterval = parse_interval('1980-03-05T01:01:00--1981-04-05T01:01:00', intervaldelimiter='--')
        self.assertEqual(resultinterval[0], datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1))
        self.assertEqual(resultinterval[1], datetime.datetime(year=1981, month=4, day=5, hour=1, minute=1))

        resultinterval = parse_interval('1980-03-05 01:01:00/1981-04-05 01:01:00', datetimedelimiter=' ')
        self.assertEqual(resultinterval[0], datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1))
        self.assertEqual(resultinterval[1], datetime.datetime(year=1981, month=4, day=5, hour=1, minute=1))

    def test_parse_repeating_interval(self):
        results = list(parse_repeating_interval('R3/1981-04-05/P1D'))
        self.assertEqual(results[0], datetime.date(year=1981, month=4, day=5))
        self.assertEqual(results[1], datetime.date(year=1981, month=4, day=6))
        self.assertEqual(results[2], datetime.date(year=1981, month=4, day=7))

        results = list(parse_repeating_interval('R11/PT1H2M/1980-03-05T01:01:00'))

        for dateindex in range(0, 11):
             self.assertEqual(results[dateindex], datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1) - dateindex * datetime.timedelta(hours=1, minutes=2))

        results = list(parse_repeating_interval('R2--1980-03-05T01:01:00--1981-04-05T01:01:00', intervaldelimiter='--'))
        self.assertEqual(results[0], datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1))
        self.assertEqual(results[1], datetime.datetime(year=1981, month=4, day=5, hour=1, minute=1))

        results = list(parse_repeating_interval('R2/1980-03-05 01:01:00/1981-04-05 01:01:00', datetimedelimiter=' '))
        self.assertEqual(results[0], datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1))
        self.assertEqual(results[1], datetime.datetime(year=1981, month=4, day=5, hour=1, minute=1))

        resultgenerator = parse_repeating_interval('R/PT1H2M/1980-03-05T01:01:00')

        for dateindex in range(0, 11):
             self.assertEqual(next(resultgenerator), datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1) - dateindex * datetime.timedelta(hours=1, minutes=2))
