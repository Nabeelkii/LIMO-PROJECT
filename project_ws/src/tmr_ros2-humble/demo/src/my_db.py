import sqlite3

def create_sample_database():
    # Connect to the database (or create it if it doesn't exist)
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()

    # Create the configurations table
    c.execute('''CREATE TABLE IF NOT EXISTS configurations (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    up_pose TEXT,
                    down_pose TEXT,
                    left_pose TEXT,
                    right_pose TEXT,
                    sku_number TEXT
                )''')

    # Sample data
    sample_data = [
        ('Configuration 1', '1', '1', '1', '1', '1'),
        ('Configuration 2', '2', '2', '2', '2', '2'),
        ('Configuration 3', '3', '3', '3', '3', '3'),
        # Add more sample data as needed
    ]

    # Insert sample data into the configurations table
    c.executemany("INSERT INTO configurations (name, up_pose, down_pose, left_pose, right_pose, sku_number) VALUES (?, ?, ?, ?, ?, ?)", sample_data)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_sample_database()
