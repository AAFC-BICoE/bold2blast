'''
Created on 2016-03-13

:author: Iyad Kandalaft <iyad.kandalaft@canada.ca>
:organization: Agriculture and Agri-Food Canada
'''
import os.path
import yaml


class Config(object):
    '''
    classdocs
    '''

    def __init__(self, config_path):
        '''
        Constructor
        '''
        
        if not os.path.isfile(config_path):
            raise IOError('Configuration file "{}" does not exist.'.format(config_path))
        
        with open(config_path, 'r') as conf_file:
            self.conf = yaml.load(conf_file.read())        
    
        self.databases = {}

    def parse_conf(self):
        required_config = ['general', 'databases']
        for elem in required_config:
            if elem not in self.conf:
                raise LookupError('Configuration file is missing the top level "{}" element.  Please see sample configuration file as an example.'.format(elem))
        
        for database_key in self.db_keys:
            database_config = self.conf['databases'][database_key]  
            self.databases[database_key] = DBConfig(database_key, database_config, self.default_destination)

            if not self._has_valid_destination(database_key):
                raise ValueError('Destination folder for database "{}" or the default-destination must be set.'.format(database_key))
            
            if not self._has_valid_search_criteria(database_key):
                raise ValueError('Search criteria for database "{}" is invalid.'.format(database_key))
        
        return True
    
    def _has_valid_search_criteria(self, db_key):
        search_criteria = self.databases[db_key].search_criteria
        if search_criteria is None:
            return False
        
        # Ensure that each database has at least one search criterion
        criteria = ['taxon', 'ids', 'bin', 'container', 'institutions', 'researchers', 'geo', 'markers']
        has_one_element = False
        for criterion in criteria:
            if criterion not in search_criteria:
                continue
            if search_criteria[criterion] is not None:
                has_one_element = True
        
        return has_one_element
         
    
    def _has_valid_destination(self, db_key):
        if self.databases[db_key].destination is None:
            return False
        
        return True
    
    @property
    def default_destination(self):
        if 'default-destination' not in self.conf['general']:
            return None
        
        return self.conf['general']['default-destination']
    
    @default_destination.setter
    def default_destination(self, path):
        self.conf['general']['default-destination'] = path
    
    @property
    def db_keys(self):
        '''Return a list of the defined databases'''
        return self.conf['databases'].keys()
    
class DBConfig():
    def __init__(self, key, config, default_destination = None):
        self.db_key = key
        self.db_conf = config
        self.default_destination = default_destination

    @property
    def blasdb_path(self):
        if 'blastdb-path' not in self.db_conf or self.db_conf['blastdb-path'] is None:    
            return os.path.join(self.destination, self.db_name)

        return self.db_conf['blastdb-path']
    
    @property
    def fasta_path(self):
        if 'fasta-path' not in self.db_conf or self.db_conf['fasta-path'] is None:
            return os.path.join(self.destination, self.db_name + '.fasta')

        return self.db_conf['fasta-path']
    
    @property
    def name(self):
        '''Return the name attribute for the requested database key
        If the name is not defined, return the db key as the name.'''

        if 'name' not in self.db_conf:
            return self.db_key
        
        return self.db_conf['name']
    
    @property
    def destination(self):
        if 'destination' not in self.db_conf or self.db_conf['destination'] is None:
            return self.default_destination
        else:
            return self.db_conf['destination']
     
    @property           
    def search_criteria(self):
        if 'search-criteria' not in self.db_conf:
            return None
        
        return self.db_conf['search-criteria']
