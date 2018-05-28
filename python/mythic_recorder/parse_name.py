#
# Title: parse_name.py
# Description: parse and load a file from the "names" directory
# Development Environment: OS X 10.13.3/Python 3.6.4
# Author: G.S. Cole (guycole at gmail dot com)
#
import time
import xmltodict

from mythic_recorder.parse_parent import ParseParent
from mythic_recorder.sql_table import Name


class ParseName(ParseParent):
    """
    Parse and load a file from the "names" directory
    """

    def __init__(self, context, eod_file):
        super().__init__(context, eod_file, 'parse_name')

    def equal_row(self, selected, fresh):
        """
        :param selected: selected name model
        :param fresh: fresh name model
        :return: true if rows match
        """
        if selected.exchange_id != fresh.exchange_id:
            return False

        if selected.symbol != fresh.symbol:
            return False

        if selected.name != fresh.name:
            return False

        if selected.put_call_flag != fresh.put_call_flag:
            return False

        if selected.root_symbol_id != fresh.root_symbol_id:
            return False

        if selected.expiration != fresh.expiration:
            return False

        if selected.strike != fresh.strike:
            return False

        return True

    def parse_row(self, exchange_id, raw_buffer):
        symbol = raw_buffer['@Code']
        name = raw_buffer['@Name']

        return Name(exchange_id, symbol, name)

    def write(self, exchange, raw_buffer):
        """
        parse and load the contents of raw_buffer
        :param exchange: associated exchange
        :param raw_buffer: raw exchange row
        :return: None or Name
        """
        try:
            name = self.parse_row(exchange.id, raw_buffer)
            if name is None:
                return None

            selected = self.select_name(name.symbol, exchange.id)
            if selected is None:
                return self.insert_name(name)
            else:
                if self.equal_row(selected, name):
                    self.duplicate_row_counter = 1 + self.duplicate_row_counter
                    return selected
                else:
                    return self.update_name(selected.id, name)
        except:
            self.fail_row_counter = 1 + self.fail_row_counter
            self.context.alert_log.log_writer(self.facility, 4, "exception parse:%s, row ndx:%d, contents:%s" %
                                              (self.eod_file.normalized_file_name, self.total_row_counter, raw_buffer))

    def execute(self):
        start_time = time.time()

        self.context.alert_log.log_writer(self.facility, 6, "start:%s" % self.eod_file.normalized_file_name)

        exchange = self.select_exchange(self.eod_file.get_exchange())
        if exchange is None:
            self.context.alert_log.log_writer(self.facility, 4, "skipping unknown exchange:%s" % self.eod_file.normalized_file_name)
            return False

        with open(self.eod_file.full_name) as in_file:
            document = xmltodict.parse(in_file.read())

        names = document['ArrayOfSYMBOL']['SYMBOL']
        for element in names:
            self.write(exchange, element)

        self.context.session.commit()

        self.context.alert_log.log_writer(self.facility, 6, "stop:%s" % self.eod_file.normalized_file_name)

        stop_time = time.time()
        self.duration = stop_time - start_time

        return True

#;;; Local Variables: ***
#;;; mode:python ***
#;;; End: ***