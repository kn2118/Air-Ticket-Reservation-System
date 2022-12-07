INSERT INTO `airline` (`name`) VALUES
('Jet Blue');

INSERT INTO `airline_staff` (`date_of_birth`, `username`, `airline_name`, `passwd`, `first_name`, `last_name`) VALUES
(NULL, 'bz1148', 'Jet Blue', 'aPassword123', 'Barry', 'Zhang'),
(NULL, 'kn2118', 'Jet Blue', 'aPassword456', 'Kevin', 'Ng');

INSERT INTO `airplane` (`id`, `airline_name`, `manufacturer`, `seats`, `age`) VALUES
(1, 'Jet Blue', 'Lockheed Martin', 900, 5),
(2, 'Jet Blue', 'Boeing', 300, 3),
(3, 'Jet Blue', 'Boeing', 300, 6);

INSERT INTO `airport` (`name`, `city`, `country`, `type`) VALUES
('JFK', 'New\r\nYork City', 'United States of America', 'BOTH'),
('PVG', 'Shanghai', 'China', 'BOTH');

INSERT INTO `customer` (`email`, `username`, `name`, `pass`, `building_num`, `street`, `city`, `state`, `phone_number`, `passport_num`, `passport_exp`, `passport_country`, `dob`) VALUES
('homer@gmail.com', 'homer', 'Homer Simpson', 'HomerSimpson123', 35, 'Bobby St', 'Queens', 'New\r\nYork', '3456789012', 98765432, '2024-08-02', 'United States of\r\nAmerica', '2000-03-03'),
('mickey@gmail.com', 'mickey', 'Mickey Mouse', 'MickeyMouseClubHouse123', 2, 'MetroTech Ctr', 'Brooklyn', 'New\r\nYork', '1234567890', 123456789, '2023-01-01', 'United States of\r\nAmerica', '2001-01-28'),
('Scooby@yahoo.com', 'scooby', 'Scooby Doo', 'ScoobyDoobyDoo123', 123, 'Atlantic Avenue', 'Brooklyn', 'New\r\nYork', '2345678901', 10101010, '2023-02-02', 'United States of\r\nAmerica', '2002-02-02');
('test@nyu.edu', 'apple', 'Nidhi', '123', 12820, 'Viscaino Rd', 'Los Altos Hills', 'CA', '123', '321', '2029-09-09', 'USA', '2003-03-07');

INSERT INTO `flight` (`flight_num`, `airline_name`, `depart_date_time`, `departure_airport`, `arrival_airport`, `airplane_id`, `arrive_date_time`, `base_price`, `stat`) VALUES
(1, 'Jet Blue', '2023-01-02 01:02:00', 'JFK', 'PVG', 1, '2023-01-02 16:00:00', 2000, 'DELAYED'),
(2, 'Jet Blue', '2023-02-03 02:03:00', 'PVG', 'JFK', 2, '2023-02-03 16:30:30', 1950, 'ON TIME'),
(3, 'Jet Blue', '2022-12-05 15:55:00', 'PVG', 'JFK', 2, '2022-12-06 12:30:30', 1950, 'ON TIME'),
(4, 'Jet Blue', '2022-11-25 06:30:00', 'JFK', 'PVG', 1, '2022-11-25 21:30:30', 1950, 'DELAYED');

INSERT INTO `ticket` (`ticket_id`, `customer_email`, `airline_name`, `flight_num`, `card_type`, `card_name`, `card_num`, `exp_date`, `sold_price`, `purchase_date_time`) VALUES
(1, 'mickey@gmail.com', 'Jet Blue', 1, 'DEBIT', 'VISA', 2147483647, '2023-01-01', 1950, '2022-11-05 11:44:00'),
(2, 'Scooby@yahoo.com', 'Jet Blue', 2, 'CREDIT', 'VISA', 2147483647, '2023-02-02', 2050, '2022-11-06 12:44:00'),
(3, 'homer@gmail.com', 'Jet Blue', 3, 'CREDIT', 'VISA', 2147483647, '2023-03-03', 2000, '2022-11-07 12:44:00'),
(4, 'test@nyu.edu', 'Jet Blue', 4, 'DEBIT', 'VISA', 2147483647, '2023-01-01', 1950, '2021-11-05 11:44:00');

