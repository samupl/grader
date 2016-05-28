import unittest
from io import StringIO

from lib.default_config_parser import DefaultConfigParser


class DefaultConfigParserTestCase(unittest.TestCase):
    def setUp(self):
        self.fp_example = StringIO()
        self.fp_example.write("""
            [database]
            engine =        django.db.backends.sqlite3
            name =          db.sqlite3
            user =          -
            password =      -
            host =          -

            [debug]
            debug =         true

            [numbers]
            float =         1.23
            int =           123
        """)
        self.fp_example.seek(0)

    def test_existing_boolean_value(self):
        """ Test if the boolean value for debug::debug returns a valid boolean (as set in the example config) """
        cfg = DefaultConfigParser()
        cfg.read_file(self.fp_example)
        self.assertTrue(cfg.getboolean('debug', 'debug'))

    def test_existing_string_value(self):
        """ Test if the boolean value for database::engine returns a valid string (as set in the example config) """
        cfg = DefaultConfigParser()
        cfg.read_file(self.fp_example)
        self.assertEqual(cfg.get('database', 'engine'), 'django.db.backends.sqlite3')

    def test_existing_int_value(self):
        """ Test if the boolean value for numbers::int returns a valid integer (as set in the example config) """
        cfg = DefaultConfigParser()
        cfg.read_file(self.fp_example)
        self.assertEqual(cfg.getint('numbers', 'int'), 123)

    def test_existing_float_value(self):
        """ Test if the boolean value for numbers::float returns a valid float (as set in the example config) """
        cfg = DefaultConfigParser()
        cfg.read_file(self.fp_example)
        self.assertEqual(cfg.getfloat('numbers', 'float'), 1.23)

    def test_not_existing_boolean_value_in_existing_section(self):
        """ Test if the boolean value for debug::debug2 (value is non-existent) returns the default parameter """
        cfg = DefaultConfigParser()
        cfg.read_file(self.fp_example)
        self.assertTrue(cfg.getboolean('debug', 'debug2', default=True))

    def test_not_existing_string_value_in_existing_section(self):
        """ Test if the string value for debug::debug2 (value is non-existent) returns the default parameter """
        cfg = DefaultConfigParser()
        cfg.read_file(self.fp_example)
        self.assertEqual(cfg.get('debug', 'debug2', default='Some string'), 'Some string')

    def test_not_existing_int_value_in_existing_section(self):
        """ Test if the integer value for debug::debug2 (value is non-existent) returns the default parameter """
        cfg = DefaultConfigParser()
        cfg.read_file(self.fp_example)
        self.assertEqual(cfg.getint('debug', 'debug2', default=123), 123)

    def test_not_existing_float_value_in_existing_section(self):
        """ Test if the float value for debug::debug2 (value is non-existent) returns the default parameter """
        cfg = DefaultConfigParser()
        cfg.read_file(self.fp_example)
        self.assertEqual(cfg.getint('debug', 'debug2', default=1.23), 1.23)

    def test_not_existing_boolean_value_in_non_existing_section(self):
        """ Boolean for non-existing::debug2 (section and value do not exist) should return the default parameter """
        cfg = DefaultConfigParser()
        cfg.read_file(self.fp_example)
        self.assertTrue(cfg.getboolean('non-existing', 'debug2', default=True))

    def test_not_existing_string_value_in_non_existing_section(self):
        """ String for non-existing::debug2 (section and value do not exist) should return the default parameter """
        cfg = DefaultConfigParser()
        cfg.read_file(self.fp_example)
        self.assertEqual(cfg.get('non-existing', 'debug2', default='Some string'), 'Some string')

    def test_not_existing_int_value_in_non_existing_section(self):
        """ Integer for non-existing::debug2 (section and value do not exist) should return the default parameter """
        cfg = DefaultConfigParser()
        cfg.read_file(self.fp_example)
        self.assertEqual(cfg.getint('non-existing', 'debug2', default=123), 123)

    def test_not_existing_float_value_in_non_existing_section(self):
        """ Float for non-existing::debug2 (section and value do not exist) should return the default parameter """
        cfg = DefaultConfigParser()
        cfg.read_file(self.fp_example)
        self.assertEqual(cfg.getint('non-existing', 'debug2', default=1.23), 1.23)
