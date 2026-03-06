# Enhanced app.py

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Setting up database connection
DATABASE = 'skincare.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the product database
def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    price REAL NOT NULL
                );''')
    conn.commit()
    conn.close()

# Sample data
def insert_sample_data():  
    conn = get_db_connection()  
    conn.execute("INSERT INTO products (name, type, price) VALUES ('Cheap Cream', 'cheap', 5.99);")
    conn.execute("INSERT INTO products (name, type, price) VALUES ('Expensive Cream', 'expensive', 49.99);")
    conn.commit()
    conn.close()

# Dupe matching logic
def find_dupes(product_name):  
    conn = get_db_connection()  
    dupes = conn.execute('SELECT * FROM products WHERE name LIKE ?', ('%' + product_name + '%',)).fetchall()
    conn.close()  
    return [dict(dupe) for dupe in dupes]

@app.route('/search', methods=['GET'])
def search():  
    query = request.args.get('query')  
    results = find_dupes(query)  
    return jsonify(results)

if __name__ == '__main__':
    init_db()  
    insert_sample_data()  
    app.run(debug=True)