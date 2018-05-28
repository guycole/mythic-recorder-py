#
# Title: sql_table.py
# Description: ORM layer, each table has dedicated class
# Development Environment: OS X 10.13.3/Python 3.6.4
# Author: G.S. Cole (guycole at gmail dot com)
#
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column
from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, Integer, String

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ApplicationLog(Base):
    """
    Application log, similar to SysLog
    """
    __tablename__ = 'application_log'

    id = Column(BigInteger, primary_key=True)
    time_stamp = Column(DateTime, default=datetime.datetime.utcnow)
    task_id = Column(BigInteger, nullable=False)
    facility = Column(String(32), nullable=False)
    level = Column(Integer, nullable=False)
    event = Column(String(128), nullable=False)

    def __init__(self, task_id, facility, level, event):
        """
        Create an application log entry
        :param task_id: parent task id
        :param facility: usually class name
        :param level: severity level, emergency = 0, debug = 7
        :param event: free form event message
        """
        self.task_id = task_id
        self.facility = facility
        self.level = level
        self.event = event

    def __repr__(self):
        return "<application_log(%d, %s, %d, %s)>" % (self.task_id, self.facility, self.level, self.event)

class Exchange(Base):
    """
    Contents of Names/Exchanges.txt
    """
    __tablename__ = 'exchange'

    id = Column(BigInteger, primary_key=True)
    creation_task_id = Column(BigInteger, nullable=False)
    update_task_id = Column(BigInteger, nullable=False)
    symbol = Column(String(32), nullable=False, unique=True)
    name = Column(String(64), nullable=False)

    def __init__(self, symbol, name):
        """
        Create an exchange row
        :param symbol: exchange symbol
        :param name: exchange name
        """
        self.creation_task_id = 0
        self.update_task_id = 0
        self.symbol = symbol
        self.name = name

    def __repr__(self):
        return "<exchange(%s, %s)>" % (self.symbol, self.name)

class FileStat(Base):
    """
    Every EodData file known to mythic recorder has one row
    """
    __tablename__ = 'file_stat'

    id = Column(BigInteger, primary_key=True)
    creation_task_id = Column(BigInteger, nullable=False)
    update_task_id = Column(BigInteger, nullable=False)
    normalized_name = Column(String(64), nullable=False, unique=True)
    file_size = Column(Integer, nullable=False)
    sha1_hash = Column(String(48), nullable=False)

    def __init__(self, task_id, normalized_name, file_size, sha1_hash):
        self.creation_task_id = task_id
        self.update_task_id = 0
        self.normalized_name = normalized_name
        self.file_size = file_size
        self.sha1_hash = sha1_hash

    def __repr__(self):
        return "<file_stat(%s, %s)>" % (self.normalized_name, self.sha1_hash)

class LoadLog(Base):
    """
    Every fresh/updated file has a row in LoadLog to manage processing
    """
    __tablename__ = 'load_log'

    id = Column(BigInteger, primary_key=True)
    creation_task_id = Column(BigInteger, nullable=False)
    update_task_id = Column(BigInteger, nullable=False)
    exchange = Column(String(16), nullable=False)
    file_name = Column(String(32), nullable=False)
    normalized_name = Column(String(64), nullable=False)
    duplicate_pop = Column(Integer, nullable=False)
    fail_pop = Column(Integer, nullable=False)
    fresh_pop = Column(Integer, nullable=False)
    update_pop = Column(Integer, nullable=False)
    stub_pop = Column(Integer, nullable=False)
    total_pop = Column(Integer, nullable=False)
    complete_flag = Column(Boolean, nullable=False)
    duration = Column(Integer, nullable=False)

    def __init__(self, task_id, exchange, file_name, normalized_name):
        """
        create a loadlog row
        :param task_id: parent task id
        :param exchange: associated exchange
        :param file_name: file name
        :param normalized_name: file name w/parent directory
        """
        self.creation_task_id = task_id
        self.update_task_id = 0
        self.exchange = exchange
        self.file_name = file_name
        self.normalized_name = normalized_name
        self.duplicate_pop = 0
        self.fail_pop = 0
        self.fresh_pop = 0
        self.update_pop = 0
        self.stub_pop = 0
        self.total_pop = 0
        self.complete_flag = False
        self.duration = 0

    def __repr__(self):
        return "<load_log(%s)>" % (self.normalized_name)

class LoadLogSummary(Base):
    """
    Summary of load log activity
    """
    __tablename__ = 'load_log_summary'

    id = Column(BigInteger, primary_key=True)
    time_stamp = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    task_id = Column(BigInteger, nullable=False)
    total_file_pop = Column(Integer, nullable=False)
    fresh_file_pop = Column(Integer, nullable=False)
    update_file_pop = Column(Integer, nullable=False)
    directory_pop = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)

    def __init__(self, task_id, duration):
        """
        Create a load log summary row
        :param task_id: parent task
        :param tar_file_name: source tar file
        :param duration: total duration in seconds
        """
        self.task_id = task_id
        self.total_file_pop = 0
        self.fresh_file_pop = 0
        self.update_file_pop = 0
        self.directory_pop = 0
        self.duration = duration

    def __repr__(self):
        return "<load_log_summary(%d)>" % (self.task_id)

class Name(Base):
    """
    Information from "Names" directory
    """
    __tablename__ = 'name'

    id = Column(BigInteger, primary_key=True)
    creation_task_id = Column(BigInteger, nullable=False)
    update_task_id = Column(BigInteger, nullable=False)
    exchange_id = Column(BigInteger, nullable=False)
    symbol = Column(String(32), nullable=False)
    name = Column(String(128), nullable=False)
    active_flag = Column(Boolean, nullable=False)
    put_call_flag = Column(Boolean, nullable=False)
    root_symbol_id = Column(BigInteger, nullable=False)
    expiration = Column(Date, nullable=False)
    strike = Column(BigInteger, nullable=False)

    def __init__(self, exchange_id, symbol, name):
        self.creation_task_id = 0
        self.update_task_id = 0
        self.exchange_id = exchange_id
        self.symbol = symbol
        self.name = name
        self.active_flag = True
        self.put_call_flag = False
        self.root_symbol_id = 0
        self.expiration = datetime.date(2056, 1, 1)
        self.strike = 0

    def __repr__(self):
        return "<name(%s, %s)>" % (self.symbol, self.name)

class PriceIntraDay(Base):
    """
    Contents of 5 minute bar price files
    """
    __tablename__ = 'price_intraday'

    id = Column(BigInteger, primary_key=True)
    task_id = Column(BigInteger, nullable=False)
    name_id = Column(BigInteger, nullable=False)
    date = Column(DateTime, nullable=False)
    open_price = Column(BigInteger, nullable=False)
    high_price = Column(BigInteger, nullable=False)
    low_price = Column(BigInteger, nullable=False)
    close_price = Column(BigInteger, nullable=False)
    volume = Column(BigInteger, nullable=False)
    open_interest = Column(BigInteger, nullable=False)

    def __init__(self, name_id, date, open_price, high_price, low_price, close_price, volume, open_interest):
        """
        Create a intraday 5 minute bar row
        :param name_id: join w/name.id
        :param date: 5 minute bar time stamp
        :param open_price: session open price as pennies * 10
        :param high_price: session high price as pennies * 10
        :param low_price: session low price as pennies * 10
        :param close_price: session close price as pennies * 10
        :param volume: session volume
        :param open_interest: open interest (as necessary)
        """
        self.task_id = 0
        self.name_id = name_id
        self.date = date
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.volume = volume
        self.open_interest = open_interest

    def __repr__(self):
        return "<price_intraday(%d, %s)>" % (self.name_id, self.date)

class PriceSession(Base):
    """
    Contents of price files
    """
    __tablename__ = 'price_session'

    id = Column(BigInteger, primary_key=True)
    task_id = Column(BigInteger, nullable=False)
    name_id = Column(BigInteger, nullable=False)
    date = Column(Date, nullable=False)
    open_price = Column(BigInteger, nullable=False)
    high_price = Column(BigInteger, nullable=False)
    low_price = Column(BigInteger, nullable=False)
    close_price = Column(BigInteger, nullable=False)
    volume = Column(BigInteger, nullable=False)
    open_interest = Column(BigInteger, nullable=False)

    def __init__(self, name_id, date, open_price, high_price, low_price, close_price, volume, open_interest):
        """
        Create a price row
        :param name_id: join w/name.id
        :param date: quote date
        :param open_price: session open price as pennies * 10
        :param high_price: session high price as pennies * 10
        :param low_price: session low price as pennies * 10
        :param close_price: session close price as pennies * 10
        :param volume: session volume
        :param open_interest: open interest (as necessary)
        """
        self.task_id = 0
        self.name_id = name_id
        self.date = date
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.volume = volume
        self.open_interest = open_interest

    def __repr__(self):
        return "<price_session(%d, %s)>" % (self.name_id, self.date)

class TaskLog(Base):
    """
    All mythic recorder operations have a "task" to track operations
    """
    __tablename__ = 'task_log'

    id = Column(BigInteger, primary_key=True)
    time_stamp = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    command = Column(String(128), nullable=False)

    def __init__(self, command):
        """
        Create a TaskLog
        :param command: task command, i.e. census, dumper, driver
        """
        self.command = command

    def __repr__(self):
        return "<task_log(%s)>" % (self.command)

class SqlTable:
    """
    SQL administration
    """
    def __init__(self, context):
        engine = create_engine(context.mysql_url, echo=False)
        Base.metadata.create_all(engine)

        self.session_maker = sessionmaker()
        self.session_maker.configure(bind=engine)

    def session_factory(self):
        return self.session_maker()