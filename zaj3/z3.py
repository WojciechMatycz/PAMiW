from flask import Flask, session, request, render_template, redirect, url_for, abort, send_from_directory
from werkzeug.utils import secure_filename
import os
import zaj3.file_manager as f_manager
import zaj3.db_manager as db_manager
import zaj3.validator as validator
import hashlib
import uuid

user_dict = {}

app = Flask(__name__)
app.secret_key = b'tester1209'
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
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
    if request.form['submit-button'] == 'Zarejestruj się':
        return redirect(url_for('register'))
    elif request.form['submit-button'] == 'Zaloguj':
        if validator.validate_user([request.form['login'], request.form['password']]):
            sid = uuid.uuid4()
            user_dict[sid] = request.form['login']
            session['session'] = sid
            return redirect(url_for('userPage'))
        else:
            return redirect(url_for('login', message='Błędny login lub hasło'))


@app.route('/matyczw/z3/userPage', methods=['GET', 'POST'])
def userPage():
    if check_if_user_logged():

        if request.method == 'POST':
            file_name = request.form['save-button']
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
        if request.args.get('message') is not None:
            return render_template('userPage.html', message=request.args.get('message'), username=username, files=files_list,
                                   number_of_files=number_of_files)
        else:
            return render_template("userPage.html", username=username, files=files_list,
                                   number_of_files=number_of_files)
    else:
        abort(401)


@app.route('/matyczw/z3/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and check_if_user_logged():
        if 'file' not in request.files:
            return redirect(url_for('userPage', message='Nie podano pliku'))

        file = request.files['file']
        if file.filename == '':
            redirect(url_for('userPage', message='Nie podano pliku'))

        username = get_current_user()

        if file and count_space_left('userDirs/' + username + '/') > 0:
            user_path = 'userDirs/' + username + '/'
            filename = secure_filename(file.filename)
            file.save(os.path.join(user_path, filename))
            return redirect(url_for('userPage', message='Pomyślnie dodano plik'))
        else:
            return redirect(url_for('userPage', message='Wykorzystałeś swój limit'))

    elif check_if_user_logged():
        return redirect(url_for('userPage'))
    else:
        return redirect(url_for('login'))


@app.route('/matyczw/z3/delete', methods=["POST"])
def delete():
    username = get_current_user()
    user_path = 'userDirs/' + username + '/'
    fname = request.form['delete-button']
    if fname is not None:
        os.remove(user_path + fname)
        return redirect(url_for('userPage'))
    else:
        abort(505)


@app.route('/matyczw/z3/logout', methods=['POST'])
def logout():
    user_dict.pop(session.get('session'))
    session.pop('session')
    return redirect(url_for('login'))


@app.route('/matyczw/z3/register', methods=['GET'])
def register():
    return render_template('register.html')


@app.route('/matyczw/z3/handle_register', methods=["POST"])
def handle_register():
    if request.form['login'] != '' and request.form['password'] != '':
        username = request.form['login']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        result = db_manager.add_user_to_db(username, password)
        if result:
            if check_if_user_logged():
                user_dict.pop(session.get('session'))
                session.pop('session')
            return redirect(url_for('login', message="Pomyslnie dodano użytkownika"))
        else:
            return render_template('register.html', error="Uzytkownik o danym loginie już istnieje")
    else:
        return render_template('register.html', error='Błąd!')


def check_if_user_logged():
    sid = session.get('session')
    return user_dict.get(sid) is not None


def get_current_user():
    sid = session.get('session')
    username = user_dict[sid]
    return username


def count_space_left(user_path):
    file_list = f_manager.get_user_file_list(user_path)
    return 5 - len(file_list)


if __name__ == '__main__':
    app.run(debug=True)
