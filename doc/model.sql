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
    add_sub_store varchar(20),
    update_date varchar(15),
    primary key (private_name)
) character set = utf8;