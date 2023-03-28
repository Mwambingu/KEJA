CREATE DATABASE IF NOT EXISTS KejaFlask;
CREATE USER IF NOT EXISTS 'keja_flask_user'@'localhost' identified with mysql_native_password by "kejaflask001";
GRANT ALL PRIVILEGES ON KejaFlask.* TO 'keja_flask_user'@'localhost';
FLUSH PRIVILEGES;
