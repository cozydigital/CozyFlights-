from flask import Flask, request, jsonify, send_from_directory
import sqlite3, os, json
from datetime import datetime

app = Flask(__name__, static_folder='public')
DB = 'skyroute.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS flight_bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        trip_type TEXT NOT NULL,
        from_city TEXT NOT NULL,
        to_city TEXT NOT NULL,
        departure_date TEXT NOT NULL,
        return_date TEXT,
        passengers INTEGER NOT NULL,
        cabin_class TEXT NOT NULL,
        special_requests TEXT,
        status TEXT DEFAULT 'pending',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS hotel_bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        destination TEXT NOT NULL,
        check_in TEXT NOT NULL,
        check_out TEXT NOT NULL,
        rooms INTEGER NOT NULL,
        guests INTEGER NOT NULL,
        room_type TEXT NOT NULL,
        budget_range TEXT NOT NULL,
        special_requests TEXT,
        status TEXT DEFAULT 'pending',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS transfer_bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        transfer_type TEXT NOT NULL,
        pickup_location TEXT NOT NULL,
        dropoff_location TEXT NOT NULL,
        pickup_date TEXT NOT NULL,
        pickup_time TEXT NOT NULL,
        passengers INTEGER NOT NULL,
        vehicle_type TEXT NOT NULL,
        flight_number TEXT,
        special_requests TEXT,
        status TEXT DEFAULT 'pending',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS cargo_bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        service_type TEXT NOT NULL,
        origin TEXT NOT NULL,
        destination TEXT NOT NULL,
        pickup_date TEXT NOT NULL,
        cargo_type TEXT NOT NULL,
        weight_kg REAL NOT NULL,
        dimensions TEXT,
        fragile INTEGER DEFAULT 0,
        special_requests TEXT,
        status TEXT DEFAULT 'pending',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    conn.commit()
    conn.close()

# ── ROUTES ──

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/admin')
def admin():
    return send_from_directory('public', 'admin.html')

# Flight booking
@app.route('/api/book/flight', methods=['POST'])
def book_flight():
    d = request.json
    required = ['full_name','email','phone','trip_type','from_city','to_city','departure_date','passengers','cabin_class']
    missing = [f for f in required if not d.get(f)]
    if missing:
        return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400
    conn = get_db()
    conn.execute('''INSERT INTO flight_bookings
        (full_name,email,phone,trip_type,from_city,to_city,departure_date,return_date,passengers,cabin_class,special_requests)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
        (d['full_name'],d['email'],d['phone'],d['trip_type'],d['from_city'],d['to_city'],
         d['departure_date'],d.get('return_date'),d['passengers'],d['cabin_class'],d.get('special_requests')))
    conn.commit()
    ref = f'SR-FL-{datetime.now().strftime("%y%m%d")}-{conn.execute("SELECT last_insert_rowid()").fetchone()[0]:04d}'
    conn.close()
    return jsonify({'success': True, 'message': 'Flight booking received!', 'reference': ref})

# Hotel booking
@app.route('/api/book/hotel', methods=['POST'])
def book_hotel():
    d = request.json
    required = ['full_name','email','phone','destination','check_in','check_out','rooms','guests','room_type','budget_range']
    missing = [f for f in required if not d.get(f)]
    if missing:
        return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400
    conn = get_db()
    conn.execute('''INSERT INTO hotel_bookings
        (full_name,email,phone,destination,check_in,check_out,rooms,guests,room_type,budget_range,special_requests)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
        (d['full_name'],d['email'],d['phone'],d['destination'],d['check_in'],d['check_out'],
         d['rooms'],d['guests'],d['room_type'],d['budget_range'],d.get('special_requests')))
    conn.commit()
    ref = f'SR-HT-{datetime.now().strftime("%y%m%d")}-{conn.execute("SELECT last_insert_rowid()").fetchone()[0]:04d}'
    conn.close()
    return jsonify({'success': True, 'message': 'Hotel booking received!', 'reference': ref})

# Transfer booking
@app.route('/api/book/transfer', methods=['POST'])
def book_transfer():
    d = request.json
    required = ['full_name','email','phone','transfer_type','pickup_location','dropoff_location','pickup_date','pickup_time','passengers','vehicle_type']
    missing = [f for f in required if not d.get(f)]
    if missing:
        return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400
    conn = get_db()
    conn.execute('''INSERT INTO transfer_bookings
        (full_name,email,phone,transfer_type,pickup_location,dropoff_location,pickup_date,pickup_time,passengers,vehicle_type,flight_number,special_requests)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
        (d['full_name'],d['email'],d['phone'],d['transfer_type'],d['pickup_location'],d['dropoff_location'],
         d['pickup_date'],d['pickup_time'],d['passengers'],d['vehicle_type'],d.get('flight_number'),d.get('special_requests')))
    conn.commit()
    ref = f'SR-TR-{datetime.now().strftime("%y%m%d")}-{conn.execute("SELECT last_insert_rowid()").fetchone()[0]:04d}'
    conn.close()
    return jsonify({'success': True, 'message': 'Transfer booking received!', 'reference': ref})

# Cargo booking
@app.route('/api/book/cargo', methods=['POST'])
def book_cargo():
    d = request.json
    required = ['full_name','email','phone','service_type','origin','destination','pickup_date','cargo_type','weight_kg']
    missing = [f for f in required if not d.get(f)]
    if missing:
        return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400
    conn = get_db()
    conn.execute('''INSERT INTO cargo_bookings
        (full_name,email,phone,service_type,origin,destination,pickup_date,cargo_type,weight_kg,dimensions,fragile,special_requests)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
        (d['full_name'],d['email'],d['phone'],d['service_type'],d['origin'],d['destination'],
         d['pickup_date'],d['cargo_type'],d['weight_kg'],d.get('dimensions'),1 if d.get('fragile') else 0,d.get('special_requests')))
    conn.commit()
    ref = f'SR-CG-{datetime.now().strftime("%y%m%d")}-{conn.execute("SELECT last_insert_rowid()").fetchone()[0]:04d}'
    conn.close()
    return jsonify({'success': True, 'message': 'Cargo booking received!', 'reference': ref})

# Admin: get all bookings
@app.route('/api/admin/bookings', methods=['GET'])
def get_all_bookings():
    conn = get_db()
    result = {}
    for table in ['flight_bookings','hotel_bookings','transfer_bookings','cargo_bookings']:
        rows = conn.execute(f'SELECT * FROM {table} ORDER BY created_at DESC').fetchall()
        result[table] = [dict(r) for r in rows]
    conn.close()
    return jsonify(result)

# Admin: update booking status
@app.route('/api/admin/bookings/<table>/<int:bid>', methods=['PATCH'])
def update_status(table, bid):
    allowed = ['flight_bookings','hotel_bookings','transfer_bookings','cargo_bookings']
    if table not in allowed:
        return jsonify({'error': 'Invalid table'}), 400
    status = request.json.get('status')
    if status not in ['pending','confirmed','cancelled']:
        return jsonify({'error': 'Invalid status'}), 400
    conn = get_db()
    conn.execute(f'UPDATE {table} SET status=? WHERE id=?', (status, bid))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

if __name__ == '__main__':
    init_db()
    print('\n✅  SkyRoute server running at http://localhost:5000')
    print('📋  Admin dashboard at http://localhost:5000/admin\n')
    app.run(debug=True, port=5000)
