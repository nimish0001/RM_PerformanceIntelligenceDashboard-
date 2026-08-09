                                    =====+=========   BUSINESS QUESTIONS   ===============

                                      
                                      
-- Ques-1) Who are the top-performing RMs based on total sales generated?
SELECT
    R.RM_ID,
    R.RM_Name,
    SUM(S.Amount) AS Total_Sales
FROM RM_Master R
JOIN Sales S
    ON R.RM_ID = S.RM_ID
GROUP BY
    R.RM_ID,
    R.RM_Name
ORDER BY Total_Sales DESC
LIMIT 10;



-- Ques-2) Which RMs sell the widest variety of products?
SELECT
    R.RM_ID,
    R.RM_Name,
    COUNT(DISTINCT S.Product) AS Products_Sold
FROM RM_Master R
JOIN Sales S
    ON R.RM_ID = S.RM_ID
GROUP BY
    R.RM_ID,
    R.RM_Name
ORDER BY Products_Sold DESC
LIMIT 10;



-- Ques-3) Which RMs manage the highest number of customers?
SELECT
    R.RM_ID,
    R.RM_Name,
    COUNT(C.Customer_ID) AS Customers_Managed
FROM RM_Master R
JOIN Customers C
    ON R.RM_ID = C.RM_ID
GROUP BY
    R.RM_ID,
    R.RM_Name
ORDER BY Customers_Managed DESC
LIMIT 10;



-- Ques-4) Which RMs have the highest customer satisfaction?
SELECT
    R.RM_ID,
    R.RM_Name,
    COUNT(F.Customer_ID) AS Feedback_Count,
    ROUND(AVG(F.Rating), 2) AS Average_Rating
FROM RM_Master R
JOIN Feedback F
    ON R.RM_ID = F.RM_ID
GROUP BY
    R.RM_ID,
    R.RM_Name
HAVING COUNT(F.Customer_ID) >= 5
ORDER BY Average_Rating DESC
LIMIT 10;



-- Ques-5) Which RMs have the highest number of complaints?
SELECT
    R.RM_ID,
    R.RM_Name,
    COUNT(C.Complaint_ID) AS Complaint_Count,
    ROUND(AVG(C.Resolution_Time), 2) AS Avg_Resolution_Time
FROM RM_Master R
JOIN Complaints C
    ON R.RM_ID = C.RM_ID
GROUP BY
    R.RM_ID,
    R.RM_Name
ORDER BY Complaint_Count DESC
LIMIT 10;



-- Ques-6) Which RMs are between 30 and 40 years old?
SELECT
    RM_ID,
    RM_Name,
    Age,
    Experience,
    City
FROM RM_Master
WHERE Age BETWEEN 30 AND 40
ORDER BY Age;



-- Ques-7) Which female RMs have more than 5 years of experience?
SELECT
    RM_ID,
    RM_Name,
    Gender,
    Age,
    Experience,
    City
FROM RM_Master
WHERE Gender = 'F'
  AND Experience > 5
ORDER BY Experience DESC;



-- Ques-8)  Which male RMs have more than 6 years of experience?
SELECT
    RM_ID,
    RM_Name,
    Gender,
    Age,
    Experience,
    City
FROM RM_Master
WHERE Gender = 'M'
  AND Experience > 6
ORDER BY Experience DESC;



-- Ques-9) Which RMs sold Fixed Deposit or Life Insurance?
SELECT
    R.RM_ID,
    R.RM_Name,
    S.Product,
    SUM(S.Amount) AS Total_Sales
FROM RM_Master R
JOIN Sales S
    ON R.RM_ID = S.RM_ID
WHERE S.Product IN ('Fixed Deposit', 'Life Insurance')
GROUP BY
    R.RM_ID,
    R.RM_Name,
    S.Product
ORDER BY Total_Sales DESC;



-- Ques-10) Which RMs achieved more than 100% in a particular month?
SELECT
    R.RM_ID,
    R.RM_Name,
    T.Month,
    T.Target,
    T.Achievement,
    T.Achievement_Pct
FROM RM_Master R
JOIN Targets T
    ON R.RM_ID = T.RM_ID
WHERE T.Month = '2023-01'
  AND T.Achievement_Pct > 100
ORDER BY T.Achievement_Pct DESC;



-- Ques-11) Which RMs have customers from the Premium segment?
SELECT
    R.RM_ID,
    R.RM_Name,
    COUNT(C.Customer_ID) AS Premium_Customers
FROM RM_Master R
JOIN Customers C
    ON R.RM_ID = C.RM_ID
WHERE C.Segment = 'Premium'
GROUP BY
    R.RM_ID,
    R.RM_Name
ORDER BY Premium_Customers DESC;



-- Ques-12) Which RMs are above the average RM sales performance?
WITH RM_Sales AS
(
    SELECT
        RM_ID,
        SUM(Amount) AS Total_Sales
    FROM Sales
    GROUP BY RM_ID
)

SELECT
    R.RM_ID,
    R.RM_Name,
    S.Total_Sales
FROM RM_Sales S
JOIN RM_Master R
    ON S.RM_ID = R.RM_ID
WHERE S.Total_Sales >
(
    SELECT AVG(Total_Sales)
    FROM RM_Sales
)
ORDER BY S.Total_Sales DESC;



--------------------------------------------------------------------- END ---------------------------------------------------------------------------------------
