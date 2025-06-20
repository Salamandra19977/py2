import hashlib

import pymysql
from migration import *

db = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    database='game'
)

c = db.cursor()

create_table_user(c)
create_table_leaderboard(c)

def register_user(name, password, email):
    if login_user(name, password):
        return False
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        c.execute(f"INSERT INTO user (name, password, email) "
                  f"VALUES ('{name}', '{hashed_password}', '{email}')")
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False

def login_user(name, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    c.execute(f"SELECT id FROM user WHERE name = '{name}' AND password = '{hashed_password}'")
    result = c.fetchone()
    if result:
        return result[0]
    else:
        return False

def update_score(user_id, new_score):
    new_score = int(new_score)
    c.execute("SELECT id FROM leaderboard WHERE user_id = %s", (user_id,))
    result = c.fetchone()

    if result:
        c.execute(
            "UPDATE leaderboard SET score = %s, update_at = CURRENT_TIMESTAMP WHERE user_id = %s",
            (new_score, user_id)
        )
    else:
        c.execute(
            "INSERT INTO leaderboard (user_id, score) VALUES (%s, %s)",
            (user_id, new_score)
        )
    db.commit()

def get_user_score(c, user_id):
    c.execute(f"SELECT score, update_at FROM leaderboard WHERE user_id = {user_id}")
    result = c.fetchone()
    if result:
        return result
    else:
        return None

def get_leaderboard(limit=10):
    c.execute("""
        SELECT user_id, score
        FROM leaderboard
        ORDER BY score DESC
        LIMIT %s
    """, (limit,))
    results = c.fetchall()
    return results
