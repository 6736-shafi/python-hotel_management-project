create or replace TABLE HOTEL.PUBLIC.BOOKINGS (
	BOOKING_ID NUMBER(38,0) NOT NULL autoincrement start 1 increment 1 noorder,
	PAYMENT_ID NUMBER(38,0),
	ROOM_ID NUMBER(38,0),
	CUSTOMER_ID NUMBER(38,0),
	CHECK_IN DATE,
	CHECK_OUT DATE,
	STATUS VARCHAR(16777216) DEFAULT 'CONFIRMED',
	CREATED_AT TIMESTAMP_NTZ(9) DEFAULT CURRENT_TIMESTAMP(),
	TOTAL_AMOUNT NUMBER(10,2) NOT NULL DEFAULT 0,
	CANCELLATION_STATUS VARCHAR(16777216) DEFAULT 'NOT_CANCELLED',
	CANCELLATION_TIMESTAMP TIMESTAMP_NTZ(9),
	primary key (BOOKING_ID),
	foreign key (CUSTOMER_ID) references HOTEL.PUBLIC.CUSTOMERS(CUSTOMER_ID),
    foreign key (PAYMENT_ID) references HOTEL.PUBLIC.PAYMENTS(PAYMENT_ID),
    foreign key (ROOM_ID) references HOTEL.PUBLIC.ROOMS(ROOM_ID)
);





create or replace TABLE HOTEL.PUBLIC.CUSTOMERS (
	CUSTOMER_ID NUMBER(38,0) NOT NULL autoincrement start 1 increment 1 noorder,
	FIRST_NAME VARCHAR(50) NOT NULL,
	LAST_NAME VARCHAR(50) NOT NULL,
	EMAIL VARCHAR(100) NOT NULL,
	PASSWORD VARCHAR(100) NOT NULL,
	PHONE_NUMBER VARCHAR(15),
	CREATED_AT TIMESTAMP_NTZ(9) DEFAULT CURRENT_TIMESTAMP(),
	unique (EMAIL),
	unique (PASSWORD),
	primary key (CUSTOMER_ID)
);




create or replace TABLE HOTEL.PUBLIC.PAYMENTS (
	PAYMENT_ID NUMBER(38,0) NOT NULL autoincrement start 1 increment 1 noorder,
	ROOM_ID NUMBER(38,0),
	PAYMENT_DATE TIMESTAMP_NTZ(9) DEFAULT CURRENT_TIMESTAMP(),
	AMOUNT NUMBER(10,2) NOT NULL,
	ISREFUND BOOLEAN DEFAULT FALSE,
	REFUNDED_AMOUNT FLOAT DEFAULT 0,
	primary key (PAYMENT_ID)
);




create or replace TABLE HOTEL.PUBLIC.ROOMS (
	ROOM_ID NUMBER(38,0) NOT NULL,
	ROOM_TYPE VARCHAR(16777216),
	PRICE FLOAT,
	IS_AVAILABLE BOOLEAN,
	primary key (ROOM_ID)
);