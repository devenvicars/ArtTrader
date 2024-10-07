from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.purchase_model import Purchase
from flask import redirect, url_for, request, render_template,session


@app.route('/', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = {
            **request.form
        }
        if 'first_name' in data:
            if not User.validate_user(data):
                return redirect(url_for('login'))

            User.add_new_user(data)
            return redirect(url_for('login'))
        else:
            if not User.validate_login(data):
                return redirect(url_for('login'))

            results = User.login_user(data)[0]
            session['user_id'] = results['id'] 
            return redirect(url_for('dashboard'))
    else:
        return render_template('registration_login.html')

@app.route('/logout', methods = ['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))

