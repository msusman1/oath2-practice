from fastapi import FastAPI, Form, Header, HTTPException
from uuid import uuid4
import psycopg2

app = FastAPI()

def get_connection():
    return psycopg2.connect(
        dbname="oath2-db",
        user="root",
        password="q3tJbd6QZiFC---",
        host="ep-purple-frost-a5qh2mmz.us-east-2.aws.neon.tech",
        sslmode="require"
    )

@app.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    if user:
        token = str(uuid4())
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET token = %s WHERE email = %s AND password = %s", (token, email, password))
        connection.commit()
        cursor.close()
        connection.close()
        return {"message": "Login Successfully", "token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid email/password combination")

@app.post("/todos")
def todos(token: str = Header(...)):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE token = %s", (token,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    if user:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM todo")
        todos = cursor.fetchall()
        cursor.close()
        connection.close()
        return {"todos": todos, "message": "Todos fetched successfully"}
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
