import sqlite3
from datetime import datetime

def init_database():
    conn = sqlite3.connect("healthmate.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS health_logs(
            log_id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            date DATE NOT NULL,
            weight FLOAT,
            height FLOAT,
            water_intake FLOAT,
            steps INTEGER,
            mood TEXT,
            calories INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            UNIQUE(user_id, date)
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username,email):
    conn = sqlite3.connect("healthmate.db")
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO users(username,email)
            VALUES (?,?)
        ''', (username,email))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def log_daily_data(user_id,date,weight,height,water,steps,mood,calories):
    conn = sqlite3.connect("healthmate.db")
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO health_logs
            (user_id,date,weight,height,water_intake,steps,mood,calories)
            VALUES(?,?,?,?,?,?,?,?)
        ''',(user_id,date,weight,height,water,steps,mood,calories))

        conn.commit()
        print(f"Log saved for user {user_id} on {date}")
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def view_all_users():
    conn = sqlite3.connect("healthmate.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()

    print("="*30,"USERS TABLES","="*30)
    for i in users:
        print(i)
    print()

def view_all_logs():
    conn = sqlite3.connect("healthmate.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM health_logs")
    logs = cursor.fetchall()
    conn.close()

    print("\n"+"="*120)
    print(f"{"LOG ID":<8}{"User ID":<8}{"Date":<12}{"Weight":<8}{"Height":<8}{"Water":<8}{"Steps":<8}{"Mood":<15}{"Calories":<8}")
    print("="*120)
    for log in logs:
        print(f"{log[0]:<8}{log[1]:<8}{str(log[2]):<12}{str(log[3]):<8}{str(log[4]):<8}{str(log[5]):<8}{str(log[6]):<8}{str(log[7]):<15}{str(log[8]):<8}")
    print("="*120+"\n")

if __name__ == "__main__":
    init_database()  
    print("Database initialized")
