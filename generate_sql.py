#lab 2- 620165751 
#Python file needed to generate sql inserts and create database and table

import pandas as pd

#allocating files too variables

#given spreadsheet with customer info
CSV_FILE= "Customers.csv"

#sql output file
OUTPUT_SQL = "customer_db.sql"

#storing the names of the database and the table name
DB_NAME = "shop_db"
TABLE_NAME= "Customers"



#prevent SQL injection by escaping special characters 
def sql_escape(value):
    if pd.isna(value):
        return "NULL"
    if isinstance(value,str):
        return "'" + value.replace("\\", "\\\\").replace("'", "''") + "'"
    if isinstance(value, (int, float)):
        if float(value).is_integer():
            return str(int(value))
        return str(value)
    return "'" + str(value).replace("\\", "\\\\").replace("'", "''") + "'"


def main():
    #dictionary using pandas function
    df = pd.read_csv(CSV_FILE)

    #output lines for sql stores in a list of fstrings
    sql_lines = [ f"DROP DATABASE IF EXISTS {DB_NAME};",
            f"CREATE DATABASE {DB_NAME};",
            f"USE {DB_NAME};"
            "",
            f"DROP TABLE IF EXISTS {TABLE_NAME};",
            f"""CREATE TABLE {TABLE_NAME}(
                customer_id INT PRIMARY KEY,
                gender VARCHAR(10) NOT NULL,
                age INT NOT NULL, 
                annual_income INT NOT NULL,
                spending_score INT NOT NULL,
                profession VARCHAR(20) NULL,
                work_experience INT NOT NULL,
                family_size INT NOT NULL);""",
            "",
            f"INSERT INTO {TABLE_NAME}(customer_id, gender, age, annual_income, spending_score, profession, work_experience, family_size) VALUES",

    ]

    #iterate the escape function over dictionary for insert queries
    rows =[]
    for _, row in df.iterrows():
        values = [
            sql_escape(row["CustomerID"]),
            sql_escape(row["Gender"]), 
            sql_escape(row["Age"]),
            sql_escape(row["Annual Income ($)"]),
            sql_escape(row["Spending Score (1-100)"]),
            sql_escape(row["Profession"]),
            sql_escape(row["Work Experience"]),
            sql_escape(row["Family Size"]),
        ]
        rows.append("  (" +", ".join(values) + ")")

    sql_lines.append(",\n".join(rows) + ";")

    

    with open(OUTPUT_SQL, "w", encoding="utf-8") as file:
        file.write("\n".join(sql_lines))

    print(f"SQL script generated successfully: {OUTPUT_SQL}")


if __name__ == "__main__":
    main()


