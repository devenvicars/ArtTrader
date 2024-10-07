from flask_app.config.mysql_connection import connectToMySQL
from flask_app import bcrypt
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

NAME_REGEX = re.compile(r'^[a-zA-Z]+$')


class User:
    DB = 'creations_db' 

    def __init__(self, data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def add_new_user(cls,data):
        data['password'] = bcrypt.generate_password_hash(data['password'])
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        """
        return connectToMySQL(User.DB).query_db(query,data)

    @classmethod
    def login_user(cls,data):
        return User.get_user_by_email(data)
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash('First Name must be at least 2 character long.','warning')
            is_valid = False
        if not NAME_REGEX.match(user['first_name']):
            is_valid - False
        if len(user['last_name']) < 2:
            flash('Last Name must be at least 2 character.','warning')
            is_valid = False
        if not NAME_REGEX.match(user['last_name']):
            is_valid = False
            flash('Name may only contain letters.','warning')
        if not EMAIL_REGEX.match(user['email']):
            flash('Please enter a valid email.','warning')
            is_valid = False
        if len(User.get_user_by_email(user)) > 0:
            is_valid = False
            flash('Email already in use.','warning')
        if len(user['password']) < 8:
            flash('Password must be at least 8 characters.','warning')
            is_valid = False
        if (user['password']) != (user['confirm_password']):
            flash('Passwords do not match')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']):
            flash('Please enter a valid email.')
            is_valid = False
        results = User.get_user_by_email(user)
        if not len(results) > 0:
            is_valid = False
            flash('Email does not exist.','error')
        if not any (bcrypt.check_password_hash(d['password'], user['password']) for d in results):
            flash('Password invalid.','error')
            is_valid = False
        return is_valid

    @classmethod
    def get_user_by_email(cls, data):
        query = """
        SELECT * FROM users
        WHERE  email = %(email)s
        """
        return connectToMySQL(User.DB).query_db(query,data)
    
    @classmethod
    def get_all_user_emails(cls,data):
        query = """
        SELECT email FROM users;
        """
        return connectToMySQL(User.DB).query_db(query,data)
    
    @classmethod
    def get_user_by_id(cls,data):
        query = """
        SELECT * FROM users
        WHERE  id = %(id)s
        """
        return connectToMySQL(User.DB).query_db(query,data)