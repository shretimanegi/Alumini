-- mysql_schema.sql
CREATE DATABASE IF NOT EXISTS alumni_db;
USE alumni_db;

CREATE TABLE IF NOT EXISTS departments (
  department_id INT AUTO_INCREMENT PRIMARY KEY,
  department_name VARCHAR(150) NOT NULL
);

CREATE TABLE IF NOT EXISTS batches (
  batch_id INT AUTO_INCREMENT PRIMARY KEY,
  batch_year INT NOT NULL
);

CREATE TABLE IF NOT EXISTS alumni (
  alumni_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  email VARCHAR(200) NOT NULL UNIQUE,
  phone VARCHAR(50),
  batch_id INT,
  department_id INT,
  current_position VARCHAR(200),
  password VARCHAR(255) NOT NULL,
  FOREIGN KEY (batch_id) REFERENCES batches(batch_id),
  FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE IF NOT EXISTS students (
  student_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  email VARCHAR(200) NOT NULL UNIQUE,
  phone VARCHAR(50),
  batch_id INT,
  department_id INT,
  password VARCHAR(255) NOT NULL,
  FOREIGN KEY (batch_id) REFERENCES batches(batch_id),
  FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE IF NOT EXISTS events (
  event_id INT AUTO_INCREMENT PRIMARY KEY,
  event_title VARCHAR(255) NOT NULL,
  event_date DATE NOT NULL,
  event_description TEXT,
  created_by INT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (created_by) REFERENCES alumni(alumni_id)
);

CREATE TABLE IF NOT EXISTS donations (
  donation_id INT AUTO_INCREMENT PRIMARY KEY,
  alumni_id INT,
  amount FLOAT NOT NULL,
  purpose VARCHAR(255),
  date DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (alumni_id) REFERENCES alumni(alumni_id)
);

CREATE TABLE IF NOT EXISTS mentorships (
  mentor_id INT AUTO_INCREMENT PRIMARY KEY,
  alumni_id INT,
  student_id INT,
  status VARCHAR(50) DEFAULT 'pending',
  requested_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (alumni_id) REFERENCES alumni(alumni_id),
  FOREIGN KEY (student_id) REFERENCES students(student_id)
);

CREATE TABLE IF NOT EXISTS jobs (
  job_id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  posted_by INT,
  deadline DATE,
  FOREIGN KEY (posted_by) REFERENCES alumni(alumni_id)
);
