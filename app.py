from flask import Flask, jsonify, request
import mysql.connector
import os
#620165751 - lab3 - Creating Flask API for Customers database
app = Flask(__name__)

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE", "shop_db"),
}

#connecting to mysql
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

#storing database row into dictionary so it can be jsonified later
def row_to_dict(row):
    return{
        "customer_id": row[0],
        "gender": row[1],
        "age": row[2],
        "annual_income": row[3],
        "spending_score": row[4],
        "profession": row[5],
        "work_experience": row[6],
        "family_size": row[7],
    }

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Customer API is running"})

@app.route("/customers", methods=["GET"])
def get_customers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT customer_id, gender, age, annual_income, spending_score,
               profession, work_experience, family_size
        FROM Customers
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    customers = [row_to_dict(row) for row in rows]
    return jsonify(customers)


@app.route("/customer/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT customer_id, gender, age, annual_income, spending_score,
               profession, work_experience, family_size
        FROM Customers
        WHERE customer_id = %s
    """, (customer_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row is None:
        return jsonify({"error": "Customer not found"}), 404

    return jsonify(row_to_dict(row))

@app.route("/add_customer", methods=["POST"])
def add_customer():
    data = request.get_json()
    required = ["CustomerID", "Gender", "Age", "AnnualIncome",
        "SpendingScore", "Profession", "WorkExperience", "FamilySize"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    conn=get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
            INSERT INTO Customers
            (customer_id, gender, age, annual_income, spending_score,
            profession, work_experience, family_size)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data["CustomerID"],
            data["Gender"],
            data["Age"],
            data["AnnualIncome"],
            data["SpendingScore"],
            data["Profession"],
            data["WorkExperience"],
            data["FamilySize"]
        ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Customer added successfully"}), 201


@app.route("/update_profession/<int:customer_id>", methods=["PUT"])
def update_profession(customer_id):
    data = request.get_json()

    if not data or "Profession" not in data:
        return jsonify({"error": "Missing field: Profession"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Customers
        SET profession = %s
        WHERE customer_id = %s
    """, (data["Profession"], customer_id))

    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return jsonify({"error": "Customer not found"}), 404

    cursor.close()
    conn.close()

    return jsonify({"message": "Profession updated successfully"})

@app.route("/highest_income_report", methods=["GET"])
def highest_income_report():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT customer_id, profession, annual_income
        FROM Customers
        WHERE (profession, annual_income) IN (
            SELECT profession, MAX(annual_income)
            FROM Customers
            GROUP BY profession
            )
    """)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "CustomerID": row[0],
            "Profession": row[1],
            "AnnualIncome": row[2]
        })

    return jsonify(result)


@app.route("/total_income_report", methods=["GET"])
def total_income_report():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT profession, SUM(annual_income) AS total_income
        FROM Customers
        GROUP BY profession
    """)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "Profession": row[0],
            "TotalIncome": row[1]
        })

    return jsonify(result)


@app.route("/average_work_experience", methods=["GET"])
def average_work_experience():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT profession, ROUND(AVG(work_experience),1)
        FROM Customers
        WHERE annual_income > 50000 AND age < 35
        GROUP BY profession
    """)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    
    result = []
    for row in rows:
        result.append({
            "Profession": row[0],
            "AverageWorkExperience": float(row[1])
        })

    return jsonify(result)

@app.route("/average_spending_score/<string:profession>", methods=["GET"])
def average_spending_score(profession):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT gender, ROUND(AVG(spending_score),1)
        FROM Customers
        WHERE profession = %s
        GROUP BY gender
    """, (profession,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    if not rows:
        return jsonify({"error": "Profession not found"}), 404

    result=[]
    for row in rows:
        result.append({
            "AverageSpendingScore": float(row[1]),
            "Gender":row[0]
        })
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)



