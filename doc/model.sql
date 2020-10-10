CREATE TABLE stock_great_retail (
    id INT AUTO_INCREMENT,
    code varchar(10),
    update_date varchar(15),
    shareholder_falling_count INT(2),
    sdlu_great_retail_count INT(2),
    float_share FLOAT(10, 2),
    primary key (id)
) character set = utf8;