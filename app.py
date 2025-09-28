from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('mandi.db')
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mandi_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            market TEXT,
            crop TEXT,
            price TEXT
        )
    ''')

    # Clear existing data
    cursor.execute('DELETE FROM mandi_prices')

    # Insert sample data
    sample_data = [
        ('Shirpur', 'Main Market', 'Banana', '₹60/kg'),
        ('Shirpur', 'Krishi Mandi', 'Banana', '₹58/kg'),
        ('Shirpur', 'Sabji Bazaar', 'Banana', '₹62/kg'),
        ('Shirpur', 'Main Market', 'Cotton', '₹5400/quintal'),
        ('Shirpur', 'Krishi Mandi', 'Cotton', '₹5200/quintal'),
        ('Shirpur', 'Sabji Bazaar', 'Cotton', '₹5600/quintal'),
        ('Shirpur', 'Main Market', 'Wheat', '₹25/kg'),
        ('Shirpur', 'Krishi Mandi', 'Wheat', '₹27/kg'),
        ('Shirpur', 'Sabji Bazaar', 'Wheat', '₹26/kg'),

        ('Amalner', 'Central Market', 'Banana', '₹65/kg'),
        ('Amalner', 'Agricultural Market', 'Banana', '₹63/kg'),
        ('Amalner', 'Weekly Bazaar', 'Banana', '₹67/kg'),
        ('Amalner', 'Central Market', 'Cotton', '₹5300/quintal'),
        ('Amalner', 'Agricultural Market', 'Cotton', '₹5500/quintal'),
        ('Amalner', 'Weekly Bazaar', 'Cotton', '₹5100/quintal'),
        ('Amalner', 'Central Market', 'Wheat', '₹28/kg'),
        ('Amalner', 'Agricultural Market', 'Wheat', '₹30/kg'),
        ('Amalner', 'Weekly Bazaar', 'Wheat', '₹26/kg'),

        ('Chopda', 'District Market', 'Wheat', '₹28/kg'),
        ('Chopda', 'Farmers Market', 'Wheat', '₹29/kg'),
        ('Chopda', 'Local Bazaar', 'Wheat', '₹27/kg'),
        ('Chopda', 'District Market', 'Sugarcane', '₹350/quintal'),
        ('Chopda', 'Farmers Market', 'Sugarcane', '₹380/quintal'),
        ('Chopda', 'Local Bazaar', 'Onion', '₹45/kg'),

        ('Muktai Nagar', 'Municipal Market', 'Sugarcane', '₹350/quintal'),
        ('Muktai Nagar', 'Wholesale Market', 'Sugarcane', '₹380/quintal'),
        ('Muktai Nagar', 'Evening Bazaar', 'Onion', '₹45/kg'),
        ('Muktai Nagar', 'Municipal Market', 'Banana', '₹64/kg'),
        ('Muktai Nagar', 'Wholesale Market', 'Cotton', '₹5800/quintal'),
    ]

    cursor.executemany('INSERT INTO mandi_prices (city, market, crop, price) VALUES (?, ?, ?, ?)', sample_data)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mandi')
def mandi_form():
    return render_template('mandi_form.html')

@app.route('/mandi_results', methods=['POST'])
def mandi_results():
    city = request.form['city']
    crop = request.form['crop']

    conn = sqlite3.connect('mandi.db')
    cursor = conn.cursor()

    cursor.execute('SELECT market, price FROM mandi_prices WHERE city = ? AND crop = ?', (city, crop))
    results = cursor.fetchall()
    conn.close()

    return render_template('mandi_results.html', results=results, city=city, crop=crop)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)