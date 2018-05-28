#
# Title: alert_log.py
# Description: alert and log support
# Development Environment: OS X 10.13.3/Python 3.6.4
# Author: G.S. Cole (guycole at gmail dot com)
#
import boto3
import syslog

from mythic_recorder.sql_table import ApplicationLog

class AlertLog:
    """
    Logging and Alerting facade.  Logging goes to SysLog and RDBMS.  Urgent messages go to SNS for email delivery.
    """

    def __init__(self, sns_arn, session, task_id):
        """
        ctor
        :param sns_arn: SNS ARN for email delivery.  NONE means no SNS.
        :param session: database session
        :param task_id: from TaskLog
        """
        self.sns_arn = sns_arn
        self.session = session
        self.task_id = task_id

    def mail_alert(self, facility, level, message):
        """
        write to SNS for mail delivery
        :param facility:
        :param level:
        :param message:
        :return: None
        """
        if self.sns_arn is None:
            return

        client = boto3.client('sns')
        response = client.publish(TopicArn = self.sns_arn, Message = "%s:%d:%s" % (facility, level, message))

        # print("Response: {}".format(response))

    def log_writer(self, facility, level, message):
        """
        write a log entry to ApplicationLog, severe entries are echoed via email
        :param facility: subsystem where message originates
        :param level: severity level, integer where 0 = emergency, 4 = warning, 6 = info
        :param message: log message
        :return: None
        """
        syslog.syslog(syslog.LOG_INFO, message)

        self.session.add(ApplicationLog(self.task_id, facility, level, message))
        self.session.commit()

        if level < 5:
            self.mail_alert(facility, level, message)

    def log_fatal(self, facility, message):
        """
        service a fatal error
        :param alert_log: alert/logging facade
        :param facility: logging facility
        :param message: message to be logged
        :return: None
        """
        print(message)
        self.log_writer(facility, 4, message)
        self.log_writer(facility, 6, 'stop')

#;;; Local Variables: ***
#;;; mode:python ***
#;;; End: ***
