#
# Title: parse_exchange.py
# Description: parse and load an exchange file from the "names" directory
# Development Environment: OS X 10.13.3/Python 3.6.4
# Author: G.S. Cole (guycole at gmail dot com)
#
import time
import xmltodict

from mythic_recorder.parse_parent import ParseParent
from mythic_recorder.sql_table import Exchange

class ParseExchange(ParseParent):
    """
    Parse and load an exchange file from the "names" directory
    """

    def __init__(self, context, eod_file):
        super().__init__(context, eod_file, 'parse_exchange')

    def equal_row(self, selected, fresh):
        """
        :param selected: selected exchange model
        :param fresh: fresh exchange model
        :return: true if rows match
        """
        if selected.symbol != fresh.symbol:
            return False

        if selected.name != fresh.name:
            return False

        return True

    def parse_row(self, raw_buffer):
        symbol = raw_buffer['@Code']
        name = raw_buffer['@Name']

        return Exchange(symbol, name)

    def write(self, exchange, raw_buffer):
        """
        parse and load the contents of raw_buffer
        :param exchange: None
        :param raw_buffer: raw exchange row
        :return: None or Exchange
        """
        try:
            current = self.parse_row(raw_buffer)
            if current is None:
                return None

            selected = self.select_exchange(current.symbol)
            if selected is None:
                return self.insert_exchange(current)
            else:
                if self.equal_row(selected, current):
                    self.duplicate_row_counter = 1 + self.duplicate_row_counter
                    return selected
                else:
                    return self.update_exchange(selected.id, current)
        except:
            self.fail_row_counter = 1 + self.fail_row_counter
            self.context.alert_log.log_writer(self.facility, 4, "exception parse:%s" % raw_buffer)

    def execute(self):
        start_time = time.time()

        with open(self.eod_file.full_name) as fd:
            document = xmltodict.parse(fd.read())

        exchanges = document['ArrayOfEXCHANGE']['EXCHANGE']
        for element in exchanges:
            self.write(None, element)

        self.context.session.commit()

        stop_time = time.time()
        self.duration = stop_time - start_time

        return True

#;;; Local Variables: ***
#;;; mode:python ***
#;;; End: ***