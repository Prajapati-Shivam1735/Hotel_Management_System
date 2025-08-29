CREATE DATABASE hotel_db;
USE hotel_db;

CREATE TABLE customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(15),
    email VARCHAR(100)
);

CREATE TABLE rooms (
    id INT PRIMARY KEY AUTO_INCREMENT,
    room_number VARCHAR(10) NOT NULL,
    room_type VARCHAR(50),
    price DECIMAL(10,2),
    status ENUM('Available', 'Booked') DEFAULT 'Available'
);

CREATE TABLE bookings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    room_id INT,
    check_in DATE,
    check_out DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (room_id) REFERENCES rooms(id)
);
