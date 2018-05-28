# mythic-recorder-py
Store your data from https://eoddata.com in a https://www.mysql.com database.

***

https://eoddata.com provides stock market price information as a commercial service.  You can acquire data from a variety of mechanisms including their "data client" which only runs on windows.  

I have a AWS EC2 instance w/windows which I to harvest information from https://eoddata.com once a week.  Once "data client" has completed the download I zip the current week and migrate it to an UNIX EC2 instance where proper tools exist for analysis.

"mythic recorder" is a python3 application which parses the files created by "data client" and writes the results to a MySQL database.  I have been collecting files from eoddata.com for several years and have a largish data set.  Despite the size mythic-recorder/MySQL continue to perform well on a AWS M5 instance.

"data client" writes XML and CSV files depending upon the content.  Symbol lists and exchange lists are XML files while price quotes are CSV files.  The raw directory hierarchy is segragated by market, which will contain session quotes and symbol lists.  Note that a directory named "5" resides within some directories, these contain 5 minute bar files.  A representative data set is provided witin the "EODData" directory.

****

## Installation (AWS EC2)

1. Create a SQS queue and enable SES (Simple Email Service).  mythic recorder will email for important issues.

1. Create a EC2 instance to host the application.  I use a M5 instance w/Amazon LINUX and a 333GB file system.

1. Move the mythic-recorder sources onto host

1. Install python3 and MySQL server.

    1. Install a user and application schema (from the "mysql" directory)

    1. i.e. mysql -u root -p mythic_recruiter_v1 < mythic_recruiter_v1.sql

1. pip install -r requirements.txt for application dependencies

1. Update the config.dev file to reflect your MySQL configuration and SQS ARN.  
    1. Note that "importDir" must point to the eoddata directory
    
1. Start the application by invoking "loader.py"

1. You can monitor progress by selecting from the "application_log" table.

### Application Notes

1. Every load operation is a "task", with an entry in "task_log" table.  You will see references to "task_log" scattered throughout the applications, this is to help determine when certain rows appeared in the data set.

1. Logging is stored within MySQL in the "application_log" table

1. When the application starts ("loader.py") I build a catalog of eoddata.com files.  
    1. file_stat table contains a row for each file, along w/a SHA1 checksum to suppress duplicate files from being loaded.
    1. load_log table contains a row for each file which requires loading.  load_log also contains load statistics
        1. duration = total time in seconds to load the file
        1. exchange = source market/exchange
        1. file_name = source file
        1. normalized_name = parent directory/source_file (required to uniquely identify files)
        1. total_pop = total row count for file
        1. fresh_pop = fresh rows within file
        1. duplicate_pop = duplicate rows (might be from previous file)
        1. update_pop = rows which were updated (known from previous file)
        1. fail_pop = rows which did not parse
        1. stub_pop = price rows which did not have an existing entry in name table
        
1. "load_log_summary" table contains a summary for entire load

1. "exchange" table defines known markets/exchanges

1. "name" table defines name/market affiliation.  A ticker symbol must be unique within a market.  It is common for eoddata price files to contain undefined ticker symbols.  I add these to "name" as encountered (called "stub names").

1. "price_session" table contains quotes for a session.

1. "price_intraday" table contains quotes for intraday bars, in my case 5 minute bars.

### Example

1. Discover the name.id for AAPL

```
select * from name where symbol = 'AAPL';

```

2. Select session price for AAPL
```
select * from price_session where name_id = 24594 order by date;

```

3. Select 5 minute bars for AAPL;
```
select * from price_intraday where name_id = 24594 order by date;

```