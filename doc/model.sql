CREATE TABLE stock_great_retail (
    code varchar(10),
    update_date varchar(15),
    shareholder_falling_count INT(2),
    sdlu_great_retail_count INT(2),
    float_share FLOAT(10, 2),
    primary key (code, update_date)
) character set = utf8;

CREATE TABLE stock_private (
    code varchar(10),
    code_name varchar(20),
    update_date varchar(15),
    private_name varchar(300),
    add_sub_store varchar(20),
    primary key (code, update_date)
) character set = utf8;

CREATE TABLE stock_private1 (
    private_name varchar(100),
    code_name varchar(20),
    add_sub_store varchar(100),
    update_date varchar(100),
    primary key (private_name)
) character set = utf8;

CREATE TABLE stock_kdj (
    id INT AUTO_INCREMENT,
    code varchar(100),
    code_name varchar(20),
    update_date varchar(100),
    if_gold_cross INT(5) default 0,
    shareholder_falling_count INT(2),
    sdlu_great_retail_count INT(2),
    float_share FLOAT(10, 2),
    macd_gold_cross INT(5) default 0,
    macd_dif FLOAT(10, 2),
    macd_dea FLOAT(10, 2),
    primary key (id)
) character set = utf8;

 //金叉是1，死叉是2，无是0

 drop table stock_kdj;