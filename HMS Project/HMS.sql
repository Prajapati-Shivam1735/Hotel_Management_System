create database hotel_management;
use hotel_management;
CREATE TABLE customers (
    ref VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100),
    fname VARCHAR(100),
    gender VARCHAR(10),
    pincode VARCHAR(10),
    mobile VARCHAR(15),
    email VARCHAR(100),
    nationality VARCHAR(50),
    id_proof VARCHAR(50),
    id_number VARCHAR(50),
    address TEXT
);
SELECT * FROM customers WHERE mobile
SELECT * FROM room
SHOW CREATE TABLE room;

