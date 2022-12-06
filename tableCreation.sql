CREATE TABLE `airline` (
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `airline_staff` (
  `date_of_birth` date DEFAULT NULL,
  `username` varchar(255) NOT NULL,
  `airline_name` varchar(255) NOT NULL,
  `passwd` varchar(255) NOT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `airplane` (
  `id` int(11) NOT NULL,
  `airline_name` varchar(255) NOT NULL,
  `manufacturer` varchar(255) DEFAULT NULL,
  `seats` int(11) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `airport` (
  `name` varchar(255) NOT NULL,
  `city` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `type` varchar(13) DEFAULT NULL,
  PRIMARY KEY(`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `customer` (
  `email` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `pass` varchar(127) NOT NULL,
  `building_num` int(11) DEFAULT NULL,
  `street` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  `phone_number` varchar(10) DEFAULT NULL,
  `passport_num` int(11) DEFAULT NULL,
  `passport_exp` date DEFAULT NULL,
  `passport_country` varchar(255) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  PRIMARY KEY(`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `flight` (
  `flight_num` int(11) NOT NULL,
  `airline_name` varchar(255) NOT NULL,
  `depart_date_time` datetime NOT NULL,
  `departure_airport` varchar(255) DEFAULT NULL,
  `arrival_airport` varchar(255) DEFAULT NULL,
  `airplane_id` int(11) DEFAULT NULL,
  `arrive_date_time` datetime DEFAULT NULL,
  `base_price` int(11) DEFAULT NULL,
  `stat` varchar(255) DEFAULT NULL,
  PRIMARY KEY(`flight_num`),
  FOREIGN KEY(`airline_name`) REFERENCES airline(`name`),
  FOREIGN KEY(`airplane_id`) REFERENCES airplane(`id`),
  FOREIGN KEY(`departure_airport`) REFERENCES airport(`name`),
  FOREIGN KEY(`arrival_airport`) REFERENCES airport(`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `review` (
  `flight_num` int(11) NOT NULL,
  `depart_date_time` datetime NOT NULL,
  `airline_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `rating` int(5) DEFAULT NULL,
  `review` varchar(4000) DEFAULT NULL,
  FOREIGN KEY(`flight_num`) REFERENCES flight(`flight_num`),
  FOREIGN KEY(`airline_name`) REFERENCES airline(`name`),
  FOREIGN KEY(`email`) REFERENCES customer(`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `staff_email` (
  `email` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  PRIMARY KEY(`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `staff_phone` (
  `phone_number` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  FOREIGN KEY(`username`) REFERENCES staff_email(`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `ticket` (
  `ticket_id` int(11) NOT NULL,
  `customer_email` varchar(255) DEFAULT NULL,
  `airline_name` varchar(255) DEFAULT NULL,
  `flight_num` int(11) DEFAULT NULL,
  `card_type` varchar(6) DEFAULT NULL,
  `card_name` varchar(21) DEFAULT NULL,
  `card_num` int(16) DEFAULT NULL,
  `exp_date` date DEFAULT NULL,
  `sold_price` int(11) DEFAULT NULL,
  `purchase_date_time` datetime DEFAULT NULL,
  PRIMARY KEY(`ticket_id`),
  FOREIGN KEY(`customer_email`) REFERENCES customer(`email`),
  FOREIGN KEY(`airline_name`) REFERENCES airline(`name`),
  FOREIGN KEY(`flight_num`) REFERENCES flight(`flight_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;