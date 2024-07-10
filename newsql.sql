-- Table for storing administrators
CREATE TABLE Admins (
    admin_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL
);

-- Table for storing teachers
CREATE TABLE Teachers (
    teacher_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL
);

-- Table for storing students
CREATE TABLE Students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL
);

-- Table for storing tests
CREATE TABLE Tests (
    test_id INT PRIMARY KEY AUTO_INCREMENT,
    test_name VARCHAR(100) NOT NULL,
    teacher_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES Teachers(teacher_id)
);

-- Table for storing questions
CREATE TABLE Questions (
    question_id INT PRIMARY KEY AUTO_INCREMENT,
    question_text TEXT NOT NULL,
    test_id INT,
    FOREIGN KEY (test_id) REFERENCES Tests(test_id)
);

-- Table for storing expected answers
CREATE TABLE ExpectedAnswers (
    expected_answer_id INT PRIMARY KEY AUTO_INCREMENT,
    answer_text TEXT NOT NULL,
    question_id INT,
    FOREIGN KEY (question_id) REFERENCES Questions(question_id)
);

-- Table for storing the relationship between teachers and students
 CREATE TABLE TeacherStudentRelationship (
    relationship_id INT PRIMARY KEY AUTO_INCREMENT,
    teacher_id INT,
    student_id INT,
    FOREIGN KEY (teacher_id) REFERENCES Teachers(teacher_id),
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);

-- Table for storing student test attempts and scores
CREATE TABLE StudentTestAttempts (
    attempt_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    test_id INT,
    score DECIMAL(5,2),
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (test_id) REFERENCES Tests(test_id)
);

-- Table for storing student answers
CREATE TABLE StudentAnswers (
    answer_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    test_id INT,
    question_id INT,
    answer_text TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (test_id) REFERENCES Tests(test_id),
    FOREIGN KEY (question_id) REFERENCES Questions(question_id)
);

-- Dummy data for Admins table
INSERT INTO Admins (username, password) VALUES ('admin1', 'adminpassword1');

-- Dummy data for Teachers table
INSERT INTO Teachers (username, password) VALUES 
('teacher1', 'teacherpassword1'),
('teacher2', 'teacherpassword2');

-- Dummy data for Students table
INSERT INTO Students (username, password) VALUES 
('student1', 'studentpassword1'),
('student2', 'studentpassword2'),
('student3', 'studentpassword3');

-- Dummy data for Tests table
INSERT INTO Tests (test_name, teacher_id) VALUES 
('Math Test 1', 1),
('Science Test 1', 2);

-- Dummy data for Questions table
INSERT INTO Questions (question_text, test_id) VALUES 
('What is 2 + 2?', 1),
('What is the capital of France?', 2);

-- Dummy data for ExpectedAnswers table
INSERT INTO ExpectedAnswers (answer_text, question_id) VALUES 
('4', 1),
('Paris', 2);

-- Dummy data for TeacherStudentRelationship table
INSERT INTO TeacherStudentRelationship (teacher_id, student_id) VALUES 
(1, 1),
(1, 2),
(2, 3);

-- Dummy data for StudentTestAttempts table
INSERT INTO StudentTestAttempts (student_id, test_id, score) VALUES 
(1, 1, 90),
(2, 1, 85),
(3, 2, 80);

-- Dummy data for StudentAnswers table
INSERT INTO StudentAnswers (student_id, test_id, question_id, answer_text) VALUES
(1, 1, 1, '4'),  -- Student 1 answer to Question 1 of Test 1
(2, 1, 1, '5'),  -- Student 2 answer to Question 1 of Test 1
(3, 2, 2, 'Paris');  -- Student 3 answer to Question 2 of Test 2