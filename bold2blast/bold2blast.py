'''
Created on 2016-03-13

:author: Iyad Kandalaft <iyad.kandalaft@canada.ca>
:organization: Agriculture and Agri-Food Canada
'''

from Bio import SeqIO
import os
import pybold.sequence
import subprocess
import tempfile


class bold2blast(object):
    def __init__(self, database, search_criteria):
        '''
        Constructor
        '''
        self.database = database
        self.search_criteria = search_criteria
        self.seq_records = []
        
    
    def _is_makeblastdb_on_path(self):
        try:
            subprocess.call(['makeblastdb'])
        except OSError as e: # Binary not found error.
            if e.errno == os.errno.ENOENT:
                return False
            else:
                raise
        return True
    
    def _fetch_sequences(self):
        sc = pybold.sequence.SequencesClient()
        self.seq_records = self.sc.get()
        
    
    def write_fasta(self, path):
        '''Generate a fasta file from the search criteria''' 
        if not self.seq_records:
            self._fetch_sequences()
            
        with open(path, "w+") as handle:
            SeqIO.write('records', handle, "fasta")
            
    
    def create_blastdb(self, blastdb_path, fasta_path=None, makeblastdb_bin=None):
        if makeblastdb_bin is None and not self._is_makeblastdb_on_path():
            raise OSError('makeblastdb is not on the path.')
        if makeblastdb_bin is not None and not os.path.isfile(makeblastdb_bin):
            raise IOError('%s is not a valid path for the makeblastdb binary'.format(makeblastdb_bin))
        
        
        if fasta_path is None:
            fasta_path = tempfile.mkstemp()
        
        self.write_fasta(fasta_path)
        
        subprocess.call([makeblastdb_bin, '-dbtype', 'nucl', '-in', fasta_path, '-input_type', 'fasta', '-out', blastdb_path, '-parse_seqids'])
            
            
        