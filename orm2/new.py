import psycopg2
import random
import time

# Database credentials
db_name = "business_db"
db_user = "postgres"
db_password = "Sairam"
db_host = "localhost"  
db_port = "5432"  # Default PostgreSQL port

# Sample data
names = ["Company A", "Company B", "Company C", "Company D", "Company E"]
countries = ["USA", "Canada", "Germany", "India", "Australia"]

# Function to generate random business data
def generate_data():
    data = []
    for i in range(5):
        name = names[i]
        revenue = round(random.uniform(1000, 10000), 2)  # Random revenue
        profit = round(random.uniform(100, 5000), 2)  # Random profit
        employees = random.randint(10, 500)  # Integer number of employees
        country = random.choice(countries)
        data.append((name, revenue, profit, employees, country))
    return data

# Function to insert data into the 'business' table
def insert_data(conn, data):
    try:
        cur = conn.cursor()
        query = """
            INSERT INTO business (name, revenue, profit, employees, country) 
            VALUES (%s, %s, %s, %s, %s);
        """
        cur.executemany(query, data)  # Insert multiple rows
        conn.commit()  # Commit after inserting data
        print("Inserted data successfully!")
        cur.close()
    except psycopg2.Error as e:
        print(f"Error inserting data: {e}")
        conn.rollback()  # Rollback if there's an error

# Main execution loop
try:
    # Connect to the database
    conn = psycopg2.connect(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    print("Connected to PostgreSQL successfully!")

    while True:
        # Generate and insert data
        data = generate_data()
        insert_data(conn, data)

        # Print inserted data for reference
        for row in data:
            print(row)

        # Wait for 20 seconds before inserting the next batch
        time.sleep(20)

except psycopg2.Error as e:
    print(f"Error connecting to PostgreSQL: {e}")

finally:
    if 'conn' in locals() and conn is not None:
        conn.close()
        print("Database connection closed.")
