USE greentech_db;

CREATE TABLE  `user` (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role ENUM('individual','company') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE company (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    registration_no VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES  `user`(user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE collectionpoint (
    point_id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT NOT NULL,
    location VARCHAR(255) NOT NULL,
    coordinates VARCHAR(100),
    isActive BOOLEAN DEFAULT TRUE,
    map_url VARCHAR(255),
    FOREIGN KEY (company_id) REFERENCES company(company_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE request (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    company_id INT NOT NULL,
    request_date DATE NOT NULL,
    status ENUM('Received','Under Recycling','Recycled') NOT NULL,
    point_id INT,
    FOREIGN KEY (user_id) REFERENCES  `user`(user_id),
    FOREIGN KEY (company_id) REFERENCES company(company_id),
    FOREIGN KEY (point_id) REFERENCES collectionpoint(point_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE device (
    device_id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    `condition` VARCHAR(50),
    request_id INT NOT NULL,
    FOREIGN KEY (request_id) REFERENCES request(request_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE request_history (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    request_id INT NOT NULL,
    status VARCHAR(50) NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (request_id) REFERENCES request(request_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



SHOW TABLES;
DROP DATABASE greentech_db;
CREATE DATABASE greentech_db;
USE greentech_db;
