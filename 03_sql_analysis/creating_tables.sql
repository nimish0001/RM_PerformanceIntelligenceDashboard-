CREATE DATABASE RM_Performance;
USE RM_Performance;

-- =====================================================
-- 1. RM MASTER TABLE
-- =====================================================

CREATE TABLE RM_Master (
    RM_ID VARCHAR(10) PRIMARY KEY,
    RM_Name VARCHAR(100),
    City VARCHAR(50),
    Age INT,
    Gender VARCHAR(10),
    Joining_Date DATETIME,
    Experience DECIMAL(4,1)
);


-- =====================================================
-- 2. CUSTOMERS TABLE
-- =====================================================

CREATE TABLE Customers (
    Customer_ID VARCHAR(15) PRIMARY KEY,
    RM_ID VARCHAR(10),
    Age INT,
    Gender VARCHAR(10),
    City VARCHAR(50),
    Income INT,
    Segment VARCHAR(20),

    FOREIGN KEY (RM_ID)
        REFERENCES RM_Master(RM_ID)
);


-- =====================================================
-- 3. LOANS TABLE
-- =====================================================

CREATE TABLE Loans (
    Loan_ID VARCHAR(15) PRIMARY KEY,
    Customer_ID VARCHAR(15),
    RM_ID VARCHAR(10),
    Loan_Type VARCHAR(50),
    Loan_Amount INT,
    Loan_Status VARCHAR(20),

    FOREIGN KEY (Customer_ID)
        REFERENCES Customers(Customer_ID),

    FOREIGN KEY (RM_ID)
        REFERENCES RM_Master(RM_ID)
);


-- =====================================================
-- 4. SALES TABLE
-- =====================================================

CREATE TABLE Sales (
    RM_ID VARCHAR(10),
    Product VARCHAR(50),
    Sale_Date DATETIME,
    Amount INT,

    FOREIGN KEY (RM_ID)
        REFERENCES RM_Master(RM_ID)
);


-- =====================================================
-- 5. TARGETS TABLE
-- =====================================================

CREATE TABLE Targets (
    RM_ID VARCHAR(10),
    Month CHAR(7),
    Target INT,
    Achievement INT,
    Achievement_Pct DECIMAL(7,2),

    FOREIGN KEY (RM_ID)
        REFERENCES RM_Master(RM_ID)
);


-- =====================================================
-- 6. COMPLAINTS TABLE
-- =====================================================

CREATE TABLE Complaints (
    Complaint_ID VARCHAR(15) PRIMARY KEY,
    Customer_ID VARCHAR(15),
    RM_ID VARCHAR(10),
    Complaint_Type VARCHAR(50),
    Resolution_Time INT,
    Resolution_Status VARCHAR(20),

    FOREIGN KEY (Customer_ID)
        REFERENCES Customers(Customer_ID),

    FOREIGN KEY (RM_ID)
        REFERENCES RM_Master(RM_ID)
);


-- =====================================================
-- 7. FEEDBACK TABLE
-- =====================================================

CREATE TABLE Feedback (
    Customer_ID VARCHAR(15),
    RM_ID VARCHAR(10),
    Rating DECIMAL(2,1),
    Feedback_Date DATETIME,
    City VARCHAR(50),
    Sentiment VARCHAR(20),

    FOREIGN KEY (Customer_ID)
        REFERENCES Customers(Customer_ID),

    FOREIGN KEY (RM_ID)
        REFERENCES RM_Master(RM_ID)
);


-- =====================================================
-- VERIFY TABLES
-- =====================================================rm_master

SHOW TABLES;
