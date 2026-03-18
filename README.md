# COMP3161 Lab 3 – Customer Data API

## Overview

This project implements a full data pipeline for managing customer data using **MySQL** and a **Flask REST API**.

The system:

* Extracts customer data from a CSV file
* Stores it in a MySQL database
* Provides API endpoints to retrieve, update, and analyze the data

---

## Features

### Data Processing

* Python script (`generate.py`) converts CSV data into SQL
* Automatically creates database and table
* Inserts all customer records

### REST API (Flask)

The API provides the following endpoints:

#### Core Endpoints

* `GET /customers` – Retrieve all customers
* `GET /customer/<customer_id>` – Retrieve a specific customer
* `POST /add_customer` – Add a new customer
* `PUT /update_profession/<customer_id>` – Update a customer’s profession

#### Analytical Endpoints

* `GET /highest_income_report` – Highest income per profession
* `GET /total_income_report` – Total income per profession
* `GET /average_work_experience` – Average work experience for young high earners
* `GET /average_spending_score/<profession>` – Average spending score by gender

---

## Technologies Used

* Python
* Flask
* MySQL
* Postman (for API testing)

---

## Project Structure

```
comp3161-lab3/
│
├── app.py                         # Flask API
├── generate.py                    # CSV → SQL script generator
├── customer_db.sql                # Database creation + insert script
├── requirements.txt               # Python dependencies
└── COMP3161_Postman_Collection.json  # API test collection
```

---

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Load Database

Open MySQL and run:

```sql
source customer_db.sql;
```

### 3. Run the API

```bash
python app.py
```

The API will be available at:

```
http://127.0.0.1:5000
```

---

## Testing the API

Use Postman to test all endpoints.

Import the provided Postman collection:

```
COMP3161_Postman_Collection.json
```

---

## Example Request

### Add Customer

**POST** `/add_customer`

```json
{
  "CustomerID": 2001,
  "Gender": "Female",
  "Age": 25,
  "AnnualIncome": 50000,
  "SpendingScore": 70,
  "Profession": "Engineer",
  "WorkExperience": 3,
  "FamilySize": 4
}
```

---

## Notes

* Database name: `shop_db`
* Table name: `Customers`
* Profession field allows NULL values
* All SQL queries are parameterized to prevent SQL injection


## Author

Justine Lewis
COMP3161 – University of the West Indies
