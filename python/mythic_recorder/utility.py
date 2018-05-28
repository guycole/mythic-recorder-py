#
# Title: utility.py
# Description: utility support
# Development Environment: OS X 10.13.3/Python 3.6.4
# Author: G.S. Cole (guycole at gmail dot com)
#
import datetime
import math
import os


class Utility:
    """
    utility methods
    """

    def date_converter(self, arg):
        """
        Original price file format: yyyymmdd 20151109
        Original name file option expiration: yymmdd AAC151016C00017500

        CSV format: 27-Apr-2018
        5 minute bar timestamp as: 27-Apr-2018 09:20
        :param arg: raw date time
        :return: converted date
        """

        if len(arg) == 6:
            # yymmdd format
            return datetime.date(2000+int(arg[:2]), int(arg[2:4]), int(arg[4:]))

        if len(arg) == 8:
            # yyyymmdd format
            return datetime.date(int(arg[:4]), int(arg[4:6]), int(arg[6:]))

        ndx = arg.find(' ')
        if ndx < 0:
            # dd-mmm-yyyy
            return datetime.datetime.strptime(arg, '%d-%b-%Y')
        else:
            # dd-mm-yyyy hh:mm
            return datetime.datetime.strptime(arg, '%d-%b-%Y %H:%M')

    def epsilon_compare(self, arg1, arg2):
        """
        floating point comparison
        :param arg1:
        :param arg2:
        :return: true if equal
        """
        return math.isclose(arg1, arg2);

    def price_converter(self, arg):
        """
        prices are integers
        :param arg: decimal point price
        :return: price as pennies * 10
        """
        return int(float(arg) * 1000.0)

    def chdir_import_directory(self, facility, context):
        """
        chdir to import directory
        :param facility: source facility (class name)
        :param context: runtime context
        :return: True if success
        """
        if os.path.exists(context.data_directory):
            os.chdir(context.data_directory)
            return True
        else:
            context.alert_log.log_fatal(facility, "missing data directory:%s" % context.data_directory)
            return False

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***