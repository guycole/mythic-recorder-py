#
# Title: context.py
# Description: runtime context
# Development Environment: OS X 10.13.3/Python 3.6.4
# Author: G.S. Cole (guycole at gmail dot com)
#
from yaml import load

class Context:

    def __init__(self):
        self.alert_log = ''
        self.session = ''

        self.task_id = 0

        self.import_directory = ''
        self.sns_alarm = ''

        self.mysql_url = ''
        self.mysql_username = ''
        self.mysql_password = ''
        self.mysql_hostname = ''
        self.mysql_database = ''

    def set_alert_log(self, arg):
        self.alert_log = arg

    def set_session(self, arg):
        self.session = arg

    def set_task_id(self, arg):
        self.task_id = arg

    def loader(self, file_name):
        with open(file_name, 'r') as in_file:
            configuration = load(in_file)
            in_file.close()

        self.import_directory = configuration['importDir']
        self.sns_alarm = configuration['snsArn']

        self.mysql_username = configuration['mySqlUserName']
        self.mysql_password = configuration['mySqlPassWord']
        self.mysql_hostname = configuration['mySqlHostName']
        self.mysql_database = configuration['mySqlDataBase']

        self.mysql_url = "mysql://%s:%s@%s:3306/%s" % (self.mysql_username, self.mysql_password, self.mysql_hostname, self.mysql_database)

#;;; Local Variables: ***
#;;; mode:python ***
#;;; End: ***