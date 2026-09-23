import sqlite3
from datetime import datetime, timedelta

def init_database():
    conn = sqlite3.connect("healthmate.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT,
            password TEXT NOT NULL,
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

def reset_database():
    """Drop all tables and recreate them."""
    conn = sqlite3.connect("healthmate.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS health_logs")
    cursor.execute("DROP TABLE IF EXISTS users")
    conn.commit()
    conn.close()
    init_database()

def add_user(username, email, password):
    conn = sqlite3.connect("healthmate.db")
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO users(username, email, password)
            VALUES (?, ?, ?)
        ''', (username, email, password))
        conn.commit()
        user_id = cursor.lastrowid
        return user_id
    except sqlite3.IntegrityError:
        cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
        existing = cursor.fetchone()
        if existing:
            return existing[0]
        return None
    finally:
        conn.close()

def login_user(email, password):
    """Authenticate a user by email and password. Returns (user_id, username) if valid."""
    conn = sqlite3.connect("healthmate.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        return user[0], user[1]
    return None, None

def log_daily_data(user_id, date, weight, height, water, steps, mood, calories):
    conn = sqlite3.connect("healthmate.db")
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT OR REPLACE INTO health_logs
            (user_id, date, weight, height, water_intake, steps, mood, calories)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, date, weight, height, water, steps, mood, calories))

        conn.commit()
        print(f"Log saved for user {user_id} on {date}")
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def get_today_log(user_id):
    """Fetch today's log for a user. Returns dict or None."""
    conn = sqlite3.connect("healthmate.db")
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute('''
        SELECT weight, height, water_intake, steps, mood, calories
        FROM health_logs WHERE user_id = ? AND date = ?
    ''', (user_id, today))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "weight": row[0], "height": row[1], "water": row[2],
            "steps": row[3], "mood": row[4], "calories": row[5]
        }
    return None

def get_weekly_logs(user_id):
    """Fetch the last 7 days of logs. Returns list of dicts."""
    conn = sqlite3.connect("healthmate.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT date, weight, height, water_intake, steps, mood, calories
        FROM health_logs
        WHERE user_id = ? AND date >= date('now', '-7 days')
        ORDER BY date ASC
    ''', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [
        {"date": r[0], "weight": r[1], "height": r[2], "water": r[3],
         "steps": r[4], "mood": r[5], "calories": r[6]}
        for r in rows
    ]

def get_recent_logs(user_id, days=14):
    """Fetch the last N days of logs for charts. Returns list of dicts."""
    conn = sqlite3.connect("healthmate.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT date, weight, height, water_intake, steps, mood, calories
        FROM health_logs
        WHERE user_id = ? AND date >= date('now', ? || ' days')
        ORDER BY date ASC
    ''', (user_id, f"-{days}"))
    rows = cursor.fetchall()
    conn.close()
    return [
        {"date": r[0], "weight": r[1], "height": r[2], "water": r[3],
         "steps": r[4], "mood": r[5], "calories": r[6]}
        for r in rows
    ]

def get_month_log_dates(user_id, year, month):
    """Return set of day numbers in a month that have logs."""
    conn = sqlite3.connect("healthmate.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT CAST(strftime('%d', date) AS INTEGER)
        FROM health_logs
        WHERE user_id = ? AND strftime('%Y', date) = ? AND strftime('%m', date) = ?
    ''', (user_id, str(year), f"{month:02d}"))
    rows = cursor.fetchall()
    conn.close()
    return {r[0] for r in rows}

def view_all_users():
    conn = sqlite3.connect("healthmate.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username, email, password, created_at FROM users")
    users = cursor.fetchall()
    conn.close()

    print("="*30, "USERS TABLE", "="*30)
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
    print(f"{'LOG ID':<8}{'User ID':<8}{'Date':<12}{'Weight':<8}{'Height':<8}{'Water':<8}{'Steps':<8}{'Mood':<15}{'Calories':<8}")
    print("="*120)
    for log in logs:
        mood_str = str(log[7]).encode('ascii', 'replace').decode()
        print(f"{log[0]:<8}{log[1]:<8}{str(log[2]):<12}{str(log[3]):<8}{str(log[4]):<8}{str(log[5]):<8}{str(log[6]):<8}{mood_str:<15}{str(log[8]):<8}")
    print("="*120+"\n")

def seed_mock_data():

    user_id = add_user("Mahi", "mahi@gmail.com", "123456")
    print(f"Mock user created with user_id: {user_id}")

    today = datetime.now().date()
    mock_data = [
        (6, 66.2, 172, 1500, 7200,  "😤 Stressed", 1520),
        (5, 65.8, 172, 1800, 8500,  "😐 Neutral",  1750),
        (4, 66.5, 172, 2000, 9200,  "😐 Neutral",  1980),
        (3, 65.5, 172, 1600, 7800,  "😤 Stressed", 1600),
        (2, 66.0, 172, 1900, 10000, "😐 Neutral",  1850),
        (1, 67.0, 172, 1700, 8800,  "😤 Stressed", 1700),
        (0, 65.8, 172, 2000, 9500,  "😐 Neutral",  1900),
    ]

    for days_ago, weight, height, water, steps, mood, calories in mock_data:
        log_date = today - timedelta(days=days_ago)
        log_daily_data(user_id, log_date, weight, height, water, steps, mood, calories)

    print(f"Inserted {len(mock_data)} mock health logs for Mahi")

if __name__ == "__main__":
    reset_database()
    print("Database reset and initialized\n")

    seed_mock_data()
    print()

    view_all_users()
    view_all_logs()
