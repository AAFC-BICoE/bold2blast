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


    def __init__(self, path):
        '''
        Constructor
        '''
        
        if not os.path.isfile(path):
            raise IOError('Configuration file "{}" does not exist.'.format(path))
        
        with open(path, 'r') as conf_file:
            self.conf = yaml.load(conf_file.read())

        self._validate_conf()
        
        
    def _validate_conf(self):
        required_config = ['general', 'databases']
        for elem in required_config:
            if elem not in self.conf:
                raise LookupError('Configuration file is missing the top level "{}" element.  Please see sample configuration file as an example.'.format(elem))
        
        if not hasattr(self.conf, 'default-destination'):
            self.conf['default-destination'] = None
        
        for database_key in self.databases():
            db = self.conf['databases'][database_key]  
            
            if not self._has_valid_destination(database_key):
                raise ValueError('Destination folder for database "{}" or the default-destination must be set.'.format(database_key))
            
            if not self._has_valid_search_criteria(database_key):
                raise ValueError('Search criteria for database "{}" is invalid.'.format(database_key))
        
    
    def _has_valid_search_criteria(self, db_key):
        search_criteria = self.db_search_criteria(db_key)
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
        if self.db_destination(db_key) is None:
            return False
        
        return True
    
    def default_destination(self):
        if 'default-destination' not in self.conf['general']:
            return None
        
        return self.conf['general']['default-destination']
    
    def databases(self):
        '''Return a list of the defined databases'''
        return self.conf['databases'].keys()
    
    def db_conf(self, db_key):
        return self.conf['databases'][db_key]
    
    def db_blasdb_path(self, db_key):
        if 'blastdb-path' not in self.db_conf(db_key) or self.db_conf(db_key)['blastdb-path'] is None:    
            return os.path.join(self.db_destination(db_key), self.db_name(db_key))

        return self.db_conf(db_key)['blastdb-path']
    
    def db_fasta_path(self, db_key):
        if 'blastdb-path' not in self.db_conf(db_key) or self.db_conf(db_key)['fasta-path'] is None:
            return os.path.join(self.db_destination(db_key), self.db_name(db_key) + '.fasta')

        return self.db_conf(db_key)['fasta-path']
    
    def db_name(self, db_key):
        '''Return the name attribute for the requested database key
        If the name is not defined, return the db key as the name.'''

        if 'name' not in self.db_conf(db_key):
            return db_key
        
        return self.db_conf(db_key)['name']
    
    def db_destination(self, db_key):
        if 'destination' not in self.db_conf(db_key) or self.db_conf(db_key)['destination'] is None:
            return self.default_destination()
        else:
            return self.db_conf(db_key)['destination']
                
    def db_search_criteria(self, db_key):
        if 'search-criteria' not in self.db_conf(db_key):
            return None
        
        return self.db_conf(db_key)['search-criteria']
