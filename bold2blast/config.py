'''
Created on 2016-03-13

:author: Iyad Kandalaft <iyad.kandalaft@canada.ca>
:organization: Agriculture and Agri-Food Canada
'''
import os.path
import rx
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
            raise IOError("Configuration file %s does not exist.".format(path))
        
        with open(path, 'r') as conf_file:
            self.conf = yaml.load(conf_file.read())
        
        self._validate_conf()
        
        
    def _validate_conf(self):
        if not hasattr(self.conf, 'databases'):
            raise LookupError('Configuration file is missing the top level "databases" element.')
        
        
        for database_key in self.databases():
            db = self.conf['databases'][database_key]  
            
            if not self._is_valid_search_criteria(db['search-criteria']):
                raise ValueError('Search criteria for database %s is invalid.'.format(database_key))
        
    
    def _is_valid_search_criteria(self, criteria):
        return True
    
    def databases(self):
        '''Return a list of the define databases'''
        return self.conf['databases'].keys()
    
    def db_blasdb_path(self, db_key):
        if not hasattr(self.conf['databases'][db_key], 'blastdb-path'):
            return os.path.curdir
        
        return self.conf['databases'][db_key]['blastdb-path']
    
    def db_fasta_path(self, db_key):
        if not hasattr(self.conf['databases'][db_key], 'fasta-path'):
            return None
        
        return self.conf['databases'][db_key]['fasta-path']
    
    def db_name(self, db_key):
        if not hasattr(self.conf['databases'][db_key], 'name'):
            return db_key
        
        return self.conf['databases'][db_key]['name']
    
    def db_search_criteria(self, db_key):
        if not hasattr(self.conf['databases'][db_key], 'search-criteria'):
            return None
        
        return self.conf['databases'][db_key]['search-criteria']