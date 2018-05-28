#
# Title: eod_file.py
# Description: eod data file
# Development Environment: OS X 10.13.3/Python 3.6.4
# Author: G.S. Cole (guycole at gmail dot com)
#
import hashlib
import os

class EodFile:
    """
    File wrapper
    """
    def __init__(self, raw_name):
        """
        :param raw_name: fully qualified file name
        """
        self.hash = ''
        self.full_name = raw_name

        # raise substring not found if error
        ndx1 = raw_name.index('ASCII')
        ndx2 = ndx1 + len('ASCII/')
        self.normalized_file_name = raw_name[ndx2:]

        tokens = raw_name.split('/')
        self.file_name = tokens[len(tokens)-1]
    
    def __repr__(self):
        return "<eod_file(%s)>" % self.normalized_file_name

    def is_intraday(self):
        """
        :return: True if this is a intraday file
        """
        temp = self.normalized_file_name.split('/')
        if len(temp) == 3:
            return True
        else:
            return False

    def sha1_hash(self):
        """
        calculate sha1 hash
        """
        BLOCK_SIZE = 65536
        hash_sha1 = hashlib.sha1()
        with open(self.full_name, 'rb') as in_file:
            buffer = in_file.read(BLOCK_SIZE)
            while len(buffer) > 0:
                hash_sha1.update(buffer)
                buffer = in_file.read(BLOCK_SIZE)

        return hash_sha1.hexdigest()

    def file_size(self):
        """
        return file size in bytes
        """
        if os.path.exists(self.full_name):
            return int(os.path.getsize(self.full_name))
        else:
            return -1

    def access_time(self):
        """
        return file access time
        """
        if os.path.exists(self.full_name):
            return int(os.path.getatime(self.full_name))
        else:
            return -1

    def create_time(self):
        """
        return file create time
        """
        if os.path.exists(self.full_name):
            return int(os.path.getctime(self.full_name))
        else:
            return -1

    def modify_time(self):
        """
        return file modification time
        """
        if os.path.exists(self.full_name):
            return int(os.path.getmtime(self.full_name))
        else:
            return -1

    def get_exchange(self):
        if self.normalized_file_name.startswith('AMEX'):
            return 'amex'
        elif self.normalized_file_name.startswith('ASX'):
            return 'asx'
        elif self.normalized_file_name.startswith('BSE'):
            return 'bse'
        elif self.normalized_file_name.startswith('CBOT'):
            return 'cbot'
        elif self.normalized_file_name.startswith('CFE'):
            return 'cfe'
        elif self.normalized_file_name.startswith('CME'):
            return 'cme'
        elif self.normalized_file_name.startswith('COMEX'):
            return 'comex'
        elif self.normalized_file_name.startswith('EUREX'):
            return 'eurex'
        elif self.normalized_file_name.startswith('FOREX'):
            return 'forex'
        elif self.normalized_file_name.startswith('HKEX'):
            return 'hkex'
        elif self.normalized_file_name.startswith('INDEX'):
            return 'index'
        elif self.normalized_file_name.startswith('KCBT'):
            return 'kcbt'
        elif self.normalized_file_name.startswith('LIFFE'):
            return 'liffe'
        elif self.normalized_file_name.startswith('LSE'):
            return 'lse'
        elif self.normalized_file_name.startswith('MGEX'):
            return 'mgex'
        elif self.normalized_file_name.startswith('NASDAQ'):
            return 'nasdaq'
        elif self.normalized_file_name.startswith('NSE'):
            return 'nse'
        elif self.normalized_file_name.startswith('NYBOT'):
            return 'nybot'
        elif self.normalized_file_name.startswith('NYMEX'):
            return 'nymex'
        elif self.normalized_file_name.startswith('NYSE'):
            return 'nyse'
        elif self.normalized_file_name.startswith('NZX'):
            return 'nzx'
        elif self.normalized_file_name.startswith('OTCBB'):
            return 'otcbb'
        elif self.normalized_file_name.startswith('SGX'):
            return 'sgx'
        elif self.normalized_file_name.startswith('TSXV'):
            return 'tsxv'
        elif self.normalized_file_name.startswith('TSX'):
            return 'tsx'
        elif self.normalized_file_name.startswith('USMF'):
            return 'usmf'
        elif self.normalized_file_name.startswith('WCE'):
            return 'wce'
        else:
            return 'unknown'

#;;; Local Variables: ***
#;;; mode:python ***
#;;; End: ***
