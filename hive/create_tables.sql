CREATE DATABASE IF NOT EXISTS smart_canteen;

USE smart_canteen;

CREATE EXTERNAL TABLE IF NOT EXISTS food_waste (
    food_date STRING,
    food_item STRING,
    prepared_quantity INT,
    sold_quantity INT,
    leftover_quantity INT,
    meal_type STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 'hdfs://master:9000/user/hduser/smart_canteen/input'
TBLPROPERTIES ('skip.header.line.count'='1');

SHOW TABLES;

DESCRIBE food_waste;
