#
# Title: parse_parent.py
# Description: parser parent class
# Development Environment: OS X 10.13.3/Python 3.6.4
# Author: G.S. Cole (guycole at gmail dot com)
#
from mythic_recorder.sql_table import Exchange
from mythic_recorder.sql_table import Name
from mythic_recorder.sql_table import PriceIntraDay
from mythic_recorder.sql_table import PriceSession

class ParseParent:
    """
    Parse and load a file from the "names" directory
    """

    def __init__(self, context, eod_file, facility):
        self.context = context
        self.eod_file = eod_file
        self.facility = facility

        self.current_row = ''
        self.duplicate_row_counter = 0
        self.duration = 0
        self.fail_row_counter = 0
        self.fresh_row_counter = 0
        self.row_ndx = 0
        self.stub_row_counter = 0
        self.total_row_counter = 0
        self.update_row_counter = 0

    def __repr__(self):
        return "%s(%d, %d, %d, %d, %s)" % (self.facility, self.fresh_row_counter, self.duplicate_row_counter, self.update_row_counter, self.fail_row_counter, self.eod_file.normalized_file_name)

    def insert_exchange(self, exchange):
        exchange.creation_task_id = self.context.alert_log.task_id
        self.context.session.add(exchange)
        self.fresh_row_counter = 1 + self.fresh_row_counter
        return exchange

    def select_exchange(self, symbol):
        return self.context.session.query(Exchange).filter_by(symbol=symbol).first()

    def update_exchange(self, row_id, exchange):
        self.context.session.query(Exchange).with_for_update().filter_by(id=row_id).update({"update_task_id":self.context.alert_log.task_id, "name":exchange.name})
        self.update_row_counter = 1 + self.update_row_counter
        return exchange

    def insert_name(self, name):
        name.creation_task_id = self.context.alert_log.task_id
        self.context.session.add(name)
        self.fresh_row_counter = 1 + self.fresh_row_counter
        return name

    def select_name(self, symbol, exchange_id):
        return self.context.session.query(Name).filter_by(symbol=symbol, exchange_id=exchange_id, active_flag=True).first()

    def update_name(self, row_id, name):
        task_id = self.context.alert_log.task_id
        self.context.session.query(Name).with_for_update().filter_by(id=row_id).update({"update_task_id": task_id, "name":name.name, "root_symbol_id":name.root_symbol_id, "expiration":name.expiration, "put_call_flag":name.put_call_flag, "strike":name.strike})
        self.update_row_counter = 1 + self.update_row_counter
        return name

    def insert_intraday_price(self, price):
        price.creation_task_id = self.context.alert_log.task_id
        self.context.session.add(price)
        self.fresh_row_counter = 1 + self.fresh_row_counter
        return price

    def select_intraday_price(self, name_id, date_time):
        return self.context.session.query(PriceIntraDay).filter_by(name_id=name_id, date=date_time).first()

    def update_intraday_price(self, row_id, price):
        self.context.session.query(PriceIntraDay).with_for_update().filter_by(id=row_id).update({"open_price":price.open_price, "high_price":price.high_price, "low_price":price.low_price, "close_price":price.close_price, "volume":price.volume, "open_interest": price.open_interest})
        self.update_row_counter = 1 + self.update_row_counter
        return price

    def insert_session_price(self, price):
        price.creation_task_id = self.context.alert_log.task_id
        self.context.session.add(price)
        self.fresh_row_counter = 1 + self.fresh_row_counter
        return price

    def select_session_price(self, name_id, date):
        return self.context.session.query(PriceSession).filter_by(name_id=name_id, date=date).first()

    def update_session_price(self, row_id, price):
        task_id = self.context.alert_log.task_id
        self.context.session.query(PriceSession).with_for_update().filter_by(id=row_id).update({"open_price":price.open_price, "high_price":price.high_price, "low_price":price.low_price, "close_price":price.close_price, "volume":price.volume, "open_interest": price.open_interest})
        self.update_row_counter = 1 + self.update_row_counter
        return price

#;;; Local Variables: ***
#;;; mode:python ***
#;;; End: ***