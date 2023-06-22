from flask import Flask, redirect, render_template, request
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'sqlflask'
app.config['MYSQL_PASSWORD'] = 'sqlflask'
app.config['MYSQL_DB'] = 'sae41'
mysql = MySQL(app)

def user_exists(username):
    conn = mysql.connection
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE login = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    cursor.close()
    return user is not None


def is_valid_user(username, password):
    conn = mysql.connection
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE login = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    cursor.close()
    return user is not None


def get_user_id(username):
    conn = mysql.connection
    cursor = conn.cursor()

    query = "SELECT id FROM users WHERE login = %s"
    cursor.execute(query, (username,))
    user_id = cursor.fetchone()

    cursor.close()
    return user_id[0] if user_id else None


def get_user_login(user_id):
    conn = mysql.connection
    cursor = conn.cursor()

    query = "SELECT login FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    user_login = cursor.fetchone()

    cursor.close()
    return user_login[0] if user_login else None


def get_user_meetings(user_id):
    conn = mysql.connection
    cursor = conn.cursor()

    query = "SELECT m.creation_date, d.date, d.meeting_id, a.response " \
            "FROM meetings AS m " \
            "JOIN dates AS d ON m.id = d.meeting_id " \
            "LEFT JOIN answers AS a ON d.id = a.date_id AND a.user_name = %s " \
            "WHERE m.user_id = %s"
    cursor.execute(query, (get_user_login(user_id), user_id))
    meetings = cursor.fetchall()

    cursor.close()
    return meetings


@app.route('/get-users', methods=['GET'])
def get_users():
    cursor = mysql.connection.cursor()
    query = "SELECT login FROM users"
    cursor.execute(query)
    users = [user[0] for user in cursor.fetchall()]
    cursor.close()
    return jsonify(users)


@app.route('/', methods=['GET', 'POST'])
def redirection():
	return redirect("/index.html")

@app.route('/index.html', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if is_valid_user(username, password):
            # Mot de passe correct
            return redirect('/reunion.html?user=' + username)
        else:
            # Mot de passe incorrect
            error = "Nom d'utilisateur ou mot de passe incorrect"
            return render_template('index.html', error=error)

    return render_template('index.html')


@app.route('/inscription.html', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not user_exists(username):
            cur = mysql.connection.cursor()
            cur.execute("USE sae41")
            query = "INSERT INTO users (login, password) VALUES (%s, %s)"
            values = (username, password)
            cur.execute(query, values)

            mysql.connection.commit()
            cur.close()

            return redirect('/index.html')
        else:
            error = "Nom d'utilisateur déjà utilisé"
            return render_template('inscription.html', error=error)

    return render_template('inscription.html')


@app.route('/reunion.html', methods=['GET', 'POST'])
def reunion():
    if request.method == 'POST':
        # Récupérer la date entrée dans le formulaire
        date = request.form['date']

        # Vérifier l'option d'horaire choisie par l'utilisateur
        time_option = request.form.get('time_option')
        if time_option == 'specific_time':
            # Horaire spécifique choisi
            time = request.form['specific_time']
        elif time_option == 'other_time':
            # Autre horaire choisi
            time = request.form['other_time']
        else:
            # Option d'horaire non valide, gérer l'erreur ici

        # Enregistrer la réunion dans la base de données
        # ...

        return redirect('/index.html')

    # Récupérer la liste des utilisateurs disponibles depuis la base de données
    cursor = mysql.connection.cursor()
    query = "SELECT login FROM users"
    cursor.execute(query)
    users = [user[0] for user in cursor.fetchall()]
    cursor.close()

    return render_template('reunion.html', users=users)





if __name__ == '__main__':
    app.run()
