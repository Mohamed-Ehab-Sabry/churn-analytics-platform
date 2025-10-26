CREATE TABLE IF NOT EXISTS customer_churn_data (
    customerID VARCHAR(50) PRIMARY KEY,
    gender VARCHAR(10),
    SeniorCitizen INT,
    Partner VARCHAR(10),
    Dependents VARCHAR(10),
    tenure INT,
    PhoneService VARCHAR(10),
    MultipleLines VARCHAR(30),
    InternetService VARCHAR(30),
    OnlineSecurity VARCHAR(30),
    OnlineBackup VARCHAR(30),
    DeviceProtection VARCHAR(30),
    TechSupport VARCHAR(30),
    StreamingTV VARCHAR(30),
    StreamingMovies VARCHAR(30),
    Contract VARCHAR(30),
    PaperlessBilling VARCHAR(10),
    PaymentMethod VARCHAR(50),
    MonthlyCharges DECIMAL(10,2),
    TotalCharges VARCHAR(20),
    Churn VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS customer_location (
    customerID VARCHAR(50) PRIMARY KEY,
    Zip_Code INT,
    Latitude DECIMAL(10,6),
    Longitude DECIMAL(10,6),
    FOREIGN KEY (customerID) REFERENCES customer_churn_data(customerID)
);

CREATE TABLE IF NOT EXISTS zip_population (
    Zip_Code INT PRIMARY KEY,
    Population INT
);