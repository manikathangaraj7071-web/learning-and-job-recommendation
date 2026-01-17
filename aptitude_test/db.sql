CREATE DATABASE aptitude_test;
USE aptitude_test;

CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question TEXT,
    option_a VARCHAR(255),
    option_b VARCHAR(255),
    option_c VARCHAR(255),
    option_d VARCHAR(255),
    correct_option CHAR(1)
);

INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_option) VALUES
('What is 10 + 20?', '20', '30', '40', '50', 'B'),
('Find the next number: 2, 4, 8, ?', '10', '12', '16', '18', 'C'),
('What is the square of 5?', '10', '20', '25', '30', 'C'),
('If A = 1, B = 2, what is C?', '1', '2', '3', '4', 'C'),
('What is 15% of 200?', '25', '30', '35', '40', 'B');
