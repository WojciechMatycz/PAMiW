from flask import Flask, session, request, render_template, redirect, url_for, abort, send_from_directory
import os
import zaj4.file_manager as f_manager
import zaj4.db_manager as db_manager
import zaj4.validator as validator
import hashlib
import uuid
import redis
import datetime
import jwt

r = redis.Redis()

app = Flask(__name__)
app.secret_key = b'tester1209'
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    #SESSION_COOKIE_SECURE=True,
    UPLOAD_FOLDER='userDirs'
)


@app.route('/matyczw/z3/')
def index():
    if check_if_user_logged():
        return redirect(url_for('userPage'))
    else:
        return redirect(url_for('login'))


@app.route('/matyczw/z3/login', methods=['POST', 'GET'])
def login():
    if not check_if_user_logged():
        if request.args.get('message') is not None:
            return render_template('login.html', message=request.args.get('message'))
        else:
            return render_template('login.html')
    else:
        return redirect(url_for('userPage'))


@app.route('/matyczw/z3/handle_login', methods=['POST'])
def handle_login():
    if request.form['submit-button'] == 'Zarejestruj sie':
        return redirect(url_for('register'))
    elif request.form['submit-button'] == 'Zaloguj':
        if validator.validate_user([request.form['login'], request.form['password']]):
            sid = uuid.uuid4()
            r.hset('matyczw:z3:' + str(sid), 'login', request.form['login'])
            session['session'] = sid
            return redirect(url_for('userPage'))
        else:
            return redirect(url_for('login', message='Bledny login lub haslo'))


@app.route('/matyczw/z3/userPage', methods=['GET', 'POST'])
def userPage():

    if check_if_user_logged():
        if request.method == 'POST':
            try:
                file_name = request.form['save-button']
            except:
                file_name = None

            if file_name:
                path = 'userDirs/' + get_current_user()
                if os.path.isfile(path + '/' + file_name):
                    return send_from_directory(directory=path, filename=file_name, as_attachment=True)
                else:
                    abort(500)

        username = get_current_user()

        f_manager.create_user_dir_if_not_exists(username)
        user_path = 'userDirs/' + username + '/'

        files_list = f_manager.get_user_file_list(user_path)
        number_of_files = count_space_left(user_path)

        token = jwt.encode({'login': username, 'sid': str(session.get('session')),
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)},
                           b'986aasd423').decode('utf-8')

        if request.args.get('message') is not None:
            return render_template('userPage.html', message=request.args.get('message'), username=username, files=files_list,
                                   number_of_files=number_of_files, token=token)
        else:
            return render_template("userPage.html", username=username, files=files_list,
                                   number_of_files=number_of_files, token=token)
    else:
        abort(401)


@app.route('/matyczw/z3/logout', methods=['POST'])
def logout():
    r.hdel('matyczw:z3:' + str(session.get('session')), 'login')
    session.pop('session')
    return redirect(url_for('login'))


@app.route('/matyczw/z3/register', methods=['GET'])
def register():
    return render_template('register.html')


@app.route('/matyczw/z3/handle_register', methods=["POST"])
def handle_register():
    if request.form['login'] != '' and request.form['password'] != '':
        username = request.form['login']
        salt = str(uuid.uuid4())
        password = hashlib.sha256((request.form['password'] + salt).encode()).hexdigest()

        result = db_manager.add_user_to_db(username, password, salt)
        if result:
            if check_if_user_logged():
                r.hdel('matyczw:z3:' + str(session.get('session')), 'login')
                session.pop('session')
            return redirect(url_for('login', message="Pomyslnie dodano użytkownika"))
        else:
            return render_template('register.html', error="Uzytkownik o danym loginie już istnieje")
    else:
        return render_template('register.html', error='Błąd!')


def check_if_user_logged():
    sid = session.get('session')
    return r.hget('matyczw:z3:'+str(sid), 'login') is not None


def get_current_user():
    sid = session.get('session')
    username = r.hget('matyczw:z3:'+str(sid), 'login').decode('utf-8')
    return username


def count_space_left(user_path):
    file_list = f_manager.get_user_file_list(user_path)
    return 5 - len(file_list)


if __name__ == '__main__':
    app.run(debug=True)
