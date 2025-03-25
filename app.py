from flask import Flask, render_template, request
import pyodbc

app = Flask(__name__)

# Connexion à la base Azure SQL
def get_db_connection():
    conn = pyodbc.connect(
        'Driver={ODBC Driver 18 for SQL Server};'
        'Server=tcp:sql-oumayma-server.database.windows.net,1433;'
        'Database=bdoumouhou;'
        'Uid=adminoumayma;'
        'Pwd=Oumayma16;'  # ← vérifie bien le mot de passe ici
        'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    )
    return conn

@app.route('/', methods=['GET', 'POST'])
def home():
    message = ""
    if request.method == 'POST':
        name = request.form['name']
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
            conn.commit()
            conn.close()
            message = f"Bienvenue {name} ! (ajouté dans la base de données ✅)"
        except Exception as e:
            message = f"Erreur lors de la connexion à la base : {e}"

    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
