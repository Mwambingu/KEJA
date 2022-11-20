CREATE DATABASE IF NOT EXISTS Keja_TestDB;
CREATE USER IF NOT EXISTS 'keja_admin'@'localhost' identified with mysql_native_password by "keja001";
GRANT ALL PRIVILEGES ON Keja_TestDB.* TO 'keja_admin'@'localhost';
FLUSH PRIVILEGES;
