
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'chiara_secret_key'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['macchina'] = user['macchina']
            if user['role'] == 'ufficio':
                return redirect(url_for('ufficio'))
            else:
                return redirect(url_for('operatore'))
        else:
            error = 'Credenziali non valide'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/ufficio')
def ufficio():
    if 'user_id' not in session or session['role'] != 'ufficio':
        return redirect(url_for('login'))
    conn = get_db_connection()
    lavorazioni = conn.execute('SELECT * FROM lavorazioni').fetchall()
    utenti = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('ufficio.html', lavorazioni=lavorazioni, utenti=utenti)

@app.route('/operatore')
def operatore():
    if 'user_id' not in session or session['role'] != 'operatore':
        return redirect(url_for('login'))
    macchina = session['macchina']
    conn = get_db_connection()
    lavorazioni = conn.execute('SELECT * FROM lavorazioni WHERE macchina = ?', (macchina,)).fetchall()
    conn.close()
    return render_template('pagina_operatore.html', lavorazioni=lavorazioni, macchina=macchina)

@app.route('/aggiungi_lavorazione', methods=['POST'])
def aggiungi_lavorazione():
    if 'user_id' not in session or session['role'] != 'ufficio':
        return redirect(url_for('login'))
    descrizione = request.form['descrizione']
    macchina = request.form['macchina']
    data_richiesta = request.form['data_richiesta']
    conn = get_db_connection()
    conn.execute('INSERT INTO lavorazioni (descrizione, macchina, data_richiesta) VALUES (?, ?, ?)',
                 (descrizione, macchina, data_richiesta))
    conn.commit()
    conn.close()
    return redirect(url_for('ufficio'))

if __name__ == '__main__':
    app.run(debug=True)
