-- Create Database
CREATE DATABASE aptitude_test;
USE aptitude_test;

-- Create Table
CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question TEXT NOT NULL,
    option1 VARCHAR(255),
    option2 VARCHAR(255),
    option3 VARCHAR(255),
    option4 VARCHAR(255),
    correct_option VARCHAR(10)
);

-- Insert Questions
INSERT INTO questions 
(question, option1, option2, option3, option4, correct_option)
VALUES
('2 + 2 = ?', '1', '2', '3', '4', '4'),
('Capital of India?', 'Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Delhi'),
('What is 10 + 20?', '20', '30', '40', '50', '30'),
('Find the next number: 2, 4, 8, ?', '10', '12', '15', '16', '16'),
('What is the square of 5?', '10', '20', '25', '30', '25'),
('If A = 1, B = 2, what is C?', '1', '2', '3', '4', '3'),
('What is 15% of 200?', '25', '30', '35', '40', '30'),
('How many days are there in a week?', '5', '6', '7', '8', '7');

-- View All Questions
SELECT * FROM questions;
