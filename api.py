from fastapi import FastAPI
from database import *
app = FastAPI()

@app.get("/leaderboard")
async def get_leaderboard():
   c.execute(f"SELECT * FROM leaderboard")
   data = c.fetchall()
   return data