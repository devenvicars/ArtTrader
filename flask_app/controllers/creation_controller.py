from flask_app import app
from flask_app.models.creation_model import Creation
from flask_app.models.user_model import User
from flask_app.models.purchase_model import Purchase
from flask import request, redirect, url_for, session, render_template, flash

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please Sign In!')
        return redirect('/')
    data = {
        **session,
        'id' : session['user_id']
    }
    user = User.get_user_by_id(data)
    creations = Creation.get_all_creations()
    purchase_data = {
        'user_id': session['user_id']
        }   
    purchases = Purchase.get_all_purchases_by_user_id(purchase_data)
    for purchase in purchases:
        purchased_creations = Creation.get_creation_by_id({'id': purchase.creation_id})
    return render_template('dashboard.html', creations=creations,user=user[0], purchased_creations = purchased_creations)

@app.route('/creations/new', methods = ['GET','POST'])
def add_new_creation():
    if 'user_id' not in session:
        flash('Please Sign In!')
        return redirect('/')
    if request.method == 'POST':
        user = User.get_user_by_id({'id' : session['user_id']})[0]
        data = {
            **request.form,
            'user_id':session['user_id']
        }
        if not Creation.validate_creation(data):
            return redirect(url_for('add_new_creation'))
        id = Creation.add_new_creation(data)
        return redirect(url_for('dashboard'))
    else:
        data = {
        'id' : session['user_id']
        }
        user = User.get_user_by_id(data)
        return render_template('add_creation.html', user = user)
    
@app.route('/creations/<int:id>', methods = ['GET', 'POST'])
def read_one_creation(id):
    if 'user_id' not in session:
        flash('Please Sign In!')
        return redirect('/')
    data = {
        'id': id
        }
    user_data = {
        'id' : session['user_id']
    }
    creation = Creation.get_creation_by_id(data)
    user = User.get_user_by_id(user_data)
    return render_template('view_creation.html', creation=creation[0], user=user[0])
    
@app.route('/creations/purchase/<int:id>', methods = ['POST'])
def add_purchase(id):
    data = {
        'id' : id
    }
    creation = Creation.get_creation_by_id(data)
    print(creation)
    if len(creation) > 0:
        data = {
            'user_id' : session['user_id'],
            'creation_id' : id
            }
        Purchase.add_purchase(data)
        data = {
            'id' : id,
            'quantity': creation[0].quantity - 1
        }
        Creation.delete_one_from_quantity(data)
        return redirect(url_for('dashboard'))
    else:
        flash('No creations found matching id!')
        return redirect(url_for('dashboard'))

@app.route('/creations/edit/<int:id>', methods = ['GET', 'POST'])
def edit_creation(id):
    if 'user_id' not in session:
        flash('Please Sign In!')
        return redirect('/')
    if request.method == 'POST':
        data = {
            **request.form,
            'id': id
        }
        if not Creation.validate_creation(data):
            return redirect(url_for('edit_creation', id = id))
        Creation.edit_by_id(data)
        return redirect(url_for('dashboard'))
    else:
        data = {
            'id' : id
        }
        creation = Creation.get_creation_by_id(data)
        return render_template('edit_creation.html', creation=creation[0])

@app.route('/creations/delete/<int:id>', methods = ['POST'])
def delete_creation(id):
    if 'user_id' not in session:
        flash('Please Sign In!')
        return redirect('/')
    data = { 
        'id' : id
    }
    Creation.delete_by_id(data)
    return redirect(url_for('dashboard'))