#
# Title: discovery.py
# Description: Inspect import directory for fresh files to reload
# Development Environment: OS X 10.13.3/Python 3.6.4
# Author: G.S. Cole (guycole at gmail dot com)
#
import os
import time

from mythic_recorder.eod_file import EodFile
from mythic_recorder.sql_table import FileStat
from mythic_recorder.sql_table import LoadLog
from mythic_recorder.sql_table import LoadLogSummary

class Discovery:
    """
    Inspect import directory for fresh files to reload.
    A fresh file is either unknown or has changed size/sha1 hash.
    FileStat table contains file statistics.
    LoadLog table contains fresh files to be parsed/loaded
    """

    def __init__(self):
        """
        ctor
        """
        self.directory_counter = 0
        self.fresh_file_counter = 0
        self.total_file_counter = 0
        self.updated_file_counter = 0

        self.facility = 'discovery'

    def insert_load_log_summary(self, session, task_id, duration):
        """
        insert a new load log summary row
        :param session: database connection
        :param task_id: parent task id
        :param duration: total discovery duration in seconds
        :return: None
        """
        summary = LoadLogSummary(task_id, duration)
        summary.total_file_pop = self.total_file_counter
        summary.fresh_file_pop = self.fresh_file_counter
        summary.update_file_pop = self.updated_file_counter
        summary.directory_pop = self.directory_counter

        session.add(summary)

        return None

    def insert_load_log(self, session, task_id, eod_file):
        """
        insert a new load log row
        :param session: database connection
        :param task_id: parent task id
        :param eod_file: candidate file
        :return: None
        """
        load_log = LoadLog(task_id, eod_file.get_exchange(), eod_file.file_name, eod_file.normalized_file_name)
        session.add(load_log)

        return None

    def insert_file_stat(self, session, task_id, eod_file):
        """
        insert a new file stat row
        :param session: database connection
        :param task_id: parent task id
        :param eod_file: candidate file
        :return: None
        """
        self.fresh_file_counter = self.fresh_file_counter + 1

        file_stat = FileStat(task_id, eod_file.normalized_file_name, eod_file.file_size(), eod_file.sha1_hash())
        session.add(file_stat)

        self.insert_load_log(session, task_id, eod_file)

        return None

    def update_file_stat(self, session, task_id, eod_file, original):
        """
        update an existing file stat row
        :param session: database connection
        :param task_id: parent task id
        :param eod_file: candidate file
        :param original: original row
        :return: None
        """
        self.updated_file_counter = self.updated_file_counter + 1

        session.query(FileStat).with_for_update().filter_by(id=original.id).update({"update_task_id":task_id, "file_size":eod_file.file_size(), "sha1_hash":eod_file.sha1_hash(ssl_command)})

        self.insert_load_log(session, task_id, eod_file)

        return None

    def process_file(self, session, task_id, eod_file):
        """
        test a file for new/updated status
        :param session: database connection
        :param task_id: parent task id
        :param eod_file: candidate file
        :return: None
        """
        selected = session.query(FileStat).filter_by(normalized_name = eod_file.normalized_file_name).order_by(FileStat.creation_task_id.desc()).first()
        if selected is None:
            self.insert_file_stat(session, task_id, eod_file)
            return None

        if eod_file.file_size() != selected.file_size:
            self.update_file_stat(session, task_id, eod_file, selected)
            return None

        if eod_file.sha1_hash() != selected.sha1_hash:
            self.update_file_stat(session, task_id, eod_file, selected)

        return None

    def process_directory(self, session, task_id, alert_log, directory_name):
        """
        test the current directory for new/updated files
        :param session: database connection
        :param task_id: parent task id
        :param alert_log: alert log
        :param directory_name: current directory name
        :return: None
        """
        self.directory_counter = self.directory_counter + 1

        candidates = os.listdir(directory_name)
        for candidate in candidates:
            normalized_name = "%s/%s" % (directory_name, candidate)
            if os.path.isdir(normalized_name):
                self.process_directory(session, task_id, alert_log, normalized_name)
            else:
                self.total_file_counter = self.total_file_counter + 1

                eod_file = EodFile(normalized_name)
                if eod_file.file_size() < 1:
                    print("skipping empty file:%s" % eod_file.full_name)
                else:
                    self.process_file(session, task_id, eod_file)

    def execute(self, context):
        """
        Inspect a directory w/a freshly unpacked ftp.eoddata.com file for updated files.
        Write updated file information to DB tables: FileStat and LoadLog.
        :param context: runtime context
        :return: True if success
        """
        start_time = time.time()
        context.alert_log.log_writer(self.facility, 6, 'start')

        status = False
        if os.path.exists(context.import_directory):
            os.chdir(context.import_directory)

            self.process_directory(context.session, context.task_id, context.alert_log, context.import_directory)
            context.session.commit()
            status = True
        else:
            context.alert_log.log_fatal(self.facility, "missing import directory:%s" % context.import_directory)
            status = False

        stop_time = time.time()
        duration = stop_time - start_time

        self.insert_load_log_summary(context.session, context.task_id, duration)
        context.session.commit()

        context.alert_log.log_writer(self.facility, 6, 'stop')

        return status

#;;; Local Variables: ***
#;;; mode:python ***
#;;; End: ***