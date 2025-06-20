def create_table_user(c):
    c.execute(f"CREATE TABLE IF NOT EXISTS user ("
                f"id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
                f"name VARCHAR(255) NOT NULL,"
                f"password VARCHAR(255) NOT NULL,"
                f"email VARCHAR(255) NOT NULL,"
                f"created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
              )

def create_table_leaderboard(c):
    c.execute(f"CREATE TABLE IF NOT EXISTS leaderboard ("
                f"id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
                f"user_id INT NOT NULL,"
                f"score INT NOT NULL,"
                f"created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                f"update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                f"FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE)")