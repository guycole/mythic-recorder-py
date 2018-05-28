#
# Title: parse_price.py
# Description: parse and load a price file
# Development Environment: OS X 10.13.3/Python 3.6.4
# Author: G.S. Cole (guycole at gmail dot com)
#
import datetime
import time

from mythic_recorder.parse_parent import ParseParent
from mythic_recorder.sql_table import Name
from mythic_recorder.sql_table import PriceIntraDay
from mythic_recorder.sql_table import PriceSession
from mythic_recorder.utility import Utility


class ParsePrice(ParseParent):
    """
    Parse and load a price file
    """

    def __init__(self, context, eod_file):
        super().__init__(context, eod_file, 'parse_price')

    def insert_stub_name(self, exchange_id, symbol):
        name = Name(exchange_id, symbol, 'stub')
        name.creation_task_id = self.context.task_id

        name.root_symbol_id = 0
        name.expiration = datetime.date(2056, 1, 1)
        name.put_call_flag = False
        name.strike = 0

        self.context.session.add(name)
        self.context.session.commit()

        self.stub_row_counter = 1 + self.stub_row_counter

        return name

    def equal_row(self, selected, fresh):
        """
        :param selected: selected price model
        :param fresh: fresh price model
        :return: true if rows match
        """
        if selected.name_id != fresh.name_id:
            return False

        if selected.date != fresh.date:
            return False

        if selected.open_price != fresh.open_price:
            return False

        if selected.high_price != fresh.high_price:
            return False

        if selected.low_price != fresh.low_price:
            return False

        if selected.close_price != fresh.close_price:
            return False

        if selected.volume != fresh.volume:
            return False

        if selected.open_interest != fresh.open_interest:
            return False

        return True

    def parse_row(self, raw_line):
        #
        # AAL,20180212,48.79,50.51,48.65,50.09,5437000
        # AAPL,20180212,158.5,163.89,157.51,162.71,60808300
        #
        if raw_line.startswith('Symbol'):
            self.fail_row_counter = 1 + self.fail_row_counter
            return None

        buffer = raw_line.strip().split(",")
        if len(buffer) < 7 or len(buffer) > 8:
            self.fail_row_counter = 1 + self.fail_row_counter
            return None

        utility = Utility()

        symbol = buffer[0].strip()
        date = utility.date_converter(buffer[1].strip())
        open_price = utility.price_converter(buffer[2].strip())
        high_price = utility.price_converter(buffer[3].strip())
        low_price = utility.price_converter(buffer[4].strip())
        close_price = utility.price_converter(buffer[5].strip())
        volume = int(buffer[6].strip())

        if len(buffer) > 7:
            open_interest = int(buffer[7].strip())
        else:
            open_interest = 0

        return symbol, date, open_price, high_price, low_price, close_price, volume, open_interest

    def write(self, exchange, raw_buffer, intraday_flag):
        """
        parse and load the contents of raw_buffer
        :param exchange: associated exchange
        :param raw_buffer: raw exchange row
        :return: None or Price
        """
        try:
            current = self.parse_row(raw_buffer)
            if current is None:
                return None

            name = self.select_name(current[0], exchange.id)
            if name is None:
                name = self.insert_stub_name(exchange.id, current[0])

            if intraday_flag:
                price = PriceIntraDay(name.id, current[1], current[2], current[3], current[4], current[5], current[6], current[7])
                selected = self.select_intraday_price(price.name_id, price.date)
                if selected is None:
                    return self.insert_intraday_price(price)
                else:
                    if self.equal_row(selected, price):
                        self.duplicate_row_counter = 1 + self.duplicate_row_counter
                        return selected
                    else:
                        return self.update_intraday_price(selected.id, price)
            else:
                price = PriceSession(name.id, current[1], current[2], current[3], current[4], current[5], current[6], current[7])
                selected = self.select_session_price(price.name_id, price.date)
                if selected is None:
                    return self.insert_session_price(price)
                else:
                    if self.equal_row(selected, price):
                        self.duplicate_row_counter = 1 + self.duplicate_row_counter
                        return selected
                    else:
                        return self.update_session_price(selected.id, price)
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

        intraday_flag = self.eod_file.is_intraday()

        with open(self.eod_file.full_name, 'rt') as in_file:
            for raw_buffer in in_file:
                self.total_row_counter = 1 + self.total_row_counter

                self.write(exchange, raw_buffer, intraday_flag)

        self.context.session.commit()

        self.context.alert_log.log_writer(self.facility, 6, "stop:%s" % self.eod_file.normalized_file_name)

        stop_time = time.time()
        self.duration = stop_time - start_time

        return True

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
