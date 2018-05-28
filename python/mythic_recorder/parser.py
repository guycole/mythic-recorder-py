#
# Title: parser.py
# Description: drive the parser
# Development Environment: OS X 10.13.3/Python 3.6.4
# Author: G.S. Cole (guycole at gmail dot com)
#
import time

from mythic_recorder.eod_file import EodFile
from mythic_recorder.parse_exchange import ParseExchange
from mythic_recorder.parse_name import ParseName
from mythic_recorder.parse_price import ParsePrice
from mythic_recorder.sql_table import LoadLog

class Parser:
    """
    Inspect LoadLog table for files awaiting service.
    Dispatch dedicated parser/loader to service file.
    """

    def __init__(self):
        self.facility = 'parser'

    def update_load_log(self, session, selected_id, retstat, parser):
        session.query(LoadLog).with_for_update().filter_by(id=selected_id). \
            update({"update_task_id":parser.context.alert_log.task_id, "duplicate_pop":parser.duplicate_row_counter,
                    "fail_pop":parser.fail_row_counter, "fresh_pop":parser.fresh_row_counter,
                    "update_pop":parser.update_row_counter, "stub_pop":parser.stub_row_counter,
                    "total_pop":parser.total_row_counter, "duration":parser.duration, "complete_flag":retstat})

        session.commit()

    def service_exchange(self, context):
        selected_set = context.session.query(LoadLog).filter_by(complete_flag=False, file_name='ExchangeList.xml').\
            order_by(LoadLog.normalized_name).all()

        for selected in selected_set:
            context.alert_log.log_writer(self.facility, 4, "exchange file updated")
            eod_file = EodFile("%s/%s" % (context.import_directory, selected.normalized_name))

            parser = ParseExchange(context, eod_file)
            retstat = parser.execute()

            self.update_load_log(context.session, selected.id, retstat, parser)

    def service_name(self, context):
        selected_set = context.session.query(LoadLog).filter_by(complete_flag=False, file_name='SymbolList.xml').\
            order_by(LoadLog.normalized_name).all()

        for selected in selected_set:
            eod_file = EodFile("%s/%s" % (context.import_directory, selected.normalized_name))

            parser = ParseName(context, eod_file)
            retstat = parser.execute()

            self.update_load_log(context.session, selected.id, retstat, parser)

    def service_price(self, context):
        selected_set = context.session.query(LoadLog).filter_by(complete_flag=False).\
            order_by(LoadLog.normalized_name).all()

        for selected in selected_set:
            eod_file = EodFile("%s/%s" % (context.import_directory, selected.normalized_name))

            parser = ParsePrice(context, eod_file)
            retstat = parser.execute()

            self.update_load_log(context.session, selected.id, retstat, parser)

    def execute(self, context):
        """
        Inspect LoadLog for fresh files awaiting parse/loading
        :param context: runtime context
        :return: None
        """
        context.alert_log.log_writer(self.facility, 6, 'start')

        try:
            self.service_exchange(context)

            self.service_name(context)

            self.service_price(context)

            status = True
        except:
            context.alert_log.log_writer(self.facility, 4, 'parse exception noted')
            status = False
        finally:
            context.alert_log.log_writer(self.facility, 6, 'parse finally')

        context.alert_log.log_writer(self.facility, 6, 'stop')

        return status

#;;; Local Variables: ***
#;;; mode:python ***
#;;; End: ***
