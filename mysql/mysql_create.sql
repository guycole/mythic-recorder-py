--
-- mysql -u root < mysql_create.sql
--
create database mythic_recorder_v1;
--
--
create user 'recorder'@'localhost' identified by 'bogus';
grant all privileges on mythic_recorder_v1.* to 'recorder'@'localhost';
--