CREATE TABLE stock_great_retail (
    code varchar(10),
    update_date varchar(15),
    shareholder_falling_count INT(2),
    sdlu_great_retail_count INT(2),
    float_share FLOAT(10, 2),
    primary key (code, update_date)
) character set = utf8;