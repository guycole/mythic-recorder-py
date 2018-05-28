#! /usr/bin/python3
#
# Title:loader.py
# Description:
# Development Environment:OS X 10.10.5/Python 2.7.7
# Author:G.S. Cole (guycole at gmail dot com)
#
import syslog
import sys
import time

from mythic_recorder.alert_log import AlertLog
from mythic_recorder.context import Context
from mythic_recorder.discovery import Discovery
from mythic_recorder.parser import Parser
from mythic_recorder.sql_table import SqlTable
from mythic_recorder.sql_table import TaskLog


class Loader:

    def __init__(self):
        """
        ctor
        """
        self.facility = 'loader'

    def execute(self, yaml_file_name):
        start_time = time.time()

        context = Context()
        context.loader(yaml_file_name)

        sql_table = SqlTable(context)
        alert_session = sql_table.session_factory()

        task_log = TaskLog(self.facility)
        alert_session.add(task_log)
        alert_session.commit()

        context.set_task_id(task_log.id)

        alert_log = AlertLog(context.sns_alarm, alert_session, task_log.id)
        alert_log.log_writer(self.facility, 6, 'start')
        context.set_alert_log(alert_log)

        discovery_session = sql_table.session_factory()
        context.set_session(discovery_session)

        try:
            discovery = Discovery()
            discovery.execute(context)
        except:
            context.alert_log.log_writer(self.facility, 4, "discovery failure noted")
        finally:
            discovery_session.commit()
            discovery_session.close()

        parse_session = sql_table.session_factory()
        context.set_session(parse_session)

        try:
            parser = Parser()
            parser.execute(context)
        except:
            context.alert_log.log_writer(self.facility, 4, "parse failure noted")
        finally:
            parse_session.commit()
            parse_session.close()

        alert_log.log_writer(self.facility, 6, 'stop')

        stop_time = time.time()
        return stop_time - start_time

print('start loader');

#
# argv[1] = configuration filename
#
if __name__ == '__main__':
    syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_LOCAL4)

    if len(sys.argv) > 1:
        yaml_file_name = sys.argv[1]
    else:
        yaml_file_name = 'config.dev'

    loader = Loader()
    duration = loader.execute(yaml_file_name)

    syslog.closelog()

print('stop loader');

#;;; Local Variables: ***
#;;; mode:python ***
#;;; End: ***
