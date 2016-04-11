'''
:author: Iyad Kandalaft <iyad.kandalaft@canada.ca>
:organization: Agriculture and Agri-Foods Canada
:group: Microbial Biodiversity Bioinformatics
:contact: mbb@agr.gc.ca 
:license: LGPL v3
'''

from tests import TESTDATA
import unittest

from bold2blast.config import Config


class ConfigTest(unittest.TestCase):
    def setUp(self):
        self.config = Config(TESTDATA['config-multiple-databases'])
    
    def tearDown(self):
        del self.config
    
    def test_parse_conf(self):
        self.assertTrue(self.config.parse_conf(), 'Configuration file validation failed when using an expected configuration format.')

    def test_parse_conf_raises_no_general_section(self):
        del self.config.conf['general']
        with self.assertRaises(LookupError):
            self.config.parse_conf()

    def test_parse_conf_raises_no_databases_section(self):
        del self.config.conf['databases']
        with self.assertRaises(LookupError):
            self.config.parse_conf()

    def test_parse_conf_raises_no_search_criteria(self):
        db_key = self.config.conf['databases'].keys()[0]
        del self.config.conf['databases'][db_key]['search-criteria']
        with self.assertRaises(ValueError):
            self.config.parse_conf()

    def test_parse_conf_raises_invalid_search_criteria(self):
        db_key = self.config.conf['databases'].keys()[0]
        for criteria in self.config.conf['databases'][db_key]['search-criteria']:
            self.config.conf['databases'][db_key]['search-criteria'] = None
        with self.assertRaises(ValueError):
            self.config.parse_conf()

    def test_parse_conf_raises_invalid_destination(self):
        db_key = self.config.conf['databases'].keys()[0]
        del self.config.conf['databases'][db_key]['destination']
        del self.config.conf['general']['default-destination']
        with self.assertRaises(ValueError):
            self.config.parse_conf()
        
    def test_has_valid_search_criteria_with_string_criteria(self):
        pass

    def test_has_valid_search_criteria_with_array_criteria(self):
        pass

    def test_has_valid_search_criteria_with_missing_criteria(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
