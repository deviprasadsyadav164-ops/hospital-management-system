-- Schema only: no patient or other personal seed data is included.
CREATE TABLE Department (
    dept_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL,
    location VARCHAR(100)
);

-- Doctor Table
CREATE TABLE Doctor (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100),
    phone VARCHAR(15),
    email VARCHAR(100),
    dept_id INT,
    FOREIGN KEY (dept_id) REFERENCES Department(dept_id)
);

-- Patient Table
CREATE TABLE Patient (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(100) NOT NULL,
    age INT,
    gender VARCHAR(10),
    phone VARCHAR(15),
    address VARCHAR(255),
    blood_group VARCHAR(5)
);

-- Appointment Table
CREATE TABLE Appointment (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    appointment_date DATE,
    appointment_time TIME,
    status VARCHAR(20) DEFAULT 'Scheduled',

    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctor(doctor_id)
);

-- Room Table
CREATE TABLE Room (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    room_number VARCHAR(10),
    room_type VARCHAR(50),
    charges DECIMAL(10,2)
);

-- Admission Table
CREATE TABLE Admission (
    admission_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    room_id INT,
    admit_date DATE,
    discharge_date DATE,

    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id),
    FOREIGN KEY (room_id) REFERENCES Room(room_id)
);

-- Staff Table
CREATE TABLE Staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    staff_name VARCHAR(100),
    designation VARCHAR(100),
    phone VARCHAR(15),
    salary DECIMAL(10,2)
);

-- Medicine Table
CREATE TABLE Medicine (
    medicine_id INT AUTO_INCREMENT PRIMARY KEY,
    medicine_name VARCHAR(100),
    manufacturer VARCHAR(100),
    price DECIMAL(10,2),
    stock INT
);

-- Prescription Table
CREATE TABLE Prescription (
    prescription_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    medicine_id INT,
    dosage VARCHAR(100),
    duration VARCHAR(50),

    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctor(doctor_id),
    FOREIGN KEY (medicine_id) REFERENCES Medicine(medicine_id)
);

-- Bill Table
CREATE TABLE Bill (
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    total_amount DECIMAL(10,2),
    payment_status VARCHAR(20),

    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id)
);
SELECT * FROM Department;
SELECT * FROM Doctor;
SELECT * FROM Patient;
SELECT * FROM Appointment;
SELECT * FROM Bill;
SELECT patient_id, patient_name, age, gender, phone, address, blood_group FROM Patient WHERE age > 30;