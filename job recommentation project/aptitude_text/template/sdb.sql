CREATE DATABASE aptitude_test;
-- 1. Create database
CREATE DATABASE aptitude_test;

-- 2. Use database
USE aptitude_test;

-- 3. Create questions table
CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question TEXT NOT NULL,
    option1 VARCHAR(255) NOT NULL,
    option2 VARCHAR(255) NOT NULL,
    option3 VARCHAR(255) NOT NULL,
    option4 VARCHAR(255) NOT NULL,
    correct_option VARCHAR(10) NOT NULL
);

-- 4. Insert sample questions
INSERT INTO questions 
(question, option1, option2, option3, option4, correct_option)
VALUES
('2 + 2 = ?', '1', '2', '3', '4', '4'),
('Capital of India?', 'Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Delhi'),
('5 * 6 = ?', '11', '25', '30', '35', '30');

-- 5. Check data
SELECT * FROM questions;
