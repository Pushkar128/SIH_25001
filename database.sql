CREATE DATABASE newdb;
USE newdb;
CREATE TABLE water_reports (
    ReportID INT AUTO_INCREMENT PRIMARY KEY,
    VillageName VARCHAR(255) NOT NULL,
    WaterSourceID VARCHAR(100),
    ReportDate DATE NOT NULL,
    BacterialLevel DECIMAL(10, 2),
    pHLevel DECIMAL(4, 2),
    TurbidityNTU DECIMAL(10, 2),
    SymptomsObserved TEXT,
    Remarks TEXT
);
USE newdb;
SELECT * FROM water_reports;

CREATE TABLE patient_cases (
    CaseID INT AUTO_INCREMENT PRIMARY KEY,
    CholeraCases INT DEFAULT 0,
    TyphoidCases INT DEFAULT 0,
    HepatitisCases INT DEFAULT 0,
    GiardiasisCases INT DEFAULT 0,
    DysenteryCases INT DEFAULT 0,
    EColiCases INT DEFAULT 0,
    Remarks TEXT,
    ReportDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
SELECT * FROM patient_cases;
CREATE TABLE users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(255) NOT NULL,
    ContactNumber VARCHAR(20),
    EmailID VARCHAR(255) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    MainRole VARCHAR(50) NOT NULL
);
SELECT * FROM users;