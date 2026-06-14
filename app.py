import os
import random
import string
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)

def get_db():
    import psycopg2
    return psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD')
    )

def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.get_json()
    long_url = data.get('url')
    code = generate_code()
    conn = get_db()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS urls (code VARCHAR(10), url TEXT)')
    cur.execute('INSERT INTO urls (code, url) VALUES (%s, %s)', (code, long_url))
    conn.commit()
    conn.close()
    return jsonify({'short_code': code})

@app.route('/<code>')
def redirect_url(code):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT url FROM urls WHERE code = %s', (code,))
    result = cur.fetchone()
    conn.close()
    if result:
        return redirect(result[0])
    return jsonify({'error': 'URL not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)