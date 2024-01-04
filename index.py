from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

# MySQL Configuration
mysql_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'restapi_user',
    'password': 'xD*)J){XPf+)',
    'database': 'edgkuujo_rest-api'
}

# Test MySQL connection
try:
    conn = mysql.connector.connect(**mysql_config)
    conn.close()
except mysql.connector.Error as e:
    print(f"Error connecting to MySQL: {e}")
    exit(1)

# Models
class Item(BaseModel):
    name: str
    description: str = None

# Create a table if not exists
conn = mysql.connector.connect(**mysql_config)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        description VARCHAR(255)
    )
""")
conn.close()

# Routes
@app.post("/items/")
async def create_item(item: Item):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()

    add_item = ("INSERT INTO items (name, description) VALUES (%s, %s)")
    item_data = (item.name, item.description)

    cursor.execute(add_item, item_data)
    conn.commit()

    new_item_id = cursor.lastrowid
    conn.close()
    return {"id": new_item_id, **item.dict()}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor(dictionary=True)

    query = ("SELECT * FROM items WHERE id = %s")
    cursor.execute(query, (item_id,))

    item = cursor.fetchone()

    conn.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
