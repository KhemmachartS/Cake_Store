import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ตั้งค่า Path สำหรับ PythonAnywhere (แก้ USERNAME เป็นของคุณ)
# หากรันในเครื่องตัวเอง ระบบจะใช้โฟลเดอร์ปัจจุบันอัตโนมัติ
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'cake_store.db')

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cakes = conn.execute('''
        SELECT Cakes.*, Categories.name as category_name 
        FROM Cakes 
        JOIN Categories ON Cakes.category_id = Categories.id
    ''').fetchall()
    categories = conn.execute('SELECT * FROM Categories').fetchall()
    conn.close()
    return render_template('index.html', cakes=cakes, categories=categories)

@app.route('/add_cake', methods=['POST'])
def add_cake():
    name = request.form['name']
    price = request.form['price']
    stock = request.form['stock']
    cat_id = request.form['category_id']
    conn = get_db_connection()
    conn.execute('INSERT INTO Cakes (name, price, stock, category_id) VALUES (?, ?, ?, ?)',
                 (name, price, stock, cat_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit_cake/<int:id>', methods=['POST'])
def edit_cake(id):
    name = request.form['name']
    price = request.form['price']
    stock = request.form['stock']
    cat_id = request.form['category_id']
    conn = get_db_connection()
    conn.execute('UPDATE Cakes SET name=?, price=?, stock=?, category_id=? WHERE id=?',
                 (name, price, stock, cat_id, id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete_cake/<int:id>')
def delete_cake(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Cakes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)