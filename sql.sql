
CREATE TABLE bookings(
id int auto_increment primary key,
date_booking datetime,
time_slot int
location varchar(50));


CREATE TABLE done_bookings(
kroon_id varchar(50) primary key,
book_id int,
FOREIGN KEY (book_id) REFERENCES bookings (id));
