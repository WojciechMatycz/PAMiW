from flask import Flask, request, redirect, abort, render_template
from werkzeug.utils import secure_filename
import os
import jwt
import zaj4.z3 as z3

app = Flask(__name__)
app.secret_key = b'tester61479254'
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    #SESSION_COOKIE_SECURE=True,
    UPLOAD_FOLDER='userDirs'
)


@app.route('/matyczw/dl/upload', methods=['GET', 'POST'])
def upload():
    token = request.form['token']
    if not token:
        return render_template('matyczw/z3/userPage', message='Brak tokenu')

    try:
        data = jwt.decode(token, b'986aasd423')
    except:
        return render_template('matyczw/z3/userPage', message='Błędny token')

    if 'file' not in request.files:
        return render_template('matyczw/z3/userPage', message='Nie podano pliku')

    file = request.files['file']
    if file.filename == '':
        render_template('matyczw/z3/userPage', message='Nie podano pliku')

    username = request.form['username']

    if file and z3.count_space_left('userDirs/' + username + '/') > 0:
        user_path = 'userDirs/' + username + '/'
        filename = secure_filename(file.filename)
        file.save(os.path.join(user_path, filename))
        return render_template('matyczw/z3/userPage', message='Pomyślnie dodano plik')
    else:
        return render_template('matyczw/z3/userPage', message='Wykorzystałeś swój limit')


@app.route('/matyczw/dl/delete', methods=["GET", "POST"])
def delete():
    token = request.form['token']
    if not token:
        return render_template('matyczw/z3/userPage', message='Brak tokenu')

    try:
        data = jwt.decode(token, b'986aasd423')
    except:
        return render_template('matyczw/z3/userPage', message='Błędny token')

    username = request.form['username']
    user_path = 'userDirs/' + username + '/'
    fname = request.form['delete-button']
    if fname is not None:
        os.remove(user_path + fname)
        return redirect('matyczw/z3/userPage')
    else:
        abort(505)

