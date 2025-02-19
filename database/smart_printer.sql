-- Active: 1739980350011@@localhost@3306
CREATE DATABASE IF NOT EXISTS smart_printer;
USE smart_printer;

-- Table to store user print requests
CREATE TABLE IF NOT EXISTS print_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    copies INT NOT NULL,
    color ENUM('black_white', 'color') NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    payment_status ENUM('pending', 'completed') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table to store payment transactions
CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    print_request_id INT NOT NULL,
    order_id VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'paid', 'failed') DEFAULT 'pending',
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (print_request_id) REFERENCES print_requests(id) ON DELETE CASCADE
);
